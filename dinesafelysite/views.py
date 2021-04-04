from django.shortcuts import render
from restaurant.utils import get_compliant_restaurant_list
from restaurant.utils import get_filtered_restaurants, restaurants_to_dict
from user.models import Review, UserActivityLog

import logging
import heapq

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
        suggested_restaurant_list = get_recent_views_recommendation(request.user)

    parameter_dict = {
        "restaurant_list": restaurant_list,
        "recommended_restaurant_list": recommended_restaurants_list,
        "restaurant_review_list": restaurant_review_list,
        "suggested_restaurant_list": suggested_restaurant_list,
    }
    return render(request, "index.html", parameter_dict)


def terms(request):
    return render(request, "terms.html")


def get_recent_views_recommendation(user):
    # Provide recommended restaurants based on user's recent views
    user_activity = UserActivityLog.objects.filter(user=user)
    categories, ratings, neighborhoods, compliance, prices = ({} for i in range(5))

    # Count the frequency for each attribute based on user visits
    for idx in range(user_activity.count()):
        restaurant = user_activity[idx].restaurant
        visits = user_activity[idx].visits

        # Get restaurant details of recent views
        c = restaurant.yelp_detail.category
        r = restaurant.yelp_detail.rating
        n = restaurant.yelp_detail.neighborhood
        p = restaurant.yelp_detail.price
        categories[c] = visits if c not in categories else categories[c]+visits
        ratings[r] = visits if r not in ratings else ratings[r]+visits
        neighborhoods[n] = visits if n not in neighborhoods else neighborhoods[n]+visits
        prices[p] = visits if p not in prices else prices[p]+visits

        if restaurant.compliant_status == "Compliant":
            if "COVIDCompliant" not in compliance:
                compliance["COVIDCompliant"] = visits
            else:
                compliance["COVIDCompliant"] += visits
        if restaurant.mopd_compliance_status == "Compliant":
            if "COVIDCompliant" not in compliance:
                compliance["MOPDCompliant"] = visits
            else:
                compliance["MOPDCompliant"] += visits

    # Get filtered restaurant candidates
    restaurant_list = get_filtered_restaurants(
        category=list(categories.keys()),
        rating=list(ratings.keys()),
        compliant=list(compliance.keys()),
        price=list(prices.keys()),
        neighborhood=list(neighborhoods.keys()),
    )

    # Get top RESTAURANT_NUMBER (18 for now) frequent restaurants
    if len(restaurant_list) <= RESTAURANT_NUMBER:
        return restaurant_list
    else:
        # Calculate frequency for each restaurant candidate based on user visits
        restaurant_dict = {}
        for restaurant in restaurant_list:
            c = restaurant.yelp_detail.category
            r = restaurant.yelp_detail.rating
            n = restaurant.yelp_detail.neighborhood
            p = restaurant.yelp_detail.price
            frequency = categories.get(c, 0) + ratings.get(r, 0) + neighborhoods.get(n, 0) + prices.get(p, 0)
            if restaurant.compliant_status == "Compliant":
                frequency += categories.get("COVIDCompliant", 0)
            if restaurant.mopd_compliance_status == "Compliant":
                frequency += categories.get("MOPDCompliant", 0)
            restaurant_dict[restaurant] = frequency

        return heapq.nlargest(RESTAURANT_NUMBER, restaurant_dict.keys(), key=restaurant_dict.get)
