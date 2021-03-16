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
    recommended_restaurants = []
    if request.user and request.user.is_authenticated:
        categories = [category.category for category in request.user.preferences.all()]
        recommended_restaurants = get_filtered_restaurants(
            limit=RESTAURANT_NUMBER,
            category=categories,
            rating=[3.0, 3.5, 4.0, 4.5, 5.0],
            compliant=["COVIDCompliant"],
        )
        recommended_restaurants_list = restaurants_to_dict(recommended_restaurants)

    parameter_dict = {
        "restaurant_list": restaurant_list,
        "recommended_restaurant_list": recommended_restaurants_list,
    }
    return render(request, "index.html", parameter_dict)


def terms(request):
    return render(request, "terms.html")
