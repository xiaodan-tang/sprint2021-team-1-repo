from django.db import models
from django.contrib.auth.models import AbstractUser
from restaurant.models import Restaurant, Categories
from phonenumber_field.modelfields import PhoneNumberField


class DineSafelyUser(AbstractUser):
    favorite_restaurants = models.ManyToManyField(Restaurant, blank=True)
    preferences = models.ManyToManyField(Categories, blank=True)


class User_Profile(models.Model):
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

    AUTH_STATUS_CHOICES = [
        ("certified", "Certified"),
        ("pending", "Pending"),
        ("uncertified", "Uncertified"),
    ]

    user = models.OneToOneField(
        DineSafelyUser, on_delete=models.CASCADE, null=True, related_name="user_profile"
    )
    photo = models.ImageField(
        default="default.jpg",
        upload_to="user_profile_pics",
    )
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    address1 = models.CharField("Address line 1", max_length=128, blank=True)
    address2 = models.CharField("Address line 2", max_length=128, blank=True)
    city = models.CharField("City", max_length=64, blank=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=10)
    state = models.CharField(max_length=128, choices=STATE_CHOICES, default="None")

    auth_status = models.CharField(
        "Authentication Status",
        max_length=16,
        choices=AUTH_STATUS_CHOICES,
        default="uncertified",
    )

    def __str__(self):
        return f"{self.user.username} User Profile"
