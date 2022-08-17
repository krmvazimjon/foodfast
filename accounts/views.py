from django.shortcuts import render, redirect
from .models import User
from .serializers import *
from my_app.models import Product
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from rest_framework.views import APIView 
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate 

def register_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username = username, password = password)
		user.save()
		return redirect('login')

	context = {}
	return render(request, 'signup.html', context)

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user:
			login(request,user)
			return redirect('index')

	context = {}
	return render(request, 'registration/login.html', context)

def logout_user(request):
	logout(request)
	return redirect('index')

class AuthUserResgitrationsView(APIView):
	permission_classes = (AllowAny, )
	def post(self, request, *args, **kwargs):
		serializer = UserSerializers(data = request.data)
		for user in User.objects.all():
			if not user:
				break
			else:
				try:
					Token.objects.get(user_id = user.id)
				except Token.DoesNotExist:
					Token.objects.create(user = user)
			if serializer.is_valid():
				user = serializer.save()
				token = Token.objects.create(user = user)
				return Response(
					{
						"user": {
							"id": serializer.data["id"],

							"firstname": serializer.data["firstname"],

							"username": serializer.data['username'],
						},
						"status": {
							"message": "User created",
							"code": f"{status.HTTP_200_OK} OK",
						},
						"token": token.key,

					}
				)
			return Response(
				{
					"error": serializer.errors,
					"status": f"{status.HTTP_203_NON_AUTHORITATIVE_INFORMATION} NON AUTHORITATIVE INFORMATION",
					}
			)


class ProductSerializersView(ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializers

class ProductIDSerializersView(RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializers