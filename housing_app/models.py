from django.db import models

class Apartment(models.Model):
	name = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	location = models.CharField(max_length=150)
	price = models.IntegerField()
	size = models.IntegerField()
	bedrooms = models.IntegerField()
	furnished = models.CharField(max_length=5)
	pets = models.CharField(max_length=5)
	description = models.TextField(default="No description")

