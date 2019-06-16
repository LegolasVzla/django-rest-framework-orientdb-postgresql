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

Also if a relationship is created, either an OUser or OCompany instance vertex are created in OrientDB with only the ID's from postgreSQL, to allow the creation of the relationship (edges).

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

## Execution

1. Do you want to generate "friends" or "works at" relationship?. According your choice:

First, you need to generate an User or a Company. If you want to generate an User, you have three possible ways:

a) By django createsuperuser command:

	python manage.py createsuperuser

And fill up an **email** and a **password** to generate a super user in postgreSQL.

b) By sending a POST request in the User API (or two users if you want to make "OFriends" relationship):

	http://127.0.0.1:8000/api/user 

c) Or by sending a POST User request in the swagger UI:

	http://127.0.0.1:8000/swagger/

Then make a GET request to get the User ID.

Second, you can generate a company:

a) By sending a POST request in the Company API:

	http://127.0.0.1:8000/api/company

b) Or by sending a POST Company request in the swagger UI:

	http://127.0.0.1:8000/swagger/
	
Then make a GET request to get Company ID.

Both objects will be generated in postgreSQL database. Then make a POST request in:

- http://127.0.0.1:8000/api/ofriends (OFriend relationship) with the two Users ID generated before
- http://127.0.0.1:8000/api/oworksat (OWorksat relationship) with the User and Company ID generated before

Both objects will be generated in orientdb database. Finally you could make a GET request in:

- http://127.0.0.1:8000/api/ofriends (OFriend relationship)
- http://127.0.0.1:8000/api/oworksat (OFriend relationship)

And you could see your recently relationship generated. Also you can send a GET request (OFriend or OFriend) in swagger UI to see the instance created.

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


## Contributions
------------------------

All work to improve performance is good

Enjoy it!
