from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.http import Http404, HttpResponseRedirect
from social_django.models import UserSocialAuth
from .models import Apartment, UserProfile, Review, Unit
from .forms import UserForm, UserProfileForm, ReviewForm

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core import serializers
import json
from django.urls import reverse
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
# import json
# from django.core.serializers.json import DjangoJSONEncoder

# found how to sort here: https://stackoverflowfrom django.shortcuts import get_object_or_404.com/questions/10488158/django-how-to-sort-objects-based-on-attribute-of-a-related-model
# found info for filtering here: https://stackoverflow.com/questions/51905712/how-to-get-the-value-of-a-django-model-field-object
# found info on url vars here: https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
def home(request):
	return render(request, 'home.html')

def apartments(request):
	search_term=''
	apartments_list = Apartment.objects.all()
	priceFilter = request.GET.get('sortInput','No Sort')
	if 'sortInput' in request.GET:
		priceFilter = request.GET['sortInput']
	if "Low to High"==priceFilter:
		apartments_list = Apartment.objects.order_by('minPrice')
	elif "High to Low"==priceFilter:
		apartments_list = Apartment.objects.order_by('-maxPrice')
	if 'search' in request.GET:
		search_term= request.GET['search']
		apartments_list= apartments_list.filter(name__icontains=search_term)
	maxPriceInput = request.GET.get('max_price_input', '3500')
	if 'max_price_input' in request.GET:
		maxPriceInput = request.GET['max_price_input']
		apartments_list = apartments_list.filter(minPrice__lte=maxPriceInput)
	"""
		for apt in apartments:
			aptprice = getattr(apt, "price")
			if "-" in aptprice:
				aptprice = aptprice.split("-")[1]
			if "–" in aptprice: # this looks like a hyphen but is not. This is not duplicate code
				aptprice = aptprice.split("–")[1]
			aptprice = aptprice.replace("-","").replace(",","").replace("$","").strip()
			if int(aptprice) > int(maxPriceInput):
				aptname = getattr(apt, "name")
				apartments = apartments.filter(name__icontains=aptname)
	"""
	bedroomInput = request.GET.get('bedroomInput','No Filter')
	if 'bedroomInput' in request.GET:
		bedroomInput = request.GET['bedroomInput']
	if bedroomInput != "None" and bedroomInput != "No Filter" and bedroomInput != "No":
		apartments_list = apartments_list.filter(maxBR__gte=bedroomInput)
	ratingInput = request.GET.get('ratingInput','No Sort')
	if 'ratingInput' in request.GET:
		ratingInput = request.GET['ratingInput']
	if "High to Low"==ratingInput:
		apartments_list = apartments_list.filter(ratings__isnull=False).order_by('-ratings__average')
	elif "Low to High"==ratingInput:
		apartments_list = apartments_list.filter(ratings__isnull=False).order_by('ratings__average')
	compare0 = None
	compare1 = None
	if not request.user.is_anonymous:
		user_profile = UserProfile.objects.get(user = request.user)
		if user_profile.compare0:
			compare0 = user_profile.compare0
		if user_profile.compare1:
			compare1 = user_profile.compare1
	paginator = Paginator(apartments_list, 10) # Show 25 apartments per page
	page = request.GET.get('page')
	apartments = paginator.get_page(page)
	data = serializers.serialize("json", apartments)
	data_json = json.loads(data)
	geolocator = GoogleV3(api_key="AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk")
	apartments_urls = []
	apartments_pks = []
	apartments_locations = []
	apartments_names = []
	apartments_images = []
	lats = []
	lons = []
	apartments_prices = []
	for i in range(0, len(apartments)):
		apartments_urls.append(reverse('apartment_detail', args=[data_json[i]['pk']]))
		apartments_pks.append(data_json[i]['pk'])
		apartments_locations.append(data_json[i]['fields']['location'])
		apartments_names.append(data_json[i]['fields']['name'])
		apartments_images.append(data_json[i]['fields']['image'])
		apartments_prices.append(data_json[i]['fields']['price'])
		try:
			location = geolocator.geocode(data_json[i]['fields']['location'])
			lats.append(location.latitude)
			lons.append(location.longitude)
		except:
			lons.append(0.00)
			lats.append(0.00)
	len_apartments = len(apartments)
	# apartment_pk = data_json[14]['pk']
	# apartment_location = data_json[14]['fields']['location']
	return render(request, 'apartments.html', {'apartments': apartments, 'priceSort': priceFilter, 'maxPriceInput': maxPriceInput, 'bedroomInput': bedroomInput, 'ratingInput':ratingInput, 'compare0':compare0, 'compare1':compare1, 'apartments_pks': apartments_pks, 'apartments_locations': apartments_locations, 'lats': lats, 'lons': lons, 'len_apartments': len_apartments, 'apartments_names': apartments_names, 'apartments_images': apartments_images, 'apartments_prices': apartments_prices})

# 7
def apartment_detail(request, id):
	try:
		num_user_reviews = 0
		user = request.user
		apartment = Apartment.objects.get(id=id)

		units = Unit.objects.all()
		units = units.filter(apartment_name__icontains=apartment.name)	

		data = serializers.serialize("json", [apartment,])
		data_json = json.loads(data)
		# data_json = data_json[0]['fields']['location']
		geolocator = GoogleV3(api_key="AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk")
		lat = 0.0
		lon = 0.0

		loc = data_json[0]['fields']['location']

		location = geolocator.geocode(data_json[0]['fields']['location'])
		try: 
			lat = location.latitude
			lon = location.longitude
		except:
			lat = 0.0
			lon = 0.0
		if request.method == "POST":
			form = ReviewForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.apartment = apartment
				post.save()

				form = ReviewForm()
				return HttpResponseRedirect(request.path_info)
			return render(request, 'apartment_detail.html', {'apartment': apartment,'units':units ,'form': form, 'lat': lat, 'lon': lon,})
		else:
			form = ReviewForm()
			reviews = Review.objects.all().filter(apartment=apartment)	
			for review in reviews:
				if	review.user == user:
					num_user_reviews = num_user_reviews + 1
			return render(request, 'apartment_detail.html', {'apartment': apartment,'units':units , 'form': form, 'reviews':reviews, 'num_user_reviews': num_user_reviews, 'lat': lat, 'lon': lon})
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
	user_for_page = request.user
	user_profile = user.userprofile
	reviews0 = Review.objects.all().filter(apartment=user_profile.compare0)
	reviews1 = Review.objects.all().filter(apartment=user_profile.compare1)
	return render(request, 'compare.html', {'compare0':user_profile.compare0, 'compare1':user_profile.compare1,'reviews0':reviews0, 'reviews1':reviews1, 'user_for_page': user_for_page})

@login_required()
def compare_maps(request):
	user = request.user
	user_for_page = request.user
	user_profile = user.userprofile
	reviews0 = Review.objects.all().filter(apartment=user_profile.compare0)
	reviews1 = Review.objects.all().filter(apartment=user_profile.compare1)
	data = serializers.serialize("json", [user_profile.compare0, user_profile.compare1])
	data_json = json.loads(data)
	# data_json = data_json[0]['fields']['location']
	geolocator = GoogleV3(api_key="AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk")
	apartments_urls = []
	apartments_pks = []
	apartments_locations = []
	apartments_names = []
	apartments_images = []
	lats = []
	lons = []
	apartments_prices = []
	for i in range(0, 2):
		apartments_urls.append(reverse('apartment_detail', args=[data_json[i]['pk']]))
		apartments_pks.append(data_json[i]['pk'])
		apartments_locations.append(data_json[i]['fields']['location'])
		apartments_names.append(data_json[i]['fields']['name'])
		apartments_images.append(data_json[i]['fields']['image'])
		apartments_prices.append(data_json[i]['fields']['price'])
		try:
			location = geolocator.geocode(data_json[i]['fields']['location'])
			lats.append(location.latitude)
			lons.append(location.longitude)
		except:
			lons.append(0.00)
			lats.append(0.00)
	return render(request, 'compare_maps.html', {'compare0':user_profile.compare0, 'compare1':user_profile.compare1,'reviews0':reviews0, 'reviews1':reviews1, 'user_for_page': user_for_page, 'apartments_pks': apartments_pks, 'apartments_locations': apartments_locations, 'lats': lats, 'lons': lons, 'apartments_names': apartments_names, 'apartments_images': apartments_images, 'apartments_prices': apartments_prices})


@login_required()
def loginsuccess(request):
	return render(request, 'login-success.html')

def get_user_profile(request, username):
	try:
		user_for_page = User.objects.get(username=username)
	except:
		raise Http404
	instance = get_object_or_404(UserProfile, user=user_for_page)
	if request.method == "POST":
		form = UserProfileForm(request.POST or None, request.FILES or None, instance=instance)
		if form.is_valid():
			# post = form.save(commit=False)
			form.save()
			form = UserProfileForm()
			return HttpResponseRedirect(request.path_info)
		return render(request, 'profile.html', {'form': form,"user_for_page":user_for_page})
	else:
		form = UserProfileForm(instance=instance)		
		return render(request, 'profile.html', {'form': form,"user_for_page":user_for_page})
    # try:
    #     user_for_page = User.objects.get(username=username)
    # except:
    #     raise Http404

    # return render(request, 'profile.html', {"user_for_page":user_for_page})

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
		user_profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
		if user_form.is_valid() and user_profile_form.is_valid():
			user_form.save()
			user_profile_form.save()
			messages.success(request, _('Your profile was successfully updated!'))
			return redirect('home')
		else:
			messages.error(request, _('Please correct the error below.'))
	else:
		user_form = UserForm(instance=request.user)
		user_profile_form = ProfileForm(instance=request.user.userprofile)
	return render(request, 'account', {
		'user_form': user_form,
		'user_profile_form': user_profile_form
	})

@login_required
def save_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.favorites.add(apartment)
	user_profile.save()
	user.save()
	return redirect('apartments')

@login_required
def edit_profile_view(request):

		user = request.user
		user_profile = user.userprofile

		if request.method == "POST":
			form = ProfileForm(request.POST or None, instance=instance)
			if form.is_valid():
				# post = form.save(commit=False)
				form.save()
				form = ProfileForm()
				return HttpResponseRedirect(request.path_info)

			return render(request, 'profile.html', {'form': form})
		else:
			form = ProfileForm()		
			return render(request, 'profile.html', {'form': form})

@login_required
def save_compare0(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare0 = apartment;
	user_profile.save()
	user.save()
	return redirect('apartments')
@login_required
def save_compare1(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare1 = apartment;
	user_profile.save()
	user.save()
	return redirect('apartments')



@login_required
def delete_favorite(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	# if user_profile.favorites.objects.filter(id = apartment_id).size() > 0:
	user_profile.favorites.remove(apartment)
	# user_profile.save()
	user.save()
	return redirect('favorites')

@login_required
def delete_review(request, review_id):
	review = Review.objects.get(pk=review_id)
	apartment_id = review.apartment.id
	Review.delete(review)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def fav_save_compare0(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare0 = apartment;
	user_profile.save()
	user.save()
	return redirect('favorites')
@login_required
def fav_save_compare1(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare1 = apartment;
	user_profile.save()
	user.save()
	return redirect('favorites')
@login_required
def delete_compare0(request):
	user = request.user
	user_profile = user.userprofile
	user_profile.compare0 = None;
	user_profile.save()
	user.save()
	return redirect('compare')
@login_required
def delete_compare1(request):
	user = request.user
	user_profile = user.userprofile
	user_profile.compare1 = None;
	user_profile.save()
	user.save()
	return redirect('compare')
@login_required
def search_compare0(request):
	search_term = ''
	apartments_list = Apartment.objects.all()
	user = request.user
	user_profile = user.userprofile
	if 'search' in request.GET:
		search_term= request.GET['search']
		apartments_list= apartments_list.filter(name__icontains=search_term)
	paginator = Paginator(apartments_list, 15)  # Show 25 apartments per page
	page = request.GET.get('page')
	apartments = paginator.get_page(page)
	reviews0 = Review.objects.all().filter(apartment=user_profile.compare0)
	reviews1 = Review.objects.all().filter(apartment=user_profile.compare1)
	return render(request, 'compare_search0.html', {'apartments': apartments,'search_term': search_term, 'compare0': user_profile.compare0, 'compare1': user_profile.compare1, 'reviews0': reviews0, 'reviews1': reviews1,})


@login_required
def save_compare0_search(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare0 = apartment;
	user_profile.save()
	user.save()
	return redirect('compare')
@login_required
def search_compare1(request):
	search_term = ''
	apartments_list = Apartment.objects.all()
	user = request.user
	user_profile = user.userprofile
	if 'search' in request.GET:
		search_term= request.GET['search']
		apartments_list= apartments_list.filter(name__icontains=search_term)
	paginator = Paginator(apartments_list, 15)  # Show 25 apartments per page
	page = request.GET.get('page')
	apartments = paginator.get_page(page)
	reviews0 = Review.objects.all().filter(apartment=user_profile.compare0)
	reviews1 = Review.objects.all().filter(apartment=user_profile.compare1)
	return render(request, 'compare_search1.html', {'apartments': apartments,'search_term': search_term, 'compare0': user_profile.compare0, 'compare1': user_profile.compare1, 'reviews0': reviews0,'reviews1': reviews1})


@login_required
def save_compare1_search(request, apartment_id):
	apartment = Apartment.objects.get(pk=apartment_id)
	user = request.user
	user_profile = user.userprofile
	user_profile.compare1 = apartment;
	user_profile.save()
	user.save()
	return redirect('compare')
