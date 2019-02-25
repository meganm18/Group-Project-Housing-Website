from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect

from django.http import Http404

from social_django.models import UserSocialAuth

from .models import Apartment, Profile

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

	user_profile = user.profile

	favorites = user_profile.favorites.all()

	# context = {	
	# 	'favorites' : current_user.favorites.all()
	# 	if request.user.is_authenticated else []
	# }
	return render(request, 'favorites.html', {'favorites': favorites})

@login_required()
def loginsuccess(request):
	return render(request, 'login-success.html')



@login_required()
def account(request):
	# user = request.user

	# try:
	# 	google_login = user.social_auth.get(provider='google')
	# except UserSocialAuth.DoesNotExist:
	# 	google_login = None
	# 	print( "user is logged in using the django default authentication")
	# else:
	# 	current_user = UserProfile.objects.get(username=request.user.username)
	# 	context = {	
	# 		'favorites' : current_user.favorites.all()
	# 		if request.user.is_authenticated else []
	# 	}
	return render(request, 'account.html')


@login_required
@transaction.atomic
def update_profile(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, _('Your profile was successfully updated!'))
			return redirect('home')
		else:
			messages.error(request, _('Please correct the error below.'))
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(request, 'account', {
		'user_form': user_form,
		'profile_form': profile_form
	})

@login_required
def save_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)

	user = request.user
	user_profile = user.profile

	if request.method == 'POST':
		user_profile.favorites.add(apartment)
		user_profile.save()
		user.save()

	return redirect('apartments')


@login_required
def delete_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)

	user = request.user
	user_profile = user.profile

	if request.method == 'POST':
		user_profile.favorites.remove(apartment)
		user_profile.save()
		user.save()

	return redirect('favorites')