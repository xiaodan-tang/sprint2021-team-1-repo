from django.shortcuts import render
from restaurant.utils import get_compliant_restaurant_list
from restaurant.utils import (
    get_filtered_restaurants,
    restaurants_to_dict,
    get_latest_inspection_record,
)
from user.models import Review, UserActivityLog, Preferences

import logging
import heapq
from datetime import datetime
from itertools import chain

logger = logging.getLogger(__name__)

RESTAURANT_NUMBER = 18
REVIEW_LIMIT = 10


def index(request):
    restaurant_list = get_compliant_restaurant_list(
        1,
        RESTAURANT_NUMBER,
        rating_filter=[3, 3.5, 4, 4.5, 5],
        compliant_filter=["COVIDCompliant"],
    )

    recent_reviews = Review.objects.order_by("-time")[:REVIEW_LIMIT]
    restaurant_review_list = [r for r in recent_reviews]

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
            p.display_value
            for p in request.user.preferences.filter(preference_type="price")
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

    # Recommended restaurant list based on user's recent views
    suggested_restaurant_list = []
    if request.user and request.user.is_authenticated:
        suggested_restaurants = get_recent_views_recommendation(request.user)
        suggested_restaurant_list = restaurants_to_dict(suggested_restaurants)

    parameter_dict = {
        "restaurant_list": restaurant_list,
        "recommended_restaurant_list": recommended_restaurants_list,
        "restaurant_review_list": restaurant_review_list,
        # recommended restaurants based on recently viewed history:
        "suggested_restaurant_list": suggested_restaurant_list,
    }
    return render(request, "index.html", parameter_dict)


def terms(request):
    return render(request, "terms.html")


def get_recent_views_recommendation(user):
    # Provide recommended restaurants based on user's recent views
    user_activity = UserActivityLog.objects.filter(user=user)
    categories, ratings, neighborhoods, compliance, prices = ({} for i in range(5))
    category_choice = set(
        [obj.value for obj in Preferences.objects.filter(preference_type="category")]
    )

    # Count the frequency for each attribute based on user visits
    for idx in range(user_activity.count()):
        restaurant = user_activity[idx].restaurant
        visits = user_activity[idx].visits
        last_visit = user_activity[idx].last_visit
        time_diff = (datetime.now() - last_visit).days
        freq = visits / (time_diff + 1)

        # Get restaurant details of recent views
        category = restaurant.yelp_detail.category.all()
        r = restaurant.yelp_detail.rating
        n = restaurant.yelp_detail.neighborhood
        p = restaurant.yelp_detail.price

        for c in category:
            if c.parent_category in category_choice:
                categories[c.parent_category] = (
                    freq
                    if c.parent_category not in categories
                    else categories[c.parent_category] + freq
                )
        ratings[r] = freq if r not in ratings else ratings[r] + freq
        neighborhoods[n] = freq if n not in neighborhoods else neighborhoods[n] + freq
        prices[p] = freq if p not in prices else prices[p] + freq

        # Better to use get_latest_inspection_record instead of restaurant.compliant_status
        # Since compliant_status might be inaccurate (not up-to-date)
        latest_records = get_latest_inspection_record(
            business_name=restaurant.restaurant_name,
            business_address=restaurant.business_address,
            postcode=restaurant.postcode,
        )
        if latest_records:
            covid_compliant_status = latest_records["is_roadway_compliant"]
        else:
            covid_compliant_status = restaurant.compliant_status

        if covid_compliant_status == "Compliant":
            if "COVIDCompliant" not in compliance:
                compliance["COVIDCompliant"] = freq
            else:
                compliance["COVIDCompliant"] += freq
        if restaurant.mopd_compliance_status == "Compliant":
            if "MOPDCompliant" not in compliance:
                compliance["MOPDCompliant"] = freq
            else:
                compliance["MOPDCompliant"] += freq

    # Get filtered restaurant candidates
    if len(compliance) == 2:
        restaurant_list = list(
            chain(
                get_filtered_restaurants(
                    category=list(categories.keys()),
                    rating=list(ratings.keys()),
                    compliant=["COVIDCompliant"],
                    price=list(prices.keys()),
                    neighborhood=list(neighborhoods.keys()),
                ),
                get_filtered_restaurants(
                    category=list(categories.keys()),
                    rating=list(ratings.keys()),
                    compliant=["MOPDCompliant"],
                    price=list(prices.keys()),
                    neighborhood=list(neighborhoods.keys()),
                ),
            )
        )
    else:
        restaurant_list = get_filtered_restaurants(
            category=list(categories.keys()),
            rating=list(ratings.keys()),
            compliant=list(compliance.keys()),
            price=list(prices.keys()),
            neighborhood=list(neighborhoods.keys()),
        )

    # If result is less than RESTAURANT_NUMBER (18 for now)
    # Get filtered restaurants only based on categories, and append to the candidate list
    if len(restaurant_list) < RESTAURANT_NUMBER:
        restaurant_list = list(
            chain(
                restaurant_list,
                get_filtered_restaurants(
                    category=list(categories.keys()),
                ),
            )
        )

    # Calculate frequency for each restaurant candidate based on user visits
    restaurant_dict = {}
    for restaurant in restaurant_list:
        category = restaurant.yelp_detail.category.all()
        r = restaurant.yelp_detail.rating
        n = restaurant.yelp_detail.neighborhood
        p = restaurant.yelp_detail.price
        frequency = ratings.get(r, 0) + neighborhoods.get(n, 0) + prices.get(p, 0)
        for c in category:
            frequency += categories.get(c.parent_category, 0)

        # Better to use get_latest_inspection_record instead of restaurant.compliant_status
        # Since compliant_status might be inaccurate (not up-to-date)
        latest_records = get_latest_inspection_record(
            business_name=restaurant.restaurant_name,
            business_address=restaurant.business_address,
            postcode=restaurant.postcode,
        )
        if latest_records:
            covid_compliant_status = latest_records["is_roadway_compliant"]
        else:
            covid_compliant_status = restaurant.compliant_status

        if covid_compliant_status == "Compliant":
            frequency += compliance.get("COVIDCompliant", 0)
        if restaurant.mopd_compliance_status == "Compliant":
            frequency += compliance.get("MOPDCompliant", 0)
        restaurant_dict[restaurant] = frequency

    # Get top RESTAURANT_NUMBER (18 for now) frequent restaurants
    return heapq.nlargest(
        RESTAURANT_NUMBER, restaurant_dict.keys(), key=restaurant_dict.get
    )
