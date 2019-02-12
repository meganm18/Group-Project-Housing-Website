from django.shortcuts import render
from django.http import HttpResponse

from django.http import Http404

from .models import Apartment

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
