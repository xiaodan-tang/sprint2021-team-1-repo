from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import random

from .models import Restaurant, FAQ

from .forms import (
    # QuestionnaireForm,
    SearchFilterForm,
)


from user.forms import (
    UserQuestionaireForm,
    Report_Review_Form,
    Report_Comment_Form,
    RestaurantQuestionForm,
    RestaurantAnswerForm,
)
from user.models import Review, Comment, RestaurantQuestion, RestaurantAnswer


from .utils import (
    query_yelp,
    query_inspection_record,
    get_latest_inspection_record,
    get_restaurant_list,
    get_reviews_stats,
    get_latest_feedback,
    get_average_safety_rating,
    get_total_restaurant_number,
    check_restaurant_saved,
    get_csv_from_github,
    questionnaire_statistics,
    get_filtered_restaurants,
    restaurants_to_dict,
    check_user_location,
)

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


def get_restaurant_profile(request, restaurant_id):

    if request.method == "POST" and "content" in request.POST:
        form = UserQuestionaireForm(request.POST, restaurant_id)
        # if form.is_valid():
        form.save()
        messages.success(request, "success")
        url = reverse("restaurant:profile", args=[restaurant_id])
        return HttpResponseRedirect(url)

    try:
        csv_file = get_csv_from_github()
        result = {}
        for idx, row in csv_file.iterrows():
            if idx == 0:
                continue
            result[row["modzcta"]] = [
                row["modzcta_name"],
                row["percentpositivity_7day"],
                row["people_tested"],
                row["people_positive"],
                row["median_daily_test_rate"],
                row["adequately_tested"],
            ]

        restaurant = Restaurant.objects.get(pk=restaurant_id)
        response_yelp = query_yelp(restaurant.business_id)
        latest_inspection = get_latest_inspection_record(
            restaurant.restaurant_name, restaurant.business_address, restaurant.postcode
        )
        feedback = get_latest_feedback(restaurant.business_id)
        average_safety_rating = get_average_safety_rating(restaurant.business_id)

        statistics_dict = questionnaire_statistics(restaurant.business_id)
        internal_reviews = list(
            Review.objects.filter(restaurant=Restaurant(pk=restaurant.pk))
            .select_related("user")
            .order_by("-time")
            .all()[:50]
            .values(
                "user",
                "user__username",
                "user__user_profile__photo",
                "id",
                "rating",
                "rating_safety",
                "rating_door",
                "rating_table",
                "rating_bathroom",
                "rating_path",
                "time",
                "content",
            )
        )
        for idx in range(len(internal_reviews)):
            comments = Comment.objects.filter(review_id=internal_reviews[idx]["id"])
            # get photo afterwards
            comments = [
                {
                    "profile": el.user.user_profile.photo,
                    "text": el.text,
                    "author": el.user.id,
                    "commentId": el.id,
                }
                for el in comments
            ]
            internal_reviews[idx]["comments"] = comments
        reviews_count, ratings_avg, ratings_distribution = get_reviews_stats(
            internal_reviews
        )

        # Get restaurant Q&As
        # limit 3 recent questions, and limit 2 recent answers for each question
        restaurant_question_list = list(
            RestaurantQuestion.objects.filter(restaurant=restaurant)
            .order_by("-time")
            .values(
                "id",
                "user",
                "user__username",
                "question",
                "time",
            )[:3]
        )
        total_question_count = RestaurantQuestion.objects.filter(
            restaurant=restaurant
        ).count()
        for idx in range(len(restaurant_question_list)):
            answers = list(
                RestaurantAnswer.objects.filter(
                    question_id=restaurant_question_list[idx]["id"]
                )
                .order_by("-time")
                .values(
                    "id",
                    "user",
                    "user__username",
                    "text",
                    "time",
                )[:2]
            )
            total_answers_count = RestaurantAnswer.objects.filter(
                question_id=restaurant_question_list[idx]["id"]
            ).count()
            restaurant_question_list[idx]["answers"] = answers
            restaurant_question_list[idx]["total_answers_count"] = total_answers_count

        # Retrieval of similar restaurants to get recommendations
        recommended_restaurants = []

        categories = [
            category["alias"] for category in response_yelp["info"]["categories"]
        ]

        ratings = [restaurant.yelp_detail.rating]

        neighborhood = [restaurant.yelp_detail.neighborhood]

        compliant_status = [restaurant.compliant_status]

        # Make a query to retrieve the restaurants with these specific attributes
        similar_restaurants = get_filtered_restaurants(
            limit=5,
            category=categories,
            neighborhood=neighborhood,
            compliant=compliant_status,
        )

        recommended_restaurants = restaurants_to_dict(similar_restaurants)

        if request.user.is_authenticated:
            user = request.user
            parameter_dict = {
                "google_key": settings.GOOGLE_MAP_KEY,
                "google_map_id": settings.GOOGLE_MAP_ID,
                "data": json.dumps(result, cls=DjangoJSONEncoder),
                "yelp_info": response_yelp,
                "lasted_inspection": latest_inspection,
                "restaurant_id": restaurant_id,
                "latest_feedback": feedback,
                "average_safety_rating": average_safety_rating,
                "saved_restaurants": len(
                    user.favorite_restaurants.all().filter(id=restaurant_id)
                )
                > 0,
                # Internal reviews
                "internal_reviews": json.dumps(internal_reviews, cls=DjangoJSONEncoder),
                "reviews_count": reviews_count,
                "ratings_avg": ratings_avg,
                "distribution": ratings_distribution,
                "statistics_dict": statistics_dict,
                "user_id": request.user.id,
                # Recommended Restuarants
                "recommended_restaurants": recommended_restaurants,
                # Restaurant Q&As
                "restaurant_question_list": restaurant_question_list,
                "total_question_count": total_question_count,
            }
        else:
            parameter_dict = {
                "google_key": settings.GOOGLE_MAP_KEY,
                "google_map_id": settings.GOOGLE_MAP_ID,
                "data": json.dumps(result, cls=DjangoJSONEncoder),
                "yelp_info": response_yelp,
                "lasted_inspection": latest_inspection,
                "restaurant_id": restaurant_id,
                "latest_feedback": feedback,
                "average_safety_rating": average_safety_rating,
                "statistics_dict": statistics_dict,
                # Internal reviews
                "internal_reviews": json.dumps(internal_reviews, cls=DjangoJSONEncoder),
                "reviews_count": reviews_count,
                "ratings_avg": ratings_avg,
                "distribution": ratings_distribution,
                # Recommended Restuarants
                "recommended_restaurants": recommended_restaurants,
                # Restaurant Q&As
                "restaurant_question_list": restaurant_question_list,
                "total_question_count": total_question_count,
            }

        return render(request, "restaurant_detail.html", parameter_dict)
    except Restaurant.DoesNotExist:
        logger.warning("Restaurant ID could not be found: {}".format(restaurant_id))
        return HttpResponseNotFound(
            "Restaurant ID {} does not exist".format(restaurant_id)
        )


def edit_review(request, restaurant_id, comment_id, action):
    if action == "delete":
        Review.objects.filter(id=comment_id).delete()
    if action == "put":
        review = Review.objects.get(id=comment_id)
        review.rating = request.POST.get("rating")
        review.content = request.POST.get("content")
        review.save()
        messages.success(request, "success")
    return HttpResponseRedirect(reverse("restaurant:profile", args=[restaurant_id]))


def edit_comment(request, restaurant_id, review_id):
    review = Review.objects.get(pk=review_id)
    comment = Comment(user=request.user, review=review)
    comment.text = request.GET.get("text")
    comment.time = datetime.now()
    comment.save()
    return HttpResponseRedirect(reverse("restaurant:profile", args=[restaurant_id]))


def delete_comment(request, restaurant_id, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    return HttpResponseRedirect(reverse("restaurant:profile", args=[restaurant_id]))


def get_inspection_info(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)

        inspection_data_list = query_inspection_record(
            restaurant.restaurant_name, restaurant.business_address, restaurant.postcode
        )

        parameter_dict = {
            "inspection_list": inspection_data_list,
            "restaurant_id": restaurant_id,
        }

        return render(request, "inspection_records.html", parameter_dict)
    except Restaurant.DoesNotExist:
        logger.warning("Restaurant ID could not be found: {}".format(restaurant_id))
        return HttpResponseNotFound(
            "Restaurant ID {} does not exist".format(restaurant_id)
        )


def get_restaurants_list(request, page):
    if request.method == "POST":
        form = SearchFilterForm(request.POST)
        if form.is_valid():
            user_location, user_geocode = check_user_location(
                request.user,
                form.cleaned_data.get("form_location"),
                form.cleaned_data.get("form_geocode"),
            )
            restaurant_list = get_restaurant_list(
                page,
                6,
                form.cleaned_data.get("keyword"),
                form.cleaned_data.get("neighbourhood"),
                form.cleaned_data.get("category"),
                form.get_price_filter(),
                form.get_rating_filter(),
                form.get_compliant_filter(),
                form.cleaned_data.get("form_sort"),
                form.cleaned_data.get("fav"),
                request.user,
                user_geocode,
            )

            if request.user.is_authenticated:
                for restaurant in restaurant_list:
                    restaurant["saved_by_user"] = check_restaurant_saved(
                        request.user, restaurant["id"]
                    )

            restaurant_number = get_total_restaurant_number(
                form.cleaned_data.get("keyword"),
                form.cleaned_data.get("neighbourhood"),
                form.cleaned_data.get("category"),
                form.get_price_filter(),
                form.get_rating_filter(),
                form.get_compliant_filter(),
                form.cleaned_data.get("form_sort"),
                form.cleaned_data.get("fav"),
                request.user,
                user_geocode,
            )
            parameter_dict = {
                "restaurant_number": restaurant_number,
                "restaurant_list": json.dumps(restaurant_list, cls=DjangoJSONEncoder),
                "page": page,
                "google_key": settings.GOOGLE_MAP_KEY_PLACES,
                "user_location": user_location,
                "user_geocode": user_geocode,
            }
            return JsonResponse(parameter_dict)
        else:
            logger.error(form.errors)
    return HttpResponse("cnm")


def get_landing_page(request, page=1):
    return render(request, "browse.html")


@login_required
def save_favorite_restaurant(request, business_id):
    if request.method == "POST":
        user = request.user
        user.favorite_restaurants.add(Restaurant.objects.get(business_id=business_id))
    return HttpResponse("Saved")


@login_required
def delete_favorite_restaurant(request, business_id):
    if request.method == "POST":
        user = request.user
        user.favorite_restaurants.remove(
            Restaurant.objects.get(business_id=business_id)
        )
        return HttpResponse("Deleted")


@csrf_exempt
def chatbot_keyword(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # If user chose to be recommended by preference
            # category list is the preference list.
            if request.user and data["is_preference"]:
                data["category"] = [
                    category.category for category in request.user.preferences.all()
                ]

            restaurants = get_filtered_restaurants(
                limit=Restaurant.objects.all().count(),
                category=data["category"],
                neighborhood=data["location"],
                rating=[3.0, 3.5, 4.0, 4.5, 5.0],
                compliant=["COVIDCompliant"],
            )

            # If number > 3, we pick 3 random restaurants in that list to recommend to user.
            total_number = restaurants.count()
            if total_number > 3:
                idx = random.sample(range(0, total_number), 3)
                restaurants = [restaurants[i] for i in idx]

            response = {"restaurants": restaurants_to_dict(restaurants)}
            return JsonResponse(response)
        except AttributeError as e:
            return HttpResponseBadRequest(e)


def get_faqs_list(request):
    faqs_list = FAQ.objects.all()
    context = {
        "faqs_list": faqs_list,
    }
    return render(request=request, template_name="faqs.html", context=context)


# Report Reviews & Comments
def report_review(request, restaurant_id, review_id):
    if request.method == "POST":
        user = request.user
        form = Report_Review_Form(request.POST, review_id, user)
        form.save()
        messages.success(request, "success")
        url = reverse("restaurant:profile", args=[restaurant_id])
        return HttpResponseRedirect(url)


def report_comment(request, restaurant_id, comment_id):
    if request.method == "POST":
        user = request.user
        form = Report_Comment_Form(request.POST, comment_id, user)
        form.save()
        messages.success(request, "success")
        url = reverse("restaurant:profile", args=[restaurant_id])
        return HttpResponseRedirect(url)


# Ask the community
def get_ask_community_page(request, restaurant_id):
    user = request.user
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    if request.method == "POST":
        if user.is_authenticated:
            form = RestaurantQuestionForm(user, restaurant, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully posted your question!")
                url = reverse("restaurant:ask_community", args=[restaurant_id])
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Failed to post your question!")
                url = reverse("restaurant:ask_community", args=[restaurant_id])
                return HttpResponseRedirect(url)
        else:
            messages.info(request, "Please login first!")
            url = reverse("user:login")
            return HttpResponseRedirect(url)
    else:
        # Get full question list and limit 2 answers per question
        question_list = list(
            RestaurantQuestion.objects.filter(restaurant=restaurant)
            .order_by("-time")
            .values(
                "id",
                "user",
                "user__username",
                "question",
                "time",
            )
        )
        for idx in range(len(question_list)):
            answers = list(
                RestaurantAnswer.objects.filter(question_id=question_list[idx]["id"])
                .order_by("-time")
                .values(
                    "id",
                    "user",
                    "user__username",
                    "text",
                    "time",
                )[:2]
            )
            question_list[idx]["answers"] = answers
            question_list[idx]["total_answers_count"] = RestaurantAnswer.objects.filter(
                question_id=question_list[idx]["id"]
            ).count()
        context = {
            "restaurant": restaurant,
            "question_list": question_list,
        }
        return render(
            request=request, template_name="test_ask_community.html", context=context
        )


def answer_community_question(request, restaurant_id, question_id):
    user = request.user
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    question = RestaurantQuestion.objects.get(pk=question_id)

    if request.method == "POST":
        if user.is_authenticated:
            form = RestaurantAnswerForm(user, question, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully posted your answer!")
                url = reverse(
                    "restaurant:answer_community", args=[restaurant_id, question_id]
                )
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Failed to post your answer!")
                url = reverse(
                    "restaurant:answer_community", args=[restaurant_id, question_id]
                )
                return HttpResponseRedirect(url)
        else:
            messages.info(request, "Please login first!")
            url = reverse("user:login")
            return HttpResponseRedirect(url)
    else:
        # Get full answer list
        answer_list = RestaurantAnswer.objects.filter(question=question)
        context = {
            "restaurant": restaurant,
            "question": question,
            "answer_list": answer_list,
        }
        return render(
            request=request, template_name="test_answer_community.html", context=context
        )
