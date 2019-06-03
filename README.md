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

## Endpoints Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods (GET, POST, PUT, DELETE), making all posssible CRUD (create, retrieve, update, delete) operations.

## Execution

1. Main model contains: User, Company, Friends and WorksAt objects. Friends is a relationship between two Users and WorksAt is a relationship between a User and a Company.

So, do you want to generate "friends" or "works at" relationship?. According your choice:

- Generate a User in: http://127.0.0.1:8000/api/user (or two users if you want to make "friends" relationship) with POST method. Then make a GET request to get the User ID.
- Generate a Company in: http://127.0.0.1:8000/api/company with POST method. Then make a GET request to get Company ID.

Both objects will be generated in postgresql database. Then make a POST request in:

- http://127.0.0.1:8000/api/ofriends (Friend relationship) with the two Users ID generated before
- http://127.0.0.1:8000/api/oworksat (Worksat relationship) with the User and Company ID generated before

Both objects will be generated in orientdb database. Finally you could make a GET request in:

- http://127.0.0.1:8000/api/ofriends (Friend relationship)
- http://127.0.0.1:8000/api/oworksat (Worksat relationship)

And you could see your recently relationship generated.

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
