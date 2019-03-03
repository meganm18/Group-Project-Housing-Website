from django.test import TestCase, RequestFactory
from .models import Apartment, Profile
from django.contrib.auth.models import User

# Create your tests here.

class ApartmentTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="Apartment 1", company="company 1", location="location 1", price=1000, size=1000, bedrooms=1, furnished="yes", pets="yes")
        Apartment.objects.create(name="Apartment 2", company="company 2", location="location 2", price=2000, size=2000, bedrooms=2, furnished="no", pets="no")

    def test_apartments_created(self):
        apartment_1 = Apartment.objects.get(name="Apartment 1")
        apartment_2 = Apartment.objects.get(name="Apartment 2")
        self.assertEqual(apartment_1.company, 'company 1')
        self.assertEqual(apartment_2.company, 'company 2')

class SavedListTestCase(TestCase):
    # help from https://docs.djangoproject.com/en/2.1/topics/testing/advanced/
    def setUp(self):
        Apartment.objects.create(name="Apartment 1", company="company 1", location="location 1", price=1000, size=1000,
                                 bedrooms=1, furnished="yes", pets="yes")
        Apartment.objects.create(name="Apartment 2", company="company 2", location="location 2", price=2000, size=2000,
                                 bedrooms=2, furnished="no", pets="no")
        self.user1 = User.objects.create_user(username="user 1")
        self.user1.save()
        self.profile_1 = Profile.objects.create(user = self.user1, bio="hello")
        self.profile_1.save()
    def test_favorites(self):
        apartment_1 = Apartment.objects.get(name="Apartment 1")
        apartment_2 = Apartment.objects.get(name="Apartment 2")
        self.profile_1.favorites.add(apartment_1)
        self.assertEqual(self.profile_1.favorites.name, "Apartment 1")
        self.profile_1.favorites.add(apartment_2)
        self.assertEqual(self.profile_1.favorites.name, ["Apartment 1", "Apartment 2"])