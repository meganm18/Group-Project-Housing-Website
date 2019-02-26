from django.test import TestCase
from .models import Apartment, Profile

# Create your tests here.

class ApartmentTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="Apartment 1", company="company 1", location="location 1", price=1000, size=1000, bedrooms=1, furnished="yes", pets="yes")
        Apartment.objects.create(name="Apartment 2", company="company 2", location="location 2", price=2000, size=2000, bedrooms=2, furnished="no", pets="no")

    def test_apartments_created(self):
        apartment_1 = Animal.objects.get(name="Apartment 1")
        apartment_2 = Animal.objects.get(name="Apartment 2")
        self.assertEqual(apartment_1.company, 'company 1')
        self.assertEqual(apartment_2.company, 'company 2')
