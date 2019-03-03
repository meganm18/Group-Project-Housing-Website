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
        User.objects.create_user(username="example user 1")
    def test_favorites(self):
        apartment_1 = Apartment.objects.get(name="Apartment 1")
        apartment_2 = Apartment.objects.get(name="Apartment 2")
        ex_user1 = User.objects.get(username="example user 1")
        try:
            self.profile_1 = Profile.objects.get(user_id=1)
        except:
            Profile.objects.create(user=ex_user1, bio="hello")
            self.profile_1 = Profile.objects.get(bio="hello")
        self.profile_1.favorites.add(apartment_1)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.name.all(), "Apartment 1")
        self.profile_1.favorites.add(apartment_2)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.name.all(), ["Apartment 1", "Apartment 2"])