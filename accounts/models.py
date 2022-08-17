from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	firstname = models.CharField(max_length = 200)
	username = models.CharField(max_length = 200, unique = True)
	password = models.CharField(max_length = 200)
