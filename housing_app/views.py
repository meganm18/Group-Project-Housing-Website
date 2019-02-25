from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import Http404

from social_django.models import UserSocialAuth

from .models import Apartment, UserProfile

def home(request):
	return render(request, 'home.html')



def apartments(request):
	apartments = Apartment.objects.all()
	return render(request, 'apartments.html', {'apartments': apartments})


def apartment_detail(request, id):
	try:
		apartment = Apartment.objects.get(id=id)
	except Apartment.DoesNotExist:
		raise Http404("Apartment not found")
	return render(request, 'apartment_detail.html', {'apartment': apartment})


def login(request):
	return render(request, 'login.html') 

@login_required()
def loggedin(request):
	return render(request, 'logged-in.html')

@login_required()
def logout(request):
	auth_logout(request)
	return render(request, 'home.html')

@login_required()
def favorites(request):
	user = request.user

	try:
		google_login = user.social_auth.get(provider='google')
	except UserSocialAuth.DoesNotExist:
		google_login = None
		print( "user is logged in using the django default authentication")
	else:
		current_user = UserProfile.objects.get(username=request.user.username)
		context = {	
			'favorites' : current_user.favorites.all()
			if request.user.is_authenticated else []
		}
	return render(request, 'favorites.html', context)

@login_required()
def loginsuccess(request):
	return render(request, 'login-success.html')