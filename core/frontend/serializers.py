from .models import (User,Company,OUsers,OCompany,OFriends,OWorksAt)
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

#class UserSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ('id','name','email','is_active','is_deleted')

'''
It's not important to display this Objects
class OUsersSerializer(serializers.Serializer):
	postgresql_id = serializers.IntegerField()
	#created_date = serializers.DateField()
	#updated_date = serializers.DateField()

	def create(self, data):
		return OUsersSerializer.objects.create(**data)

class OCompanySerializer(serializers.Serializer):
	postgresql_id = serializers.IntegerField()
	#created_date = serializers.DateField()
	#updated_date = serializers.DateField()
'''

class OFriendsSerializer(serializers.Serializer):
	#aux_id = serializers.IntegerField()
	from_postgresql_ouser_id = serializers.IntegerField()
	to_postgresql_ouser_id = serializers.IntegerField()

	def create(self, data):
		return OFriends.objects.create(**data)

	def update(self, instance, data):
		#instance.aux_id = data.get("aux_id")
		instance.from_postgresql_ouser_id = data.get("from_postgresql_ouser_id")
		instance.to_postgresql_ouser_id = data.get("to_postgresql_ouser_id")
		instance.save()
		return instance

class OWorksAtSerializer(serializers.Serializer):
	#aux_id = serializers.IntegerField()
	from_postgresql_ouser_id = serializers.IntegerField()
	to_postgresql_ocompany_id = serializers.IntegerField()

	def create(self, data):
		return OWorksAt.objects.create(**data)
	
	def update(self, instance, data):
		#instance.aux_id = data.get("aux_id")
		instance.from_postgresql_ouser_id = data.get("from_postgresql_ouser_id")
		instance.to_postgresql_ocompany_id = data.get("to_postgresql_ocompany_id")
		instance.save()
		return instance