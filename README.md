# django-rest-framework-orientdb-postgresql

- [Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

- [Orientdb](https://orientdb.com/) is the first multi-model database. Fastest graph database

- [PostgreSQL](https://www.postgresql.org/) is the World's Most Advanced Open Source Relational Database

What would happen if we integrate this technologies?...Let's check it!

## Requirements
- Ubuntu 18
- Orientdb: follow [next steps](https://computingforgeeks.com/how-to-install-and-configure-orientdb-on-ubuntu-18-04-lts/) to install it
- Install PostgreSQL:
```
  sudo apt-get update
  sudo apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev
```
## Installation

Create your virtualenv (see Troubleshooting section) and install the requirements:

	virtualenv env --python=python3
	source env/bin/activate

	pip install -r requirements.txt

Create logs folder:

	mkdir logs

The structure of the **settings.ini** file, is described below:

	[postgresdbConf]
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=dbname
	DB_USER=user
	DB_PASS=password
	DB_HOST=host
	DB_PORT=port

	[orientdbConf]
	DB_NAME=dbname
	DB_USER=user
	DB_PASS=password
	DB_HOST=host
	DB_PORT=host

Fill in with your own PostgreSQL and OrientDB credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432 and in OrientDB localhost/2424 (OrientDB Studio is 2480).

Run the migrations (to PostgreSQL):

	python manage.py makemigrations

	python manage.py migrate

Run the server:

	python manage.py runserver

You could see the home page in:

	http://127.0.0.1:8000/

## Models

There are 4 main models :
- Users: are stored in postgreSQL
- Companies: are stored in postgreSQL
- OFriends: relationship between two users. Are stored in OrientDB
- OWorksat: relationship between a user and a company. Are stored in OrientDB

Also if a relationship is created, either an OUser or OCompany instance vertex are created in OrientDB with only the ID's from postgreSQL, to allow the creation of the relationship (edges). This is a possible way to "Join" postgreSQL (e.g. structure) and orientdb (graph querys) strengths.

You can play with the Orientdb models and delete them easily by console. In your terminal, access to the orientdb path:

	sudo /opt/orientdb/bin/console.sh

Switch to your database:

	connect remote:localhost/databases/<your_database_name> root orientdb

You can do changes in your orientdb data and finally, you can delete your orientdb objects:

	delete edge ofriends;
	delete edge oworksat;
	drop class Ofriends;
	drop class Oworksat;
	delete vertex from OUsers;
	delete vertex from OCompany;
	drop class OUsers;
	drop class OCompany;

And when you run django server, it will generate all the models again, similar to "python manage.py migrate" command.

## Swagger Documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool for API documentation. "Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption."

## Endpoints Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods (GET, POST, PUT, DELETE), making all posssible CRUD (create, retrieve, update, delete) operations.

You can see the endpoints structure in the Swagger UI documentation:
	
	http://127.0.0.1:8000/swagger/

Basically the structure is as below for all the instances (User, Company, OFriends, OWorksat)

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`api/<instance>` | GET | READ | Get all the '<instance>' records
`api/<instance>/:id` | GET | READ | Get a single <instance> (at the moment, only for User and Company instances) reacord
`api/<instance>`| POST | CREATE | Create a new <instance> record
`api/<instance>/:id` | PUT | UPDATE | Update a <instance> (at the moment, only for User and Company instances) record
`api/<instance>/:id` | DELETE | DELETE | Delete a <instance> (for relationships, only works in swagger UI DELETE method) record

## Testing the API

Exists many ways to test the API. 

By your terminal:
- Using [curl](https://curl.haxx.se/)
- Using [httpie](https://github.com/jakubroztocil/httpie#installation), which is a user friendly http client that's written in Python, and it's in the requirements.txt file.

By the DRF UI or Swagger UI:
- In the basic root view for DefaultRouter of DRF: http://127.0.0.1:8000/
- In the swagger UI: http://127.0.0.1:8000/swagger/

Also you can use postman.

## Getting Token Authentication for your Superuser

With the Django's development server up, only authenticated users can use the User API service, for that reason if you try in your terminal this (even without any data):

	http  http://127.0.0.1:8000/api/user/1/

You get:
```
{
    "detail": "Authentication credentials were not provided."
}
```
So, you need to generate your DRF token authentication. First, create your superuser by django createsuperuser command:

	python manage.py createsuperuser

And fill up an **email** and a **password** to generate a superuser in postgreSQL. You could generate another user if you want to make "OFriends" relationship.

Then, generate you need to generate your token. You have 2 ways:

1. By rest_auth UI. Go to:

	http://127.0.0.1:8000/rest-auth/login/

And fill up with your **email** (username and email) and **password** superuser, send the POST request and that's it, now you have your token!

2. By rest_framework.authtoken. In your terminal write:

	python manage.py drf_create_token <your_superuser_email>

And you get your token. Now you can access to the User Api. Copy your token and make the request:

	http http://127.0.0.1:8000/api/user/1/ 'Authorization: Token <your_token>'

Also, in the DRF User API, you could access in the form:

	http://127.0.0.1:8000/api/user/1/?auth_token=<your_token>

## Generating Companies

a) By sending a POST request in the Company API:

	http://127.0.0.1:8000/api/company

b) Or by sending a POST Company request in the swagger UI:

	http://127.0.0.1:8000/swagger/
	
Then make a GET request to get Company ID.

Your Company will be generated in PostgreSQL database. 

## Generating Orientdb relationships

Do you want to generate "friends" or "works at" relationship?. According your choice, make a POST request in:

- http://127.0.0.1:8000/api/ofriends (OFriends relationship) with the two Users ID generated before
- http://127.0.0.1:8000/api/oworksat (OWorksat relationship) with the User and Company ID generated before

Both objects will be generated in orientdb database. Finally you could make a GET request in:

- http://127.0.0.1:8000/api/ofriends (OFriends relationship)
- http://127.0.0.1:8000/api/oworksat (OFriends relationship)

And you could see your recently relationship generated. Also you can send a GET request (OFriends or OFriend) in swagger UI to see the instance created.

If you want to delete and edge (OFriends,OWorksat), you can do it by accessing to Orientdb Studio (or by orientdb console), i.e:

	http://localhost:2480/studio/index.html#/


Execute your query, similar as below:

	select * from `<your_edge>`

And take note of your @rid (see Troubleshooting section). Finally, send a delete request in swagger UI, passing the @rid:

	http://127.0.0.1:8000/swagger/

You could find more pyorient OGM documentation in the [official repository](https://github.com/orientechnologies/pyorient/blob/master/OGM.md) or in the [home page](https://orientdb.com/docs/2.2.x/PyOrient-OGM.html).

## Troubleshooting

1. About pyorient:

Pyorient stable version is "1.5.5", but it has a current [issue](https://github.com/orientechnologies/pyorient/issues/27#issuecomment-410819253), so inside of your virtualenv:

	env/lib/python3.6/site-packages/pyorient

Open **orient.py** and comment this block of code (from 100 to 103 line):
```
if self.protocol > SUPPORTED_PROTOCOL:
        raise PyOrientWrongProtocolVersionException(
            "Protocol version " + str(self.protocol) +
            " is not supported yet by this client.", []) 
```

2. About delete/destroy method using pyorient OGM:

I created an [issue](https://github.com/mogui/pyorient/issues/284) with the intention to search for a better way to delete and edge instead of using simple raw query, so in the api.py, i had to use a pyorient client to do that:
```
def destroy(self, request, *args, **kwargs):
	client = orientdbConnection()

	client.command("delete edge <my_edge> where @rid = '" + kwargs['pk'] + "'")
	
	return Response(status=status.HTTP_204_NO_CONTENT)
```

Obviously this is not what it should be, but it's a solution. Even with this, I couldn't find a susccessfully way to pass in the DRF querystring, an orientdb @rid to delete an edge, I only achieved this in the swagger UI delete request (if you find how to do that, please tell me)


## Contributions
------------------------

All work to improve performance is good

Enjoy it!
