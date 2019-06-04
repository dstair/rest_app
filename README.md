# rest_app
A basic REST API built using Python and Flask.

### Installation instructions

This code was tested on a Mac running OSX 10.14.5, using Python 3.7.3. Because we are using virtualenv, this setup should be somewhat compatible across platforms.

1. Clone the repo; create a virtualenv; activate it; and install required packages:

        git clone git@github.com:dstair/rest_app
        cd rest_app
        # Here my virtualenv version is Python 3, and the venv created points to a Python 3 installation
        #  I installed Python 3 using 'brew install python@3'
        virtualenv venv
        cd venv
        source ./bin/activate
        pip install -r requirements.txt
        cd api

1. Set up the database (this is not yet automated). From the api/ folder run:

        sqlite3 rest_api.db

        DROP TABLE IF EXISTS people;

        CREATE TABLE people(
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          name STRING NOT NULL, 
          age INTEGER NOT NULL, 
          locale STRING NOT NULL
        );

1. Run the tests - 5 of the 6 tests should pass. From the api/ folder run:

        python test_server.py

1. You should be able to run the app now.

        # (we are now in rest_app/venv/api)
        FLASK_APP=server.py FLASK_ENV=development flask run

1. The app should now be up and running. If you would like, you can manually test the endpoints using the following curl commands:

        TEST PUT:
          curl http://localhost:5000/resources/data/ -d 'data={"name": "peter", "locale": "NYC", "age": 42}' -X PUT -v
        TEST GET:
          curl http://localhost:5000/resources/data/1 -v
        TEST DELETE:
          curl http://localhost:5000/resources/data/1 -X DELETE -v


### Deploying the API

I chose to look at 2 services on different ends of the spectrum in terms of being "fully managed" vs "fully configurable". Regardless of which one you chose, you would want to swap in a production server instead of the built in Flask development server; configure a secret key; and build a distribution file.

Heroku:
 
- Pros: provides a fully managed deployment. Deployment is as easy as pushing via git, and can be done frequently. It is also possible to set up easy CI integration.
- Cons:
Heroku offers relatively less flexibility than, say, AWS. You can't SSH on to the instance running your app. You can't install languages or libraries outside of what Heroku supports. If you want to integrate with a service like S3, you need to see what is available in the Heroku Marketplace, and you will pay a significant premium over what you would going through AWS. Also, storage and compute shapes and sizes are much more limited.

AWS Elastic Beanstalk:
- Pros:
Auto scaling with a load balancer. Pay only for the AWS resources you use. AWS has a large number of users, so the service you are running on is stable.
- Cons:
You can SSH on to the underlying EC2 instances, which means you could break things. You also have a lot more choices in terms of instance size, auto scaling threshold, etc. It's somewhat easy to make a mistake - for example, setting overly aggressive auto scaling policies without scale-back rules could result in a large bill. Deploying code to your instances is a DIY project. You need to plug in your database yourself.


### Pseudocode for deployment

For Heroku:
- Sign up for a Heroku account
- Create a new Heroku application
- On your laptop, set up git to have a second remote called "heroku"
- Install a production grade server and set a config file that Heroku will use to recognize it
- Push your code to Heroku (git push heroku)

For AWS Elastic Beanstalk:
- log in to the aws console
- create elastic beanstalk app
- copy build file on to corresponding EC2 instances (ideally with an automated deploy script)
- run build file with a production-grade server

### Securing the endpoint

There are a number of layers of security which can be added:
- employing good design principles for seucrity: principle of least privilege, open design, fail-safe defaults.
- requiring SSL encryption. 
- adding token based authentication
- expiring sessions after a limited amount of time.
- if the application only needs to be available to a certain set of IP addresses (for example, 50 customers; or, every IP address in the U.S.), access can be restricted based on source IP.
- Third parties like Carbon Black or Symantec also provide paid endpoint protection.

### Monitoring the endpoint

We will want data on uptime, performance, error rates, and usage. The choice of which technology to use will be tied to how we deploy the API. If we deploy on the Google Cloud's Google App Engine, for example, we will have very good visiblity in to the usage, latency, and error rates of each individual endpoint, as well as access to error logs, meaning we have little to no work to do for monitoring. If we wanted to choose our own monitoring solution, we could add monitoring probes in key sections of our API's code base (examples: DataDog, flask-monitor). If we want an external solution, we could consider using something like Postman Monitoring, which could send requests to our API and store performance data over time. External apps have the disadvantage of only being able to record externally visible characteristics (i.e., latency but not total usage).

### Scaling

Fortunately, the API is stateless - all state exists in the database, and responses are sent only after a successful database write. So, a large number of copies of the application can run in individual containers. However, they would need to be placed behind a load balancer; and some database performance considerations would need to be made on the back end. Typically auto-scaling to meet continuously increasing demand would be done by picking a metric - such as CPU utilization, or requests per second - and adding more containers or instances to that application when a certain threshold is exceeded. An example threshold might be 80%+ CPU usage for 10 seconds.

For the back end database, say we are using Postgres in production. Postgres can comfortably handle 10,000 writes/second on a single instance. We would want to ensure that Postgres can accept a large number of incoming connections that is proportionate to the number of containers connecting; and we would want to enable connection pooling for more efficient resource usage. We could also run some optimizations on the "people" table based on usage - for example, creating an index on "id", and possibly partitioning for faster lookups.



