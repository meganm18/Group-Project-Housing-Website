from django.db import models

from django.contrib.auth.models import User
from social_django.models import UserSocialAuth

class Apartment(models.Model):
	name = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	location = models.CharField(max_length=150)
	price = models.IntegerField()
	size = models.IntegerField()
	bedrooms = models.IntegerField()
	furnished = models.CharField(max_length=5)
	pets = models.CharField(max_length=5)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=100)
	email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
	is_authenticated = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	favorites = models.ManyToManyField(Apartment)

#class user(models.Model):
#	username = models.CharField(max_length=100)
#	email = models.EmailField(max_length=70, null=True, blank=True, unique=True)