from django.db import models
from django.contrib.auth.models import User
from core.settings import Node,Relationship,graph
from pyorient.ogm.property import (String, Date, DateTime, Decimal, Double,
	Integer, Boolean, EmbeddedMap, EmbeddedSet,Link, UUID)
#from pyorient.ogm.what import sysdate
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length = 500)
	email = models.CharField(max_length = 500, blank = True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_date=models.DateTimeField(auto_now_add=True)
	updated_date=models.DateTimeField(auto_now=True)

	def __get_company_information__(self):
		return '%s %s' % (self.name,self.email).filter(is_active=True,is_deleted=False)

	company_information = property(__get_company_information__)

class OUsers(Node):
	element_plural = 'ousers'
	postgresql_id=Integer(nullable=False,unique=True)
	#created_date=DateTime(nullable=False,default=sysdate())
	#updated_date=DateTime(nullable=False,default=sysdate())

class OCompany(Node):
	element_plural = 'ocompany'
	postgresql_id=Integer(nullable=False,unique=True)
	#created_date=DateTime(nullable=False,default=sysdate())
	#updated_date=DateTime(nullable=False,default=sysdate())
	
class OFriends(Relationship):
	label = 'ofriends'
	from_postgresql_ouser_id=Integer(nullable=False,unique=True)
	to_postgresql_ouser_id=Integer(nullable=False,unique=True)

class OWorksAt(Relationship):
	label = 'oworksat'
	from_postgresql_ouser_id=Integer(nullable=False,unique=True)
	to_postgresql_ocompany_id=Integer(nullable=False,unique=True)

graph.create_all(Node.registry)
graph.create_all(Relationship.registry)