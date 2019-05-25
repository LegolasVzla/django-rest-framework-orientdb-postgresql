from frontend.models import (User)
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from rest_framework import serializers, validators

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = UserSerializer
