from django.contrib import admin
from .models import Apartment, UserProfile

# Register your models here.

admin.site.register(Apartment)

admin.site.register(UserProfile)