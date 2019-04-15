from django.test import TestCase, RequestFactory
from .models import Apartment, UserProfile
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


class SavedFavTestCase(TestCase):
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
            self.profile_1 = UserProfile.objects.get(user_id=2)
        except:
            UserProfile.objects.create(user=ex_user1, bio="hello")
            self.profile_1 = UserProfile.objects.get(bio="hello")
        self.profile_1.favorites.set = Apartment.objects
        self.profile_1.favorites.clear()
        self.profile_1.favorites.add(apartment_1)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.all()[0].name, "Apartment 1")
        self.profile_1.favorites.add(apartment_2)
        self.profile_1.save()
        self.assertEqual(self.profile_1.favorites.all()[1].name, "Apartment 2")
class SaveCompareTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="Apartment 1", company="company 1", location="location 1", price=1000, size=1000,
                                 bedrooms=1, furnished="yes", pets="yes")
        Apartment.objects.create(name="Apartment 2", company="company 2", location="location 2", price=2000, size=2000,
                                 bedrooms=2, furnished="no", pets="no")
        User.objects.create_user(username="example user 1")

    def test_compare(self):
        apartment_1 = Apartment.objects.get(name="Apartment 1")
        apartment_2 = Apartment.objects.get(name="Apartment 2")
        ex_user1 = User.objects.get(username="example user 1")
        try:
            self.profile_1 = UserProfile.objects.get(user_id=1)
        except:
            UserProfile.objects.create(user=ex_user1, bio="hello")
            self.profile_1 = UserProfile.objects.get(bio="hello")
        self.profile_1.compare0=apartment_1
        self.profile_1.save()
        self.assertEqual(self.profile_1.compare0.name, "Apartment 1")
        self.profile_1.compare1 = apartment_2
        self.profile_1.save()
        self.assertEqual(self.profile_1.compare1.name, "Apartment 2")

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

    def test_compare_page(self):
        request4 = self.factory.get(r'^compare/')
        request4.user = self.user1
        response4 = login(request4)
        self.assertEqual(response4.status_code, 200)

##class SortingApartmentsTestCase(TestCase):
##    def setUp(self):
##        #create apartments with unique prices and ratings
##        Apartment.objects.create(name="Apartment 1", price = 2000)
##        Apartment.objects.create(name="Apartment 2", price = 1000)
##
##    def test_rating_sort(self):
##        apartment1 = Apartment.objects.get(name="Apartment 1")
##        apartment1.ratings.set(5)
##        apartment2 = Apartment.objects.get(name="Apartment 2")
##        apartment2.ratings.set(4)
##        apartmentObjs = Apartment.objects.all()
##        apartmentObjs = apartmentObjs.filter(ratings__isnull=False).order_by('-ratings__average')
##        self.assertEqual(apartmentObjs[0].name, "Apartment 1")

##    def test_price_sort(self):
##        apartmentObjs = Apartment.objects.all()
##        apartmentObjs = apartmentObjs.order_by('-price')
##        self.assertEqual(apartmentObjs[0].name, "Apartment 2")

##class FilteringApartmentsTestCase(TestCase):
##    def setUp(self):
##        #create apartments with unique bedroom numbers
##        Apartment.objects.create(name="Apartment 1", bedrooms = 1)
##        Apartment.objects.create(name="Apartment 2", bedrooms = 2)

##    def test_bedroom_filter(self):
##        apartmentObjs = Apartment.objects.all()
##        apartmentObjs = apartmentObjs.filter(bedrooms__icontains=2)
##        self.assertEqual(apartmentObjs[0].name, "Apartment 2")