from django.test import TestCase, RequestFactory
from .models import Apartment, Profile, Rating
from django.contrib.auth.models import User
from .views import home, apartments, apartment_detail, login


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
        self.profile_1.favorites.set = Apartment.objects
        self.profile_1.favorites.clear()
        self.profile_1.favorites.add(apartment_1)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.all()[0].name, "Apartment 1")
        self.profile_1.favorites.add(apartment_2)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.all()[1].name, "Apartment 2")

class ViewPagesTestCase(TestCase):
    #https://docs.djangoproject.com/en/2.1/topics/testing/advanced/
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="user1")
        self.user1 = User.objects.get(username="user1")
        Apartment.objects.create(name="Apartment 1", company="company 1", location="location 1", price=1000, size=1000,
                                 bedrooms=1, furnished="yes", pets="yes")
        self.apartment1 = Apartment.objects.get(name="Apartment 1")
        Apartment.objects.create(name="Apartment 2", company="company 2", location="location 2", price=2000, size=2000,
                                 bedrooms=2, furnished="yes", pets="yes")
        self.apartment2 = Apartment.objects.get(name="Apartment 2")

    def test_home(self):
        request = self.factory.get(r'^$')
        request.user = self.user1
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_apartments(self):
        request1 = self.factory.get(r'^apartments/$')
        request1.user = self.user1
        response1 = apartments(request1)
        self.assertEqual(response1.status_code, 200)

    def test_apartment_detail(self):
        request2 = self.factory.get(r'^apartments/1/')
        request2.user = self.user1
        response2 = apartment_detail(request2, self.apartment1.id)
        self.assertEqual(response2.status_code, 200)

    def test_login_page(self):
        request3 = self.factory.get(r'^login/')
        request3.user = self.user1
        response3 = login(request3)
        self.assertEqual(response3.status_code, 200)

class RatingTestCase(TestCase):
    def setUp(self):
        #create rating object
        Apartment.objects.create(name = 'Apartment 1')
        apartment_1 = Apartment.objects.get("Apartment 1")
        Rating.objects.create(text = "nice", score = "5", apartment=apartment_1)
    def testApartmetRatingCreated(self):
        #assert true that rating is accessible
        self.assertTrue(True)