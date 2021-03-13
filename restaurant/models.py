from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime


class Categories(models.Model):
    category = models.CharField(max_length=200, primary_key=True)
    parent_category = models.CharField(max_length=200, default=None, null=True)

    def __str__(self):
        return "{} {}".format(self.category, self.parent_category)


class YelpRestaurantDetails(models.Model):
    business_id = models.CharField(max_length=200, primary_key=True)
    neighborhood = models.CharField(max_length=200, default=None, null=True)
    category = models.ManyToManyField(Categories, blank=True)
    price = models.CharField(max_length=200, default=None, null=True)
    rating = models.FloatField(blank=True, default=0.0, null=True)
    img_url = models.CharField(max_length=200, default=None, null=True)
    latitude = models.DecimalField(
        max_digits=17, decimal_places=14, blank=True, default=0
    )
    longitude = models.DecimalField(
        max_digits=17, decimal_places=14, blank=True, default=0
    )

    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(
            self.business_id,
            self.neighborhood,
            self.category,
            self.price,
            self.rating,
            self.img_url,
            self.latitude,
            self.longitude,
        )


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200)
    business_address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    yelp_detail = models.ForeignKey(
        YelpRestaurantDetails,
        on_delete=models.SET_DEFAULT,
        max_length=200,
        default=1,
        blank=True,
        null=True,
        unique=True,
    )
    business_id = models.CharField(
        max_length=200, default=None, blank=True, null=True, unique=True
    )
    compliant_status = models.CharField(
        max_length=200, default=None, blank=True, null=True
    )

    class Meta:
        unique_together = (("restaurant_name", "business_address", "postcode"),)

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.id,
            self.restaurant_name,
            self.business_address,
            self.postcode,
            self.business_id,
            self.compliant_status,
        )


class InspectionRecords(models.Model):
    restaurant_inspection_id = models.CharField(max_length=200, primary_key=True)
    restaurant_name = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    business_address = models.CharField(max_length=200)
    is_roadway_compliant = models.CharField(max_length=200)
    skipped_reason = models.CharField(max_length=200)
    inspected_on = models.DateTimeField()
    business_id = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(
            self.restaurant_inspection_id,
            self.restaurant_name,
            self.is_roadway_compliant,
            self.skipped_reason,
            self.inspected_on,
            self.postcode,
            self.business_address,
            self.business_id,
        )


class UserQuestionnaire(models.Model):
    restaurant_business_id = models.CharField(max_length=200, null=False)
    user_id = models.CharField(max_length=200, null=False, default="")
    safety_level = models.CharField(max_length=1)
    saved_on = models.DateTimeField(default=timezone.now, null=False, blank=True)
    temperature_required = models.CharField(max_length=5, null=False, default="False")
    contact_info_required = models.CharField(max_length=5, null=False, default="False")
    employee_mask = models.CharField(max_length=5, null=False, default="False")
    capacity_compliant = models.CharField(max_length=5, null=False, default="False")
    distance_compliant = models.CharField(max_length=5, null=False, default="False")

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {}".format(
            self.restaurant_business_id,
            self.user_id,
            self.safety_level,
            self.saved_on,
            self.temperature_required,
            self.contact_info_required,
            self.employee_mask,
            self.capacity_compliant,
            self.distance_compliant,
        )


class Zipcodes(models.Model):
    zipcode = models.CharField(max_length=200, primary_key=True)
    borough = models.CharField(max_length=200, default=None, null=True)
    neighborhood = models.CharField(max_length=200, default=None, null=True)

    def __str__(self):
        return "{} {} {}".format(self.zipcode, self.borough, self.neighborhood)


class Review(models.Model):
    # Basic info
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )
    time = models.DateTimeField(default=datetime.now, editable=False)
    content = models.TextField()

    # Ratings
    rating = models.PositiveIntegerField(default=0)
    rating_safety = models.PositiveIntegerField(default=0)
    # Accessibility Ratings
    rating_entry = models.PositiveIntegerField(default=0)
    rating_door = models.PositiveIntegerField(default=0)
    rating_table = models.PositiveIntegerField(default=0)
    rating_bathroom = models.PositiveIntegerField(default=0)
    rating_path = models.PositiveIntegerField(default=0)

    # Images
    image1 = models.ImageField(null=True, blank=True, upload_to="review_images/")
    image2 = models.ImageField(null=True, blank=True, upload_to="review_images/")
    image3 = models.ImageField(null=True, blank=True, upload_to="review_images/")

    def __str__(self):
        return f"{self.user.username} review on {self.restaurant.restaurant_name}"

