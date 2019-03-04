from django.db import models
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.deconstruct import deconstructible

@deconstructible
class Rating(models.Model):
	text = models.TextField(default="No Review")
	score = models.IntegerField(default=0)
	username = models.CharField(max_length =100, default= "noUser")
	apartmentID = models.IntegerField(default=0)
	def __str__(self):
		return self.text

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
	ratings = models.ForeignKey(Rating, on_delete=models.CASCADE, default=Rating())
	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default="static/images/blank_profile.png")
	bio = models.TextField(max_length=500, blank=True)
	favorites = models.ManyToManyField(Apartment)
	#avator = models.ImageField(blank=True)
	ratings = models.ForeignKey(Rating, on_delete=models.CASCADE, default=Rating)
	def __str__(self):
		return self.user.username


# The following receivers save data to the user profile whenever changes are made
# code retrieved from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
