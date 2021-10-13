from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import *
from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.contrib.auth.models import User

class TokenPairSerializer(TokenObtainPairSerializer):
	def validate(self,attrs):
		data = super(TokenPairSerializer,self).validate(attrs)
		data['is_admin'] = self.user.is_superuser
		data['groups']  = [x.name for x in self.user.groups.all()]
		data['username'] = self.user.username
		data['firs_name'] = self.user.first_name
		data['last_name'] = self.user.last_name

		return data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		read_only_fields = "is_active", "is_staff",
		exclude = "last_login","is_staff","date_joined","user_permissions",

		extra_kwargs = {
			'username': {
				'validators': [UnicodeUsernameValidator()],
			}
		}

class RegisterSerializer(serializers.Serializer):
	email = serializers.CharField(required=True)
	password = serializers.CharField(required=True)


class AccountSerializer(serializers.ModelSerializer):
	class Meta:	
		model = Account
		fields = "__all__"
	
class DepotSerializer(serializers.ModelSerializer):
	class Meta:	
		model = Depot
		fields = "__all__"
	
class RetraitSerializer(serializers.ModelSerializer):
	class Meta:	
		model = Retrait
		fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:	
		model = Transaction
		fields = "__all__"
	

