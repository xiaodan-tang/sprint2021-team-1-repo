from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from restaurant.utils import get_filtered_restaurants, restaurants_to_dict

from .models import (
    User_Profile,
    Review,
    Comment,
    DineSafelyUser,
    Report_Ticket_Comment,
    Report_Ticket_Review,
    Preferences,
)

from restaurant.models import Categories
import json

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect


from .utils import (
    send_reset_password_email,
    send_verification_email,
    send_feedback_email,
)

from .forms import (
    UserCreationForm,
    UserProfileCreationForm,
    ResetPasswordForm,
    UpdatePasswordForm,
    GetEmailForm,
    UserPreferenceForm,
    ContactForm,
    ProfileUpdateForm,
)

import logging

logger = logging.getLogger(__name__)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            logger.info("valid")
            if user is not None:
                login(request, user)
                return redirect("user:register")

        # Check if the user is active or not.
        for error in form.errors.as_data()["__all__"]:
            if "This account is inactive." in error:
                user = get_user_model().objects.get(username=form.data["username"])
                send_verification_email(request, user.email)
                return render(
                    request=request, template_name="sent_verification_email.html"
                )
    else:
        form = AuthenticationForm()
    return render(request, template_name="login.html", context={"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            form2 = UserProfileCreationForm(user=user, data=request.POST)
            form2.save()

            send_verification_email(request, form.cleaned_data.get("email"))
            return render(request=request, template_name="sent_verification_email.html")
    else:
        form = UserCreationForm()
    return render(
        request=request, template_name="register.html", context={"form": form}
    )


def show_report(request):
    if not request.user.is_staff:
        messages.warning(request, "You are not authorized to do so.")
        return redirect("user:profile")

    internal_reviews = list(
        Report_Ticket_Review.objects.all()
        .select_related("user")
        .select_related("review")
        .values(
            "id",
            "review_id",
            "reason",
            "time",
            "user__id",
            "user__username",
            "review__content",
            "review__image1",
            "review__image2",
            "review__image3",
        )
    )

    internal_comments = list(
        Report_Ticket_Comment.objects.all()
        .select_related("user")
        .select_related("comment")
        .values(
            "id",
            "comment_id",
            "reason",
            "time",
            "user__id",
            "user__username",
            "comment__text",
        )
    )

    return render(
        request=request,
        template_name="admin_comment.html",
        context={
            "internal_reviews": internal_reviews,
            "internal_comments": internal_comments,
        },
    )


# @login_required()
def user_facing(request, user_id):
    if not request.user.is_authenticated:
        return redirect("user:login")
    user = DineSafelyUser.objects.get(pk=user_id)
    user_profile = User_Profile.objects.get(user=user)
    favorite_restaurant_list = user.favorite_restaurants.all()
    user_pref_list = user.preferences.all()
    user_pref_list_json = []
    internal_reviews = list(
        Review.objects.filter(user=user)
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
            "restaurant__restaurant_name",
            "restaurant__yelp_detail__img_url",
            "restaurant__id",
        )
    )
    for pref in user_pref_list:
        pref_dic = model_to_dict(pref)
        user_pref_list_json.append(pref_dic)
    return render(
        request=request,
        template_name="facing_page.html",
        context={
            "favorite_restaurant_list": favorite_restaurant_list,
            "user_pref": user_pref_list,
            "user_pref_json": json.dumps(user_pref_list_json, cls=DjangoJSONEncoder),
            "user_profile": user_profile,
            "profile_pic": "" if user_profile is None else user_profile.photo,
            "internal_reviews": json.dumps(internal_reviews, cls=DjangoJSONEncoder),
            "facing_page_user_id": user.username,
        },
    )


# @login_required()
def user_reviews(request):
    if not request.user.is_authenticated:
        return redirect("user:login")
    user = request.user
    internal_reviews = list(
        Review.objects.filter(user=user)
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
            "restaurant__restaurant_name",
            "restaurant__yelp_detail__img_url",
            "restaurant__id",
        )
    )
    return render(
        request=request,
        template_name="profile_review.html",
        context={
            "internal_reviews": json.dumps(internal_reviews, cls=DjangoJSONEncoder),
            "user_id": request.user.id,
        },
    )


# @login_required()
def post_logout(request):
    logout(request)
    return redirect("user:login")


# @login_required()
def profile(request):
    if not request.user.is_authenticated:
        return redirect("user:login")

    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(user=user, data=request.POST)
        if form.is_valid():
            if "profile-pic" in request.FILES:
                profile_pic = form.save_image(request.FILES["profile-pic"])
                User_Profile.objects.update_or_create(
                    user=user, defaults={"photo": profile_pic}
                )
            form.save()
            return redirect("user:profile")
    user_profile = User_Profile.objects.get(user=user)
    favorite_restaurant_list = user.favorite_restaurants.all()
    user_pref_list = user.preferences.all()
    user_pref_list_json = []
    for pref in user_pref_list:
        pref_dic = model_to_dict(pref)
        user_pref_list_json.append(pref_dic)
    category_pref = user.preferences.filter(preference_type="category")
    neighbourhood_pref = user.preferences.filter(preference_type="neighbourhood")
    rating_pref = user.preferences.filter(preference_type="rating")
    compliance_pref = user.preferences.filter(preference_type="compliance")
    price_pref = user.preferences.filter(preference_type="price")
    categories = Preferences.objects.filter(preference_type="category")
    neighbourhoods = Preferences.objects.filter(preference_type="neighbourhood")
    user_pref = [
        category_pref,
        neighbourhood_pref,
        rating_pref,
        compliance_pref,
        price_pref,
    ]

    return render(
        request=request,
        template_name="profile.html",
        context={
            "favorite_restaurant_list": favorite_restaurant_list,
            "user_pref_json": json.dumps(user_pref_list_json, cls=DjangoJSONEncoder),
            "user_profile": user_profile,
            "profile_pic": "" if user_profile is None else user_profile.photo,
            "categories": categories,
            "neighbourhoods": neighbourhoods,
            "user_pref": user_pref,
        },
    )

#view the viewing history
def view_history(request):
    dummy_restaurants = get_filtered_restaurants(
            limit=11,
           # category='chinese',
          #  rating=ratings,
           # compliant=compliance,
          #  price=prices,
           # neighborhood=neighborhoods,
        )
    dummy_restaurants = restaurants_to_dict(dummy_restaurants)

    print( "length:", len(dummy_restaurants))
    my_dict = {'restaurants' : dummy_restaurants}
    return render(request, 'view_history.html', context= my_dict)



def reset_password_link(request, base64_id, token):
    if request.method == "POST":

        uid = force_text(urlsafe_base64_decode(base64_id))

        user = get_user_model().objects.get(pk=uid)
        if not user or not PasswordResetTokenGenerator().check_token(user, token):
            return HttpResponse("This is invalid!")
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            form.save(uid)
            return redirect("user:login")
        else:
            return HttpResponse("Invalid")
    else:
        form = ResetPasswordForm()
        return render(
            request=request, template_name="reset.html", context={"form": form}
        )


def verify_user_link(request, base64_id, token):
    uid = force_text(urlsafe_base64_decode(base64_id))
    user = get_user_model().objects.get(pk=uid)
    if not user or not PasswordResetTokenGenerator().check_token(user, token):
        return HttpResponse("This is invalid!")
    user.is_active = True
    user.save()

    return redirect("user:login")


def forget_password(request):
    if request.method == "POST":
        form = GetEmailForm(request.POST)
        if form.is_valid():
            send_reset_password_email(request, form.cleaned_data.get("email"))
            return render(request=request, template_name="sent_email.html")
        return render(
            request=request, template_name="reset_email.html", context={"form": form}
        )
    else:
        form = GetEmailForm()
        return render(
            request=request, template_name="reset_email.html", context={"form": form}
        )


def add_preference(request):
    if request.method == "POST":
        form = UserPreferenceForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return HttpResponse("Preference Saved")
        return HttpResponseBadRequest("Bad Request")


def delete_preference(request, preference_type, value):
    if request.method == "POST":
        user = request.user
        user.preferences.remove(
            Preferences.objects.filter(
                preference_type=preference_type, value=value
            ).first()
        )
        logger.info(
            "Removed preference {}: {} for {}".format(preference_type, value, user)
        )
        return HttpResponse("Preference Removed")


def update_password(request):
    if not request.user.is_authenticated:
        return redirect("user:login")

    user = request.user
    if request.method == "POST":
        form = UpdatePasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save(user)
            return redirect("user:login")

        error_list = []
        for field in form:
            for error in field.errors:
                error_list.append(error)
        context = {"status": "400", "errors": error_list}
        response = HttpResponse(json.dumps(context), content_type="application/json")
        response.status_code = 400
        return response


def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            # Sends user answers to website email
            feedback_sent = send_feedback_email(request, email, subject, message)
            if feedback_sent:
                return redirect("user:request_received")
            else:
                messages.error(request, "An error occurred, feedback was not sent!")
        else:
            messages.error(request, "Invalid or missing data in contact form!")
    form = ContactForm()
    return render(
        request=request, template_name="contact_us.html", context={"form": form}
    )


def request_received(request):
    return render(request=request, template_name="request_received.html")
