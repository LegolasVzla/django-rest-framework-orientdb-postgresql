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

Run the migrations (to PostgreSQL):

	python manage.py makemigrations

	python manage.py migrate

Run the server:

	python manage.py runserver

You could see the home page in:

	http://127.0.0.1:8000/

## Endpoints Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods (GET, POST, PUT, DELETE), making all posssible CRUD (create, retrieve, update, delete) operations.

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
