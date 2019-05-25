from .models import (User)
from rest_framework import serializers

#class UserSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')
