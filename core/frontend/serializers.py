from .models import (User,Company,OUsers,OCompany)
from rest_framework import serializers

#class UserSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('__all__')

class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ('__all__')

class OUsersSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	postgresql_id = serializers.IntegerField()
	created_date = serializers.DateField()
	updated_date = serializers.DateField()

	def create_ousers(self, data):
		return OUsers.objects.create(**data)
	
	def update_ousers(self, instance, data):
		instance.postgresql_id = data.get("postgresql_id")
		instance.created_date = data.get("created_date")
		instance.updated_date = data.get("updated_date")
		instance.save()
		return instance

class OCompanySerializer(serializers.Serializer):
	id = serializers.IntegerField()
	postgresql_id = serializers.IntegerField()
	created_date = serializers.DateField()
	updated_date = serializers.DateField()

	def create_ocompany(self, data):
		return OCompany.objects.create(**data)
	
	def update_ocompany(self, instance, data):
		instance.postgresql_id = data.get("postgresql_id")
		instance.created_date = data.get("created_date")
		instance.updated_date = data.get("updated_date")
		instance.save()
		return instance
