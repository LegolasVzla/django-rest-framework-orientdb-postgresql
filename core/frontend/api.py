from .models import (User,Company,OFriends,OWorksAt)
from rest_framework import status, viewsets, permissions
from .serializers import (UserSerializer,CompanySerializer, 
	OWorksAtSerializer,OFriendsSerializer)
from rest_framework import serializers, validators
from rest_framework.pagination import PageNumberPagination
from core.settings import (graph)
from core.pyorient_client import *
from pyorient.ogm.query import Query
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer
	pagination_class = StandardResultsSetPagination

	def destroy(self, request, *args, **kwargs):
		'''
		1. Check: if the ouser doesn't exist, the user isn't in a relationship
		so, the user will be removed
		'''
		if(len(graph.ousers.query(
			postgresql_id=int(kwargs['pk'])
			)) == 0):
			instance = self.get_object()
			self.perform_destroy(instance)

			return Response(status=status.HTTP_204_NO_CONTENT)

		# 2. If not, the user is in a relationship, so it won't be removed
		else:
			print ("Not possible")

			return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

	def perform_destroy(self, instance):
		instance.delete()

class CompanyViewSet(viewsets.ModelViewSet):
	queryset = Company.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CompanySerializer
	pagination_class = StandardResultsSetPagination

	def destroy(self, request, *args, **kwargs):
		'''
		1. Check: if the ocompany doesn't exist, the company isn't in a relationship
		so, the company will be removed
		'''
		if(len(graph.ousers.query(
			postgresql_id=int(kwargs['pk'])
			)) == 0):
			instance = self.get_object()
			self.perform_destroy(instance)

			return Response(status=status.HTTP_204_NO_CONTENT)

		# 2. If not, the company is in a relationship, so it won't be removed
		else:
			print ("Not possible")

			return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

	def perform_destroy(self, instance):
		instance.delete()

'''
class OUsersViewSet(viewsets.ViewSet):
	def list(self,request):
		oquery = graph.ousers.query()
		permission_classes = [
			permissions.AllowAny
		]
		serializer = OUsersSerializer(oquery, many=True)
		serializer_class = OUsersSerializer
		return Response(serializer.data)

class OCompanyViewSet(viewsets.ModelViewSet):
	queryset = graph.ocompany.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OCompanySerializer
'''

class OFriendsViewSet(viewsets.ModelViewSet):

	queryset = graph.ofriends.query()   # In fact, this is a pyorient Query! but DRF needs it
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OFriendsSerializer
	pagination_class = StandardResultsSetPagination

	'''
	def list(self,request):
		queryset = graph.ofriends.query()
		permission_classes = [
			permissions.AllowAny
		]
		serializer_class = OFriendsSerializer
		return Response(serializer_class)
	'''
	def create(self,request):

		aux_id = ''
		queryset = graph.ofriends.query()	# In fact, this is a pyorient Query! but DRF needs it
		
		# NOTE: If exist a better way to get the last record, maybe using order_by, ¡PLEASE tell me!
		'''
		for i in queryset:
			aux_id = i.aux_id
		aux_id+=1
		'''
		#import pdb;pdb.set_trace()	

		# 1. Get postgres values id
		from_postgresql_ouser = get_object_or_404(
			User,
			is_active=True,
			id=request.data['from_postgresql_ouser_id']
			)

		to_postgresql_ouser = get_object_or_404(
			User,
			is_active=True,
			id=request.data['to_postgresql_ouser_id']
			)

		# 2. Check if the OUsers vertex record doesn't exists
		if(len(graph.ousers.query(
			postgresql_id=from_postgresql_ouser.id
			)) == 0):

			# Create the record
			from_ouser = graph.ousers.create(postgresql_id=from_postgresql_ouser.id)
			#print ("From: Creating new ousers record")

		else:
			# Get the record id
			from_ouser = graph.ousers.query(postgresql_id=from_postgresql_ouser.id)
			#print ("From: Id: " + str(from_postgresql_ouser.id) + " in ousers already exists")

		# 3. Check if the OUsers vertex record doesn't exists
		if(len(graph.ousers.query(
			postgresql_id=to_postgresql_ouser.id
			)) == 0):

			# Create the record
			to_ouser = graph.ousers.create(postgresql_id=to_postgresql_ouser.id)
			#print ("To: Creating new ousers record")

		else:
			# Get the record id
			to_ouser = graph.ousers.query(postgresql_id=to_postgresql_ouser.id)
			#print ("To: Id: " + str(to_postgresql_ouser.id) + " in ousers already exists")

		# 4. Check if the relationship doesn't exists
		if(len(graph.ofriends.query(
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ouser_id=to_postgresql_ouser.id
			)) == 0):

			# Create relationship if not exist

			# Case 1: Boths objects already exists
			if(isinstance(from_ouser,Query) and isinstance(to_ouser,Query)):
				graph.ofriends.create(
					from_ouser.first(),
					to_ouser.first(),
					#aux_id=aux_id,
					from_postgresql_ouser_id=from_postgresql_ouser.id,
					to_postgresql_ouser_id=to_postgresql_ouser.id
					)

			# Case 2: Destination user already exists in orientdb, but not origin user
			elif(not isinstance(from_ouser,Query) and isinstance(to_ouser,Query)):
				graph.ofriends.create(
					from_ouser,
					to_ouser.first(),
					#aux_id=aux_id,
					from_postgresql_ouser_id=from_postgresql_ouser.id,
					to_postgresql_ouser_id=to_postgresql_ouser.id
					)

			# Case 3: Origin user already exists in orientdb, but not the user destination
			elif(isinstance(from_ouser,Query) and not isinstance(to_ouser,Query)):
				graph.ofriends.create(
					from_ouser.first(),
					to_ouser,
					#aux_id=aux_id,
					from_postgresql_ouser_id=from_postgresql_ouser.id,
					to_postgresql_ouser_id=to_postgresql_ouser.id
					)

			# Case 4: Neither the origin user nor the user destination exists in orientdb
			elif(not isinstance(from_ouser,Query) and not isinstance(to_ouser,Query)):
				graph.ofriends.create(
					from_ouser,
					to_ouser,
					#aux_id=aux_id,
					from_postgresql_ouser_id=from_postgresql_ouser.id,
					to_postgresql_ouser_id=to_postgresql_ouser.id
					)

			#print ("The relationship for OFriends doesn't exists, so it's created")

		queryset = graph.ofriends.query()
		permission_classes = [
			permissions.AllowAny
		]
		serializer = OFriendsSerializer(queryset, many=True)		
		serializer_class = OFriendsSerializer
		return Response(serializer.data)

	def destroy(self, request, *args, **kwargs):
		client = orientdbConnection()

		client.command("delete edge ofriends where @rid = '" + kwargs['pk'] + "'")

		#client.command("delete edge ofriends where aux_id = '" + kwargs['pk'] + "'")
		
		return Response(status=status.HTTP_204_NO_CONTENT)

class OWorksAtViewSet(viewsets.ModelViewSet):

	queryset = graph.oworksat.query()   # In fact, this is a pyorient Query! but DRF needs it
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OWorksAtSerializer
	pagination_class = StandardResultsSetPagination

	'''
	def list(self,request):
		queryset = graph.oworksat.query()
		permission_classes = [
			permissions.AllowAny
		]
		serializer_class = OWorksAtSerializer
		return Response(serializer_class)
	'''
	def create(self,request):

		# 1. Get postgres values id
		from_postgresql_ouser = get_object_or_404(
			User,
			is_active=True,
			id=request.data['from_postgresql_ouser_id']
			)

		to_postgresql_ocompany = get_object_or_404(
			Company,
			is_active=True,
			id=request.data['to_postgresql_ocompany_id']
			)

		# 2. Check if the OUsers vertex record doesn't exists
		if(len(graph.ousers.query(
			postgresql_id=from_postgresql_ouser.id
			)) == 0):

			# Create the record
			from_ouser = graph.ousers.create(postgresql_id=from_postgresql_ouser.id)
			#print ("From: Creating new ousers record")

		else:
			# Get the record id
			from_ouser = graph.ousers.query(postgresql_id=from_postgresql_ouser.id)
			#print ("From: Id: " + str(from_postgresql_ouser.id) + " from ousers already exists")

		# 3. Check if the OCompany vertex record doesn't exists
		if(len(graph.ocompany.query(
			postgresql_id=to_postgresql_ocompany.id
			)) == 0):

			# Create the record
			to_ocompany = graph.ocompany.create(postgresql_id=to_postgresql_ocompany.id)
			#print ("To: Creating new ocompany record")

		else:
			# Get the record id
			to_ocompany = graph.ocompany.query(postgresql_id=to_postgresql_ocompany.id)
			#print ("To: Id: " + str(to_postgresql_ocompany.id) + " from ocompany already exists")

		# 4. Check if the relationship doesn't exists
		if(len(graph.oworksat.query(
				from_postgresql_ouser_id=from_postgresql_ouser.id,
				to_postgresql_ocompany_id=to_postgresql_ocompany.id
			)) == 0):

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

			#print ("The relationship for OCompany doesn't exists, so it's created")

		queryset = graph.oworksat.query()
		permission_classes = [
			permissions.AllowAny
		]
		serializer = OWorksAtSerializer(queryset, many=True)		
		serializer_class = OFriendsSerializer
		return Response(serializer.data)

	def destroy(self, request, *args, **kwargs):
		client = orientdbConnection()

		client.command("delete edge oworksat where @rid = '" + kwargs['pk'] + "'")
		
		return Response(status=status.HTTP_204_NO_CONTENT)
