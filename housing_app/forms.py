
# Forms code retrieved from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

from django import forms

from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import fields, CheckboxInput

from .models import Profile, Rating


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'favorites']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score','text']