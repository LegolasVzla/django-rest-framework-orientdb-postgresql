from django.db import models
from django.contrib.auth.models import User
from core.settings import Node,Relationship,graph
from pyorient.ogm.property import (String, Date, DateTime, Decimal, Double,
	Integer, Boolean, EmbeddedMap, EmbeddedSet,Link, UUID)

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length = 500)
	email = models.CharField(max_length = 500, blank = True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_date=models.DateTimeField(auto_now_add=True)
	updated_date=models.DateTimeField()

	def __get_company_information__(self):
		return '%s %s' % (self.name,self.email).filter(is_active=True,is_deleted=False)

	company_information = property(__get_company_information__)

class OUsers(Node):
	element_plural = 'ousers'
	id=Integer(unique=True)
	postgresql_id=Integer()
	created_date=models.DateTimeField(auto_now_add=True)
	updated_date=models.DateTimeField()

class OCompany(Node):
	element_plural = 'ocompany'
	id=Integer(unique=True)
	postgresql_id=Integer()
	created_date=models.DateTimeField(auto_now_add=True)
	updated_date=models.DateTimeField()
	

graph.create_all(Node.registry)
#graph.create_all(Relationship.registry)