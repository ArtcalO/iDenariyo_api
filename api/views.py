from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

from rest_framework import permissions
from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
CREATE_METHODS = ['POST']

def genAccountNumber(last):
	old_acc_id = last.split('/')[1]
	acc_letter = last.split('/')[1][:1]
	acc_number = last.split('/')[1][1:]

	if(int(acc_number) == 999999):
		acc_letter = chr(ord(acc_letter)+1)
		acc_number = "1".zfill(6)

	else:
		acc_number = str(int(acc_number)+1).zfill(6)

	new_acc_id = acc_letter+""+acc_number
	return last.replace(old_acc_id, new_acc_id)


class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer

class RegisterView(APIView):
	serializer_class = RegisterSerializer
	permission_classes = AllowAny,
	
	@transaction.atomic()
	def post(self, request, format=None):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.data.get('email')
			password = serializer.data.get('password')
			email = serializer.data.get('email')
			
			user = User(
				username = username,
			)
			password = password
			user.email = email
			user.is_active = True
			user.set_password(password)

			new_account_number = ""

			try:
				last_account = Account.objects.all().reverse().last()
				new_account_number = genAccountNumber(last_account.account_number)
			except:
				new_account_number = "TKZ/A"+"1".zfill(6)+"/iDEN"
			account = Account(
				user = user,
				amount = 1000000.0,
				)
			account.account_number = new_account_number
			user.save()
			account.save()
			return Response({"status":"success"},201)
		return Response({"status":"bad request"},400)

class AccountViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Account.objects.all()
	serializer_class = AccountSerializer

class DepotViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Depot.objects.all()
	serializer_class = DepotSerializer

class RetraitViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Retrait.objects.all()
	serializer_class = RetraitSerializer

class TransactionViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer