from django.shortcuts import render
from restaurant.utils import get_compliant_restaurant_list
from restaurant.utils import get_filtered_restaurants, restaurants_to_dict

# from .models import Restaurant

import logging

logger = logging.getLogger(__name__)

RESTAURANT_NUMBER = 18


def index(request):
    restaurant_list = get_compliant_restaurant_list(
        1,
        RESTAURANT_NUMBER,
        rating_filter=[3, 3.5, 4, 4.5, 5],
        compliant_filter=["COVIDCompliant"],
    )

    # below is for recommendation
    recommended_restaurants_list = []
    if request.user and request.user.is_authenticated:
        categories = [
            category.value
            for category in request.user.preferences.filter(preference_type="category")
        ]
        ratings = [
            rating.value
            for rating in request.user.preferences.filter(preference_type="rating")
        ]
        neighborhoods = [
            neighbourhood.display_value
            for neighbourhood in request.user.preferences.filter(
                preference_type="neighbourhood"
            )
        ]
        compliance = [
            c.value
            for c in request.user.preferences.filter(preference_type="compliance")
        ]
        prices = [
            p.value for p in request.user.preferences.filter(preference_type="price")
        ]

        recommended_restaurants = get_filtered_restaurants(
            limit=RESTAURANT_NUMBER,
            category=categories,
            rating=ratings,
            compliant=compliance,
            price=prices,
            neighborhood=neighborhoods,
        )
        recommended_restaurants_list = restaurants_to_dict(recommended_restaurants)

    parameter_dict = {
        "restaurant_list": restaurant_list,
        "recommended_restaurant_list": recommended_restaurants_list,
    }
    return render(request, "index.html", parameter_dict)


def terms(request):
    return render(request, "terms.html")
