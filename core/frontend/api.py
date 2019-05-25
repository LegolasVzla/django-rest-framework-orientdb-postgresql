from .models import (User,Company,OUsers,OCompany)
from rest_framework import viewsets, permissions
from .serializers import (UserSerializer, CompanySerializer, 
	OUsersSerializer, OCompanySerializer)
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
