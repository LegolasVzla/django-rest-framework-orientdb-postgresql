from .models import (User,Company,OFriends,OWorksAt)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,CompanySerializer, 
	OWorksAtSerializer,OFriendsSerializer)
from rest_framework import serializers, validators
from core.settings import (graph)
from pyorient.ogm.query import Query

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer

class CompanyViewSet(viewsets.ModelViewSet):
	queryset = Company.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CompanySerializer
'''
class OUsersViewSet(viewsets.ModelViewSet):
	queryset = graph.ousers.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OUsersSerializer

class OCompanyViewSet(viewsets.ModelViewSet):
	queryset = graph.ocompany.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OCompanySerializer
'''

class OFriendsViewSet(viewsets.ModelViewSet):

	# Missing validation if the Users exists in postgresql
	# 1. If not exists, don't do the relationship

	'''
	Missing a better structure for a generic user origin and user 
	destination request from DRF api inputs
	'''

	# Get postgres value id
	from_postgresql_ouser = User.objects.get(is_active=True,id=1)

	# Get postgres value id
	to_postgresql_ouser = User.objects.get(is_active=True,id=2)

	print ("OFriendsViewSet")

	# 2. Check if the OUsers vertex record doesn't exists
	if(len(graph.ousers.query(
		postgresql_id=from_postgresql_ouser.id
		)) == 0):

		# Create the record
		from_ouser = graph.ousers.create(postgresql_id=from_postgresql_ouser.id)
		print ("From: Creating new ousers record")

	else:

		# Get the record id
		from_ouser = graph.ousers.query(postgresql_id=from_postgresql_ouser.id)
		print ("From: Id: " + str(from_postgresql_ouser.id) + " in ousers already exists")

	# 3. Check if the OUsers vertex record doesn't exists
	if(len(graph.ousers.query(
		postgresql_id=to_postgresql_ouser.id
		)) == 0):

		# Create the record
		to_ouser = graph.ousers.create(postgresql_id=to_postgresql_ouser.id)
		print ("To: Creating new ousers record")

	else:

		# Get the record id
		to_ouser = graph.ousers.query(postgresql_id=to_postgresql_ouser.id)
		print ("To: Id: " + str(to_postgresql_ouser.id) + " in ousers already exists")

	# 4. Check if the relationship doesn't exists
	if(len(graph.ofriends.query(
			from_postgresql_ouser_id=from_postgresql_ouser.id,
			to_postgresql_ouser_id=to_postgresql_ouser.id
		)) == 0):

		# Create relationship if not exist

		# Case 1: Boths objects already exists
		if(isinstance(from_ouser,Query) and isinstance(to_ocompany,Query)):
			graph.ofriends.create(
				from_ouser.first(),
				to_ouser.first(),
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ouser_id=to_postgresql_ouser.id
				)

		# Case 2: Destination user already exists in orientdb, but not origin user
		elif(not isinstance(from_ouser,Query) and isinstance(to_ouser,Query)):
			graph.ofriends.create(
				from_ouser,
				to_ouser.first(),
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ouser_id=to_postgresql_ouser.id
				)

		# Case 3: Origin user already exists in orientdb, but not the user destination
		elif(isinstance(from_ouser,Query) and not isinstance(to_ouser,Query)):
			graph.ofriends.create(
				from_ouser.first(),
				to_ouser,
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ouser_id=to_postgresql_ouser.id
				)

		# Case 4: Neither the origin user nor the user destination exists in orientdb
		elif(not isinstance(from_ouser,Query) and not isinstance(to_ouser,Query)):
			graph.ofriends.create(
				from_ouser,
				to_ouser,
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ouser_id=to_postgresql_ouser.id
				)

		print ("The relationship for OFriends doesn't exists, so it's created")

	queryset = graph.ofriends.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OFriendsSerializer

class OWorksAtViewSet(viewsets.ModelViewSet):

	# Missing validation if the User and the Company exists in postgresql
	# 1. If not exists, don't do the relationship

	'''
	Missing a better structure for a generic user and company request from 
	DRF api inputs
	'''
	# Get postgres value id
	from_postgresql_ouser = User.objects.get(is_active=True,id=2)
	#print (from_postgresql_ouser.id)

	# Get postgres value id
	to_postgresql_ocompany = Company.objects.get(is_active=True,id=1)
	#print (to_postgresql_ocompany.id)

	print ("OWorksAtViewSet")

	# 2. Check if the OUsers vertex record doesn't exists
	if(len(graph.ousers.query(
		postgresql_id=from_postgresql_ouser.id
		)) == 0):

		# Create the record
		from_ouser = graph.ousers.create(postgresql_id=from_postgresql_ouser.id)
		print ("From: Creating new ousers record")

	else:

		# Get the record id
		from_ouser = graph.ousers.query(postgresql_id=from_postgresql_ouser.id)
		print ("From: Id: " + str(from_postgresql_ouser.id) + " from ousers already exists")

	# 3. Check if the OCompany vertex record doesn't exists
	if(len(graph.ocompany.query(
		postgresql_id=to_postgresql_ocompany.id
		)) == 0):

		# Create the record
		to_ocompany = graph.ocompany.create(postgresql_id=to_postgresql_ocompany.id)
		print ("To: Creating new ocompany record")

	else:

		# Get the record id
		to_ocompany = graph.ocompany.query(postgresql_id=to_postgresql_ocompany.id)
		print ("To: Id: " + str(to_postgresql_ocompany.id) + " from ocompany already exists")

	# 4. Check if the relationship doesn't exists
	if(len(graph.oworksat.query(
			from_postgresql_ouser_id=from_postgresql_ouser.id,
			to_postgresql_ocompany_id=to_postgresql_ocompany.id
		)) == 0):

		#import pdb;pdb.set_trace()

		# Create relationship if not exist

		# Case 1: Boths objects already exists
		if(isinstance(from_ouser,Query) and isinstance(to_ocompany,Query)):
			graph.oworksat.create(
				from_ouser.first(),
				to_ocompany.first(),
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ocompany_id=to_postgresql_ocompany.id
				)

		# Case 2: The user already exists in orientdb, but not the company
		elif(not isinstance(from_ouser,Query) and isinstance(to_ocompany,Query)):
			graph.oworksat.create(
				from_ouser,
				to_ocompany.first(),
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ocompany_id=to_postgresql_ocompany.id
				)

		# Case 3: The company already exists in orientdb, but not the user
		elif(isinstance(from_ouser,Query) and not isinstance(to_ocompany,Query)):
			graph.oworksat.create(
				from_ouser.first(),
				to_ocompany,
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ocompany_id=to_postgresql_ocompany.id
				)

		# Case 4: Neither the company nor the user exists in orient db
		elif(not isinstance(from_ouser,Query) and not isinstance(to_ocompany,Query)):
			graph.oworksat.create(
				from_ouser,
				to_ocompany,
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ocompany_id=to_postgresql_ocompany.id
				)

		print ("The relationship for OCompany doesn't exists, so it's created")


	queryset = graph.oworksat.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OWorksAtSerializer

'''
delete edge ofriends;
delete edge oworksat;
drop class Ofriends;
drop class Oworksat;
delete vertex from OUsers;
delete vertex from OCompany;
drop class OUsers;
drop class OCompany;
'''