from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.http import Http404, HttpResponseRedirect
from social_django.models import UserSocialAuth
from .models import Apartment, UserProfile, Review
from .forms import UserForm, ProfileForm, ReviewForm
from django.contrib.auth.models import User
# found how to sort here: https://stackoverflow.com/questions/10488158/django-how-to-sort-objects-based-on-attribute-of-a-related-model

def home(request):
	return render(request, 'home.html')

def apartments(request):
	search_term=''
	apartments = Apartment.objects.all()
	if 'sortInput' in request.GET:
		if "Sort by Price (low to high)"==request.GET['sortInput']:
			apartments = Apartment.objects.order_by('price')
		elif "Sort by Price (high to low)"==request.GET['sortInput']:
			apartments = Apartment.objects.order_by('-price')
	if 'search' in request.GET:
		search_term= request.GET['search']
		apartments= apartments.filter(name__icontains=search_term)
	if 'max_price_input' in request.GET:
		maxPriceInput = request.GET['max_price_input']
		apartments = apartments.filter(price__lt=maxPriceInput)
	else:
		maxPriceInput = 3000;
	if 'bedroomInput' in request.GET:
		bedroomInput = request.GET['bedroomInput']
		if bedroomInput != "No Filter":
			apartments = apartments.filter(bedrooms__icontains=bedroomInput)
	else:
		bedroomInput = "No Filter"
	if 'ratingInput' in request.GET:
		ratingInput = request.GET['ratingInput']
		if "Sort by Average Rating (high to low)"==ratingInput:
			apartments = apartments.filter(ratings__isnull=False).order_by('-ratings__average')
		elif "Sort by Average Rating (low to high)"==ratingInput:
			apartments = apartments.filter(ratings__isnull=False).order_by('ratings__average') 
	else:
		ratingInput = "No Filter"	
	return render(request, 'apartments.html', {'apartments': apartments, 'search_term': search_term, 'maxPriceInput': maxPriceInput, 'bedroom_filter': bedroomInput, 'ratingInput':ratingInput})


def apartment_detail(request, id):
	try:
		apartment = Apartment.objects.get(id=id)

		if request.method == "POST":
			form = ReviewForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.apartment = apartment
				post.save()

				form = ReviewForm()
				return HttpResponseRedirect(request.path_info)
			return render(request, 'apartment_detail.html', {'apartment': apartment, 'form': form,})
		else:
			form = ReviewForm()
			reviews = Review.objects.all().filter(apartment=apartment)		
			return render(request, 'apartment_detail.html', {'apartment': apartment, 'form': form, 'reviews':reviews})
	except Apartment.DoesNotExist:
		raise Http404("Apartment not found")

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
	user_for_page = request.user
	user = request.user

	user_profile = user.userprofile

	favorites = user_profile.favorites.all()

	return render(request, 'favorites.html', {'user_for_page': user_for_page,'favorites': favorites})

## page like favorites that will list your ratings
##@login_required()
##def myReviews(request):
##	user = request.user
##	user_profile=user.userprofile
##
##	return render(request, 'ratings.html', {'ratings': ratings})

@login_required()
def compare(request):
	user = request.user
	user_profile = user.userprofile
	reviews0 = Review.objects.all().filter(apartment=user_profile.compare0)
	reviews1 = Review.objects.all().filter(apartment=user_profile.compare1)
	return render(request, 'compare.html', {'compare0':user_profile.compare0, 'compare1':user_profile.compare1,'reviews0':reviews0, 'reviews1':reviews1})

@login_required()
def loginsuccess(request):
	return render(request, 'login-success.html')

def get_user_profile(request, username):
    try:
        user_for_page = User.objects.get(username=username)
    except:
        raise Http404

    return render(request, 'profile.html', {"user_for_page":user_for_page})

def get_user_reviews(request, username):
	try:
		user_for_page = User.objects.get(username=username)
		reviews = Review.objects.all().filter(user=user_for_page)	
	except:
		raise Http404

	return render(request, 'reviews.html', {"user_for_page":user_for_page,"reviews":reviews})

# The following code saves the user profile data in combination with the receivers in models.py
# code retrieved from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@login_required
@transaction.atomic
def update_profile(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, _('Your profile was successfully updated!'))
			return redirect('home')
		else:
			messages.error(request, _('Please correct the error below.'))
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.userprofile)
	return render(request, 'account', {
		'user_form': user_form,
		'profile_form': profile_form
	})

@login_required
def save_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)

	user = request.user
	user_profile = user.userprofile

	if request.method == 'POST':
		user_profile.favorites.add(apartment)
		user_profile.save()
		user.save()
	return redirect('apartments')

@login_required
def save_compare0(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	if request.method == "POST":
		user_profile.compare0 = apartment;
		user_profile.save()
		user.save()
	return redirect('apartments')
@login_required
def save_compare1(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	if request.method == "POST":
		user_profile.compare1 = apartment;
		user_profile.save()
		user.save()
	return redirect('apartments')



@login_required
def delete_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	if request.method == 'POST':
		if user_profile.favorites.objects.filter(id = apartment_id).size() > 0:
			user_profile.favorites.delete(id = apartment_id)
			user_profile.save()
			user.save()
	return redirect('favorites')


@login_required
def fav_save_compare0(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	if request.method == "POST":
		user_profile.compare0 = apartment;
		user_profile.save()
		user.save()
	return redirect('favorites')
@login_required
def fav_save_compare1(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	if request.method == "POST":
		user_profile.compare1 = apartment;
		user_profile.save()
		user.save()
	return redirect('favorites')
