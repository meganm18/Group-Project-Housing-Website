from django.db import models
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.db.models.signals import post_save
from django.dispatch import receiver



class Apartment(models.Model):
	name = models.CharField(max_length=150)
	company = models.CharField(max_length=150)
	location = models.CharField(max_length=150)
	price = models.CharField(max_length=100)
	size = models.CharField(max_length=100)
	bedrooms = models.CharField(max_length=100)
	furnished = models.CharField(max_length=5)
	pets = models.CharField(max_length=5)
	description = models.TextField(default="No description")
	distance = models.CharField(max_length=100,default="--")
	number = models.CharField(max_length=100,default="--")
	bathrooms = models.CharField(max_length=100,default="--")
	def __str__(self):
		return self.name

## We needed to change the database to fix the login problem. I was having trouble doing that and there was probably
## a more elegant solution but this seems to work.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default="static/images/blank_profile.png")
	bio = models.TextField(max_length=500, blank=True)
	favorites = models.ManyToManyField(Apartment, blank=True,related_name="favorites")
	#compare = models.ManyToManyField(Apartment, blank=True, related_name="compare")
	compare0 = models.ForeignKey(Apartment, blank = True, null=True, on_delete='SET_DEFAULT', related_name="compare0")
	compare1 = models.ForeignKey(Apartment, blank = True, null=True, on_delete='SET_DEFAULT', related_name="compare1")
	def __str__(self):
		return self.user.username


# The following receivers save data to the user profile whenever changes are made
# code retrieved from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()