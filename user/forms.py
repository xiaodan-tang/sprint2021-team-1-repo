from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
import logging
import os.path
import boto3
import random
import string

from .models import User_Profile, Preferences

logger = logging.getLogger(__name__)


class UserQuestionaireForm(forms.Form):
    def __init__(self, data, restaurant_id):
        self.restaurant_id = restaurant_id
        self.user_id = data["user_id"]
        self.rating = data["rating"]
        self.rating_safety = data["rating_safety"]
        self.rating_entry = data["rating_entry"]
        self.rating_door = data["rating_door"]
        self.rating_table = data["rating_table"]
        self.rating_bathroom = data["rating_bathroom"]
        self.rating_path = data["rating_path"]
        # self.restaurant_business_id = data.restaurant_business_id # not sure if needed
        self.content = data["content"]

    def save(self):
        user = get_user_model().objects.get(pk=self.user_id)
        ret = user.reviews.create(
            rating=self.rating,
            rating_safety=self.rating_safety,
            rating_entry=self.rating_entry,
            rating_door=self.rating_door,
            rating_table=self.rating_table,
            rating_bathroom=self.rating_bathroom,
            rating_path=self.rating_path,
            content=self.content,
            restaurant_id=self.restaurant_id,
        )
        ret.save()
        return ret


class ProfileUpdateForm(forms.Form):
    STATE_CHOICES = [
        ("Alabama", "Alabama"),
        ("Alaska", "Alaska"),
        ("Arizona", "Arizona"),
        ("Arkansas", "Arkansas"),
        ("California", "California"),
        ("Colorado", "Colorado"),
        ("Connecticut", "Connecticut"),
        ("Delaware", "Delaware"),
        ("District of Columbia", "District of Columbia"),
        ("Florida", "Florida"),
        ("Georgia", "Georgia"),
        ("Hawaii", "Hawaii"),
        ("Idaho", "Idaho"),
        ("Illinois", "Illinois"),
        ("Indiana", "Indiana"),
        ("Iowa", "Iowa"),
        ("Kansas", "Kansas"),
        ("Kentucky", "Kentucky"),
        ("Louisiana", "Louisiana"),
        ("Maine", "Maine"),
        ("Montana", "Montana"),
        ("Nebraska", "Nebraska"),
        ("Nevada", "Nevada"),
        ("New Hampshire", "New Hampshire"),
        ("New Jersey", "New Jersey"),
        ("New Mexico", "New Mexico"),
        ("New York", "New York"),
        ("North Carolina", "North Carolina"),
        ("North Dakota", "North Dakota"),
        ("Ohio", "Ohio"),
        ("Oklahoma", "Oklahoma"),
        ("Oregon", "Oregon"),
        ("Maryland", "Maryland"),
        ("Massachusetts", "Massachusetts"),
        ("Michigan", "Michigan"),
        ("Minnesota", "Minnesota"),
        ("Mississippi", "Mississippi"),
        ("Missouri", "Missouri"),
        ("Pennsylvania", "Pennsylvania"),
        ("Rhode Island", "Rhode Island"),
        ("South Carolina", "South Carolina"),
        ("South Dakota", "South Dakota"),
        ("Tennessee", "Tennessee"),
        ("Texas", "Texas"),
        ("Utah", "Utah"),
        ("Vermont", "Vermont"),
        ("Virginia", "Virginia"),
        ("Washington", "Washington"),
        ("West Virginia", "West Virginia"),
        ("Wisconsin", "Wisconsin"),
        ("Wyoming", "Wyoming"),
    ]

    user_id = forms.CharField(label="user_id")
    username = forms.CharField(
        label="username", min_length=4, max_length=150, required=False
    )
    firstname = forms.CharField(
        label="firstname", min_length=1, max_length=150, required=False
    )
    lastname = forms.CharField(
        label="lastname", min_length=1, max_length=150, required=False
    )
    email = forms.EmailField(label="email", required=False)
    profile_pic = forms.CharField(label="profile_pic", required=False)
    phone = forms.CharField(label="phone", min_length=1, max_length=150, required=False)
    address1 = forms.CharField(
        label="address1", min_length=1, max_length=150, required=False
    )
    address2 = forms.CharField(
        label="address2", min_length=1, max_length=150, required=False
    )
    city = forms.CharField(label="city", min_length=1, max_length=64, required=False)
    zip_code = forms.CharField(
        label="zip_code", min_length=1, max_length=10, required=False
    )
    state = forms.ChoiceField(
        label="state", choices=STATE_CHOICES, initial=None, required=False
    )

    def __init__(self, user, data=None):
        self.user = user
        super(ProfileUpdateForm, self).__init__(data=data)

    def save_image(self, file):
        char_set = string.ascii_letters + string.digits
        file_name = (
            "".join(random.sample(char_set * 6, 10)) + os.path.splitext(file.name)[1]
        )
        boto3.client("s3").upload_fileobj(
            file, "dineline", "media/user_profile_pics/" + file_name
        )
        return "https://dineline.s3.amazonaws.com/media/user_profile_pics/" + file_name

    def save(self, commit=True):
        uid = self.cleaned_data["user_id"]
        user = get_user_model().objects.get(pk=uid)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]
        user.save()
        user_profile = User_Profile.objects.get(user=user)
        user_profile.phone = self.cleaned_data["phone"]
        user_profile.address1 = self.cleaned_data["address1"]
        user_profile.address2 = self.cleaned_data["address2"]
        user_profile.city = self.cleaned_data["city"]
        user_profile.zip_code = self.cleaned_data["zip_code"]
        user_profile.state = self.cleaned_data["state"]
        user_profile.save()
        return user


class UserProfileCreationForm(forms.Form):
    STATE_CHOICES = [
        ("Alabama", "Alabama"),
        ("Alaska", "Alaska"),
        ("Arizona", "Arizona"),
        ("Arkansas", "Arkansas"),
        ("California", "California"),
        ("Colorado", "Colorado"),
        ("Connecticut", "Connecticut"),
        ("Delaware", "Delaware"),
        ("District of Columbia", "District of Columbia"),
        ("Florida", "Florida"),
        ("Georgia", "Georgia"),
        ("Hawaii", "Hawaii"),
        ("Idaho", "Idaho"),
        ("Illinois", "Illinois"),
        ("Indiana", "Indiana"),
        ("Iowa", "Iowa"),
        ("Kansas", "Kansas"),
        ("Kentucky", "Kentucky"),
        ("Louisiana", "Louisiana"),
        ("Maine", "Maine"),
        ("Montana", "Montana"),
        ("Nebraska", "Nebraska"),
        ("Nevada", "Nevada"),
        ("New Hampshire", "New Hampshire"),
        ("New Jersey", "New Jersey"),
        ("New Mexico", "New Mexico"),
        ("New York", "New York"),
        ("North Carolina", "North Carolina"),
        ("North Dakota", "North Dakota"),
        ("Ohio", "Ohio"),
        ("Oklahoma", "Oklahoma"),
        ("Oregon", "Oregon"),
        ("Maryland", "Maryland"),
        ("Massachusetts", "Massachusetts"),
        ("Michigan", "Michigan"),
        ("Minnesota", "Minnesota"),
        ("Mississippi", "Mississippi"),
        ("Missouri", "Missouri"),
        ("Pennsylvania", "Pennsylvania"),
        ("Rhode Island", "Rhode Island"),
        ("South Carolina", "South Carolina"),
        ("South Dakota", "South Dakota"),
        ("Tennessee", "Tennessee"),
        ("Texas", "Texas"),
        ("Utah", "Utah"),
        ("Vermont", "Vermont"),
        ("Virginia", "Virginia"),
        ("Washington", "Washington"),
        ("West Virginia", "West Virginia"),
        ("Wisconsin", "Wisconsin"),
        ("Wyoming", "Wyoming"),
    ]

    address1 = forms.CharField(label="address1")
    address2 = forms.CharField(label="address2")
    city = forms.CharField(label="city")
    zip_code = forms.CharField(label="zip_code")
    state = forms.ChoiceField(label="state", choices=STATE_CHOICES)

    def __init__(self, user, data):
        self.user = user
        self.data = data
        self.user_profile = User_Profile.objects.get(user=self.user)
        # super(UserProfileCreationForm, self).__init__(data=data)

    def save(self, commit=True):
        if "phone" in self.data:
            self.user_profile.phone = self.data["phone"]
        if "address1" in self.data:
            self.user_profile.address1 = self.data["address1"]
        if "address2" in self.data:
            self.user_profile.address2 = self.data["address2"]
        if "city" in self.data:
            self.user_profile.city = self.data["city"]
        if "zip_code" in self.data:
            self.user_profile.zip_code = self.data["zip_code"]
        if "state" in self.data:
            self.user_profile.state = self.data["state"]
        self.user_profile.save()
        return self.user_profile


class UserCreationForm(forms.Form):
    username = forms.CharField(label="Enter Username", min_length=4, max_length=150)
    email = forms.EmailField(label="Enter email")
    password1 = forms.CharField(label="Enter password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        r = get_user_model().objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not email:
            raise ValidationError("Email is required")
        r = get_user_model().objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_password1(self):
        user = User(
            username=self.cleaned_data.get("username"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password1"),
        )
        password_validators = [
            MinimumLengthValidator(),
            UserAttributeSimilarityValidator(),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]

        try:
            validate_password(
                password=self.cleaned_data["password1"],
                user=user,
                password_validators=password_validators,
            )
            return self.cleaned_data["password1"]
        except ValidationError as e:
            logger.error("validation failed")
            raise ValidationError(e)

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        user.set_password(self.cleaned_data["password1"])

        return user


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label="password1", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        user = User(
            username=self.cleaned_data.get("username"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password2"),
        )
        password_validators = [
            MinimumLengthValidator(),
            UserAttributeSimilarityValidator(),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]

        try:
            validate_password(
                password=self.cleaned_data["password2"],
                user=user,
                password_validators=password_validators,
            )
        except ValidationError as e:
            logger.error("validation failed")
            raise ValidationError(e)
        return self.cleaned_data["password2"]

    def save(self, uid, commit=True):
        user = get_user_model().objects.get(pk=uid)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class UpdatePasswordForm(forms.Form):
    password_current = forms.CharField(
        label="password_current", widget=forms.PasswordInput
    )
    password_new = forms.CharField(label="password_new", widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label="password_confirm", widget=forms.PasswordInput
    )

    def __init__(self, user, data=None):
        self.user = user
        super(UpdatePasswordForm, self).__init__(data=data)

    def clean_password_current(self):
        if not self.user.check_password(
            self.cleaned_data.get("password_current", None)
        ):
            raise ValidationError("Current password is incorrect")

    def clean_password_confirm(self):
        password1 = self.cleaned_data.get("password_new")
        password2 = self.cleaned_data.get("password_confirm")

        if password1 and password2 and password1 != password2:
            raise ValidationError("New passwords don't match")

        user = User(
            username=self.cleaned_data.get("username"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password_confirm"),
        )
        password_validators = [
            MinimumLengthValidator(),
            UserAttributeSimilarityValidator(),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
        ]

        try:
            validate_password(
                password=self.cleaned_data["password_confirm"],
                user=user,
                password_validators=password_validators,
            )
        except ValidationError as e:
            logger.error("validation failed")
            raise ValidationError(e)
        return self.cleaned_data["password_confirm"]

    def save(self, user, commit=True):
        user.set_password(self.cleaned_data["password_new"])
        user.save()
        return user


class GetEmailForm(forms.Form):
    email = forms.EmailField(label="email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        r = get_user_model().objects.filter(email=email)
        if r.count() == 0:
            raise ValidationError("Email doesn't exists")
        return email


class UserPreferenceForm(forms.Form):
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
        ("HighPBridge and Morrisania", "High Bridge and Morrisania"),
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
        ("Southwest Queens", "Southwest Queens"),
        ("Rockaways", "Rockaways"),
    ]

    CHOICES_CATEGORY = [
        ("newamerican", "newamerican"),
        ("armenian", "armenian"),
        ("barbeque", "barbeque"),
        ("bars", "bars"),
        ("bistros", "bistros"),
        ("burgers", "burgers"),
        ("chinese", "chinese"),
        ("danish", "danish"),
        ("diners", "diners"),
        ("ethiopian", "ethiopian"),
        ("filipino", "filipino"),
        ("french", "french"),
        ("georgian", "georgian"),
        ("german", "german"),
        ("greek", "greek"),
        ("hotdog", "hotdog"),
        ("italian", "italian"),
        ("bistros", "bistros"),
        ("japanese", "japanese"),
        ("jewish", "jewish"),
        ("kebab", "kebab"),
        ("korean", "korean"),
        ("kosher", "kosher"),
        ("mexican", "mexican"),
        ("noodles", "noodles"),
        ("pizza", "pizza"),
        ("salad", "salad"),
        ("sandwiches", "sandwiches"),
        ("seafood", "seafood"),
        ("sushi", "sushi"),
        ("tapassmallplates", "tapassmallplates"),
        ("vegan", "vegan"),
        ("vegetarian", "vegetarian"),
        ("vietnamese", "vietnamese"),
        ("waffles", "waffles"),
        ("wraps", "wraps"),
    ]

    CHOICES_RATING = [("5", "5"), ("4", "4"), ("3", "3"), ("2", "2"), ("1", "1")]

    CHOICES_COMPLIANCE = [("COVIDCompliant", "COVID-19 Compliant"), ("MOPDCompliant", "MOPD Compliant")]

    CHOICES_PRICE = [("price_1", "$"), ("price_2", "$$"), ("price_3", "$$$"), ("price_4", "$$$$")]

    category_list = forms.MultipleChoiceField(
        label="category_list", choices=CHOICES_CATEGORY, required=False
    )
    neighbourhood_list = forms.MultipleChoiceField(
        label="neighbourhood_list", choices=CHOICES_NEIGHBOURHOOD, required=False
    )
    rating_list = forms.MultipleChoiceField(
        label="rating_list", choices=CHOICES_RATING, required=False
    )
    compliance_list = forms.MultipleChoiceField(
            label="compliance_list", choices=CHOICES_COMPLIANCE, required=False
    )
    price_list =  forms.MultipleChoiceField(
            label="price_list", choices=CHOICES_PRICE, required=False
    )

    def save(self, user, commit=True):
        category_list = self.cleaned_data.get("category_list", [])
        neighbourhood_list = self.cleaned_data.get("neighbourhood_list", [])
        rating_list = self.cleaned_data.get("rating_list", [])
        compliance_list = self.cleaned_data.get("compliance_list", [])
        price_list = self.cleaned_data.get("price_list", [])
        # Save all new category preferences
        for category in category_list:
            user.preferences.add(Preferences.objects.filter(preference_type="category", value=category).first())
        # Save all new neighbourhood preferences
        for neighbourhood in neighbourhood_list:
            user.preferences.add(Preferences.objects.filter(preference_type="neighbourhood", value=neighbourhood).first())
        # Save all new rating preferences
        for rating in rating_list:
            user.preferences.add(Preferences.objects.filter(preference_type="rating", value=rating).first())
        # Save all new compliance preferences
        for compliance in compliance_list:
            user.preferences.add(Preferences.objects.filter(preference_type="compliance", value=compliance).first())
        # Save all new price preferences
        for price in price_list:
            user.preferences.add(Preferences.objects.filter(preference_type="price", value=price).first())


class ContactForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    subject = forms.CharField(label="Subject", max_length=120, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True, max_length=300)
