import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from user.models import Preferences


CHOICES_NEIGHBOURHOOD = [
    ("Chelsea and Clinton"),
    ("Lower East Side"),
    ("Gramercy Park and Murray Hill"),
    ("Greenwich Village and Soho"),
    ("Upper West Side"),
    ("Central Harlem"),
    ("Upper East Side"),
    ("East Harlem"),
    ("Inwood and Washington Heights"),
    ("Lower Manhattan"),
    ("Stapleton and St. George"),
    ("Tribeca"),
    ("Port Richmond"),
    ("South Shore"),
    ("Mid-Island"),
    ("High Bridge and Morrisania"),
    ("Central Bronx"),
    ("Hunts Point and Mott Haven"),
    ("Bronx Park and Fordham"),
    ("Southeast Bronx"),
    ("Northeast Bronx"),
    ("Kingsbridge and Riverdale"),
    ("Southeast Queens"),
    ("Northwest Queens"),
    ("Long Island City"),
    ("Northwest Brooklyn"),
    ("Bushwick and Williamsburg"),
    ("East New York and New Lots"),
    ("Southwest Brooklyn"),
    ("Flatbush"),
    ("Greenpoint"),
    ("Central Brooklyn"),
    ("Borough Park"),
    ("Sunset Park"),
    ("Bushwick and Williamsburg"),
    ("Southern Brooklyn"),
    ("Canarsie and Flatlands"),
    ("North Queens"),
    ("Northeast Queens"),
    ("Central Queens"),
    ("West Queens"),
    ("West Central Queens"),
    ("Southeast Queens"),
    ("Jamaica"),
    ("Southwest Queens"),
    ("Rockaways"),
]


CHOICES_CATEGORY = [
    ("newamerican"),
    ("armenian"),
    ("barbeque"),
    ("bars"),
    ("bistros"),
    ("burgers"),
    ("chinese"),
    ("danish"),
    ("diners"),
    ("ethiopian"),
    ("filipino"),
    ("french"),
    ("georgian"),
    ("german"),
    ("greek"),
    ("hotdog"),
    ("italian"),
    ("bistros"),
    ("japanese"),
    ("jewish"),
    ("kebab"),
    ("korean"),
    ("kosher"),
    ("mexican"),
    ("noodles"),
    ("pizza"),
    ("salad"),
    ("sandwiches"),
    ("seafood"),
    ("sushi"),
    ("tapassmallplates"),
    ("vegan"),
    ("vegetarian"),
    ("vietnamese"),
    ("waffles"),
    ("wraps"),
]


CHOICES_RATING = [("5"), ("4"), ("3"), ("2"), ("1")]


CHOICES_COMPLIANCE = [("COVIDCompliant"), ("MOPDCompliant")]


CHOICES_PRICE = [("price_1"), ("price_2"), ("price_3"), ("price_4")]


def add_neighbourhood():
    for neighbourhood in CHOICES_NEIGHBOURHOOD:
        p = Preferences(preference_type="neighbourhood", value=neighbourhood)
        p.save()


def add_category():
    for category in CHOICES_CATEGORY:
        p = Preferences(preference_type="category", value=category)
        p.save()


def add_rating():
    for rating in CHOICES_RATING:
        p = Preferences(preference_type="rating", value=rating)
        p.save()


def add_compliance():
    for compliance in CHOICES_COMPLIANCE:
        p = Preferences(preference_type="compliance", value=compliance)
        p.save()


def add_price():
    for price in CHOICES_PRICE:
        p = Preferences(preference_type="price", value=price)
        p.save()


if __name__ == "__main__":
    add_neighbourhood()
    add_category()
    add_rating()
    add_compliance()
    add_price()
