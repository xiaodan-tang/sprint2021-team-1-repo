import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from user.models import Preferences  # noqa: E402


CHOICES_NEIGHBOURHOOD = [
    ("Chelsea_and_Clinton", "Chelsea and Clinton"),
    ("Lower_East_Side", "Lower East Side"),
    ("Gramercy_Park_and_Murray_Hill", "Gramercy Park and Murray Hill"),
    ("Greenwich_Village_and_Soho", "Greenwich Village and Soho"),
    ("Upper_West_Side", "Upper West Side"),
    ("Central_Harlem", "Central Harlem"),
    ("Upper_East_Side", "Upper East Side"),
    ("East_Harlem", "East Harlem"),
    ("Inwood_and_Washington_Heights", "Inwood and Washington Heights"),
    ("Lower_Manhattan", "Lower Manhattan"),
    ("Stapleton_and_St_George", "Stapleton and St. George"),
    ("Tribeca", "Tribeca"),
    ("Port_Richmond", "Port Richmond"),
    ("South_Shore", "South Shore"),
    ("Mid-Island", "Mid-Island"),
    ("HighPBridge_and_Morrisania", "High Bridge and Morrisania"),
    ("Central_Bronx", "Central Bronx"),
    ("Hunts_Point_and_Mott_Haven", "Hunts Point and Mott Haven"),
    ("Bronx_Park_and_Fordham", "Bronx Park and Fordham"),
    ("Southeast_Bronx", "Southeast Bronx"),
    ("Northeast_Bronx", "Northeast Bronx"),
    ("Kingsbridge_and_Riverdale", "Kingsbridge and Riverdale"),
    ("Southeast_Queens", "Southeast Queens"),
    ("Northwest_Queens", "Northwest Queens"),
    ("Long_Island_City", "Long Island City"),
    ("Northwest_Brooklyn", "Northwest Brooklyn"),
    ("Bushwick_and_Williamsburg", "Bushwick and Williamsburg"),
    ("East_New_York_and_New_Lots", "East New York and New Lots"),
    ("Southwest_Brooklyn", "Southwest Brooklyn"),
    ("Flatbush", "Flatbush"),
    ("Greenpoint", "Greenpoint"),
    ("Central_Brooklyn", "Central Brooklyn"),
    ("Borough_Park", "Borough Park"),
    ("Sunset_Park", "Sunset Park"),
    ("Bushwick_and_Williamsburg", "Bushwick and Williamsburg"),
    ("Southern_Brooklyn", "Southern Brooklyn"),
    ("Canarsie_and_Flatlands", "Canarsie and Flatlands"),
    ("North_Queens", "North Queens"),
    ("Northeast_Queens", "Northeast Queens"),
    ("Central_Queens", "Central Queens"),
    ("West_Queens", "West Queens"),
    ("West_Central Queens", "West Central Queens"),
    ("Southeast_Queens", "Southeast Queens"),
    ("Jamaica", "Jamaica"),
    ("Southwest_Queens", "Southwest Queens"),
    ("Rockaways", "Rockaways"),
]


CHOICES_CATEGORY = [
    ("newamerican", "New American"),
    ("armenian", "Armenian"),
    ("barbeque", "Barbeque"),
    ("bars", "Bars"),
    ("bistros", "Bistros"),
    ("burgers", "Burgers"),
    ("chinese", "Chinese"),
    ("danish", "Danish"),
    ("diners", "Diners"),
    ("ethiopian", "Ethiopian"),
    ("filipino", "Filipino"),
    ("french", "French"),
    ("georgian", "Georgian"),
    ("german", "German"),
    ("greek", "Greek"),
    ("hotdog", "Hotdog"),
    ("italian", "Italian"),
    ("japanese", "Japanese"),
    ("jewish", "Jewish"),
    ("kebab", "Kebab"),
    ("korean", "Korean"),
    ("kosher", "Kosher"),
    ("mexican", "Mexican"),
    ("noodles", "Noodles"),
    ("pizza", "Pizza"),
    ("salad", "Salad"),
    ("sandwiches", "Sandwiches"),
    ("seafood", "Seafood"),
    ("sushi", "Sushi"),
    ("tapassmallplates", "Tapass Small Plates"),
    ("vegan", "Vegan"),
    ("vegetarian", "Vegetarian"),
    ("vietnamese", "Vietnamese"),
    ("waffles", "Waffles"),
    ("wraps", "Wraps"),
]


CHOICES_RATING = [
    ("5", "5 Stars"),
    ("4", "4 Stars"),
    ("3", "3 Stars"),
    ("2", "2 Stars"),
    ("1", "1 Star"),
]


CHOICES_COMPLIANCE = [
    ("COVIDCompliant", "COVID-19 Compliant"),
    ("MOPDCompliant", "MOPD Compliant"),
]


CHOICES_PRICE = [
    ("price_1", "$"),
    ("price_2", "$$"),
    ("price_3", "$$$"),
    ("price_4", "$$$$"),
]


def add_neighbourhood():
    for neighbourhood in CHOICES_NEIGHBOURHOOD:
        p = Preferences(
            preference_type="neighbourhood",
            value=neighbourhood[0],
            display_value=neighbourhood[1],
        )
        p.save()


def add_category():
    for category in CHOICES_CATEGORY:
        p = Preferences(
            preference_type="category", value=category[0], display_value=category[1]
        )
        p.save()


def add_rating():
    for rating in CHOICES_RATING:
        p = Preferences(
            preference_type="rating", value=rating[0], display_value=rating[1]
        )
        p.save()


def add_compliance():
    for compliance in CHOICES_COMPLIANCE:
        p = Preferences(
            preference_type="compliance",
            value=compliance[0],
            display_value=compliance[1],
        )
        p.save()


def add_price():
    for price in CHOICES_PRICE:
        p = Preferences(preference_type="price", value=price[0], display_value=price[1])
        p.save()


if __name__ == "__main__":
    # print("hello world")
    # add_neighbourhood()
    # add_category()
    # add_rating()
    # add_compliance()
    # add_price()
