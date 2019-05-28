from .models import (User,Company,OFriends,OWorksAt)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer,CompanySerializer, 
	OFriendsSerializer,OWorksAtSerializer)
from rest_framework import serializers, validators
from core.settings import (graph)

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
	# Get postgres value id
	# Check if exists
	# Create Vertex's
	# Create relationship
	queryset = graph.ofriends.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OFriendsSerializer

class OWorksAtViewSet(viewsets.ModelViewSet):
	# Get postgres value id
	# Check if exists
	# Create Vertex's
	# Create relationship
	queryset = graph.oworksat.query()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = OWorksAtSerializer
