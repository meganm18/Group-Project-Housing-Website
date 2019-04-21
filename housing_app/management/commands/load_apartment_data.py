from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from housing_app.models import Apartment
from housing_app.models import Unit
from pytz import UTC



ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the apartment data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from apartment_data.csv into our Pet model"

    def handle(self, *args, **options):
        if Apartment.objects.exists():
            print('Apartment data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Loading apartment")
        for row in DictReader(open('./apartment_data.csv')):
            apartment = Apartment()
            apartment.name = row['Apartment Name']
            apartment.company = row['Company']
            apartment.location = row['Location']
            apartment.price = row['Price']
            apartment.size = row['Size']
            apartment.bedrooms = row['Bedrooms']
            apartment.furnished = row['Furnished']
            apartment.pets = row['Pets']
            apartment.description = row['Description']
            apartment.distance = row['Distance to Grounds']
            apartment.number = row['Number']
            apartment.bathrooms = row['Bathrooms']
            apartment.image = row['Image']
            apartment.save()

        for row in DictReader(open('./units_data.csv')):
            unit = Unit()
            unit.unit_name = row['Unit Name']
            unit.apartment_name = row['Apartment']
            unit.price = row['Price']
            unit.size = row['Size']
            unit.bedrooms = row['Bedrooms']
            unit.bathrooms = row['Bathrooms']
            unit.save()

