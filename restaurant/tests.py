from django.test import RequestFactory, TestCase
from django.forms.models import model_to_dict
from django.test import Client
from datetime import datetime, timedelta
from unittest import mock

from django.urls import reverse

from .forms import QuestionnaireForm
from django.contrib.auth import get_user_model
from .models import (
    Restaurant,
    InspectionRecords,
    YelpRestaurantDetails,
    Zipcodes,
    UserQuestionnaire,
    Categories,
    AccessibilityRecord,
    FAQ,
)
from .views import (
    get_inspection_info,
    get_landing_page,
    get_restaurant_profile,
    get_faqs_list,
)
from .utils import (
    merge_yelp_info,
    get_restaurant_info_yelp,
    get_restaurant_reviews_yelp,
    query_yelp,
    get_latest_inspection_record,
    get_restaurant_list,
    get_filtered_restaurants,
    get_latest_feedback,
    get_average_safety_rating,
    check_restaurant_saved,
    questionnaire_report,
    questionnaire_statistics,
    check_user_location,
)

from dinesafelysite.views import index

from user.models import (
    Review,
    Comment,
    Report_Ticket_Review,
    Report_Ticket_Comment,
)


import json

from django.contrib.auth.models import AnonymousUser


def create_restaurant(
    restaurant_name, business_address, yelp_detail, postcode, business_id
):
    return Restaurant.objects.create(
        restaurant_name=restaurant_name,
        business_address=business_address,
        yelp_detail=yelp_detail,
        postcode=postcode,
        business_id=business_id,
    )


def create_inspection_records(
    restaurant_inspection_id,
    restaurant_name,
    postcode,
    business_address,
    is_roadway_compliant,
    skipped_reason,
    inspected_on,
    business_id=None,
):
    return InspectionRecords.objects.create(
        restaurant_inspection_id=restaurant_inspection_id,
        restaurant_name=restaurant_name,
        postcode=postcode,
        business_address=business_address,
        is_roadway_compliant=is_roadway_compliant,
        skipped_reason=skipped_reason,
        inspected_on=inspected_on,
        business_id=business_id,
    )


def create_accessibility_record(
    restaurant_name,
    compliant,
    business_address,
    street_number,
    street_name,
    city,
    postcode="",
):
    return AccessibilityRecord.objects.create(
        restaurant_name=restaurant_name,
        compliant=compliant,
        business_address=business_address,
        street_number=street_number,
        street_name=street_name,
        city=city,
        postcode=postcode,
    )


def create_yelp_restaurant_details(
    business_id, neighborhood, price, rating, img_url, latitude, longitude
):
    return YelpRestaurantDetails.objects.create(
        business_id=business_id,
        neighborhood=neighborhood,
        price=price,
        rating=rating,
        img_url=img_url,
        latitude=latitude,
        longitude=longitude,
    )


def create_faq(question, answer):
    return FAQ.objects.create(question=question, answer=answer)


def create_review(user, restaurant, content, rating):
    return Review.objects.create(
        user=user,
        restaurant=restaurant,
        content=content,
        rating=rating,
    )


def create_comment(user, review, text):
    return Comment.objects.create(
        user=user,
        review=review,
        text=text,
    )


def create_report_review(user, review, reason):
    return Report_Ticket_Review.objects.create(
        user=user,
        review=review,
        reason=reason,
    )


def create_report_comment(user, comment, reason):
    return Report_Ticket_Comment.objects.create(
        user=user,
        comment=comment,
        reason=reason,
    )


class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def content(self):
        return self.content


class ModelTests(TestCase):
    def test_create_restaurant(self):
        restaurant = create_restaurant(
            restaurant_name="Gary Danko",
            business_address="800 N Point St",
            yelp_detail=None,
            postcode="94109",
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.restaurant_name, "Gary Danko")
        self.assertEqual(restaurant.business_address, "800 N Point St")
        self.assertEqual(restaurant.postcode, "94109")
        self.assertEqual(restaurant.business_id, "WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(
            str(restaurant),
            "1 Gary Danko 800 N Point St 94109 WavvLdfdP6g8aZTtbBQHTw None",
        )

    def test_is_accessible_compliant_true(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        accessibility_record = create_accessibility_record(
            restaurant_name="Just Salad",
            compliant=1,
            business_address="252 7th Ave",
            street_number="252",
            street_name="7th Ave",
            city="Brooklyn",
            postcode="11215",
        )
        restaurant.save()
        accessibility_record.save()
        self.assertTrue(restaurant.is_accessible_compliant())

    def test_is_accessible_compliant_false(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        accessibility_record = create_accessibility_record(
            restaurant_name="Just Salad",
            compliant=0,
            business_address="252 7th Ave",
            street_number="252",
            street_name="7th Ave",
            city="Brooklyn",
            postcode="11215",
        )
        restaurant.save()
        accessibility_record.save()
        self.assertFalse(restaurant.is_accessible_compliant())

    def test_is_accessible_compliant_not_found(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="1290 AVE AMERICAS",
            yelp_detail=None,
            postcode="10104",
            business_id="VSfYR6MriVSQDAmO0gPFPQ",
        )
        accessibility_record = create_accessibility_record(
            restaurant_name="Just Salad",
            compliant=1,
            business_address="252 7th Ave",
            street_number="252",
            street_name="7th Ave",
            city="Brooklyn",
            postcode="11215",
        )
        restaurant.save()
        accessibility_record.save()
        self.assertFalse(restaurant.is_accessible_compliant())

    def test_create_categories(self):
        cat = Categories(category="wine_bar", parent_category="bars")
        self.assertIsNotNone(cat)
        self.assertEqual(cat.category, "wine_bar")

    def test_create_inspection_records(self):
        inspection_record = create_inspection_records(
            restaurant_inspection_id="27555",
            restaurant_name="blah blah",
            postcode="11101",
            business_address="somewhere in LIC",
            is_roadway_compliant="Compliant",
            skipped_reason="Nan",
            inspected_on=datetime(2020, 10, 24, 17, 36),
        )
        self.assertIsNotNone(inspection_record)
        self.assertEqual(inspection_record.restaurant_inspection_id, "27555")
        self.assertEqual(inspection_record.restaurant_name, "blah blah")
        self.assertEqual(inspection_record.postcode, "11101")
        self.assertEqual(inspection_record.business_address, "somewhere in LIC")
        self.assertEqual(inspection_record.is_roadway_compliant, "Compliant")
        self.assertEqual(inspection_record.skipped_reason, "Nan")
        self.assertEqual(inspection_record.inspected_on, datetime(2020, 10, 24, 17, 36))
        self.assertEqual(
            str(inspection_record),
            "27555 blah blah Compliant Nan 2020-10-24 17:36:00 "
            "11101 somewhere in LIC None",
        )

    def test_yelp_restaurant_details(self):
        Categories.objects.create(category="wine_bar", parent_category="bars")
        details = YelpRestaurantDetails.objects.create(
            business_id="WavvLdfdP6g8aZTtbBQHTw",
            neighborhood="Upper East Side",
            price="$$",
            rating=4.0,
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg",
            latitude=40.8522129,
            longitude=-73.8290069,
        )

        YelpRestaurantDetails.objects.create(
            business_id="1",
            neighborhood="Upper East Side",
            price="$$",
            rating=4.0,
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg",
            latitude=40.8522129,
            longitude=-73.8290069,
        )

        category = Categories.objects.get(category="wine_bar")
        details.category.add(category)
        self.assertIsNotNone(details)
        self.assertEqual(details.business_id, "WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(details.neighborhood, "Upper East Side")
        self.assertEqual(details.price, "$$")
        self.assertEqual(details.rating, 4.0)
        self.assertEqual(
            details.img_url,
            "https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg",
        )
        self.assertEqual(details.latitude, 40.8522129)
        self.assertEqual(details.longitude, -73.8290069)
        self.assertEqual(
            str(details),
            "WavvLdfdP6g8aZTtbBQHTw Upper East Side restaurant.Categories.None $$ 4.0 https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg 40.8522129 -73.8290069",
        )

    def test_create_zipcodes(self):
        neigbourhood_map = Zipcodes(
            zipcode="11220",
            borough="Brooklyn",
            neighborhood="Sunset Park",
        )

        self.assertIsNotNone(neigbourhood_map)
        self.assertEqual(neigbourhood_map.zipcode, "11220")
        self.assertEqual(neigbourhood_map.borough, "Brooklyn")
        self.assertEqual(neigbourhood_map.neighborhood, "Sunset Park")
        self.assertEqual(str(neigbourhood_map), "11220 Brooklyn Sunset Park")

    def test_create_questionnaire(self):
        questionnaire = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now(),
            temperature_required="True",
            contact_info_required="True",
            employee_mask="True",
            capacity_compliant="True",
            distance_compliant="True",
        )
        self.assertIsNotNone(questionnaire)
        self.assertEqual(questionnaire.restaurant_business_id, "WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(questionnaire.user_id, "1")
        self.assertEqual(questionnaire.safety_level, "5")
        self.assertIsNotNone(questionnaire.saved_on)
        self.assertEqual(questionnaire.temperature_required, "True")
        self.assertEqual(questionnaire.contact_info_required, "True")
        self.assertEqual(questionnaire.employee_mask, "True")
        self.assertEqual(questionnaire.capacity_compliant, "True")
        self.assertEqual(questionnaire.distance_compliant, "True")
        self.assertEqual(
            str(questionnaire),
            "WavvLdfdP6g8aZTtbBQHTw 1 5 "
            + str(questionnaire.saved_on)
            + " True True True True True",
        )

    def test_create_accessibility_record(self):
        accessibility_record = create_accessibility_record(
            restaurant_name="Just Salad",
            compliant=1,
            business_address="252 7th Ave",
            street_number="252",
            street_name="7th Ave",
            city="Brooklyn",
            postcode="11215",
        )
        self.assertIsNotNone(accessibility_record)
        self.assertEqual(accessibility_record.restaurant_name, "Just Salad")
        self.assertEqual(accessibility_record.compliant, 1)
        self.assertEqual(accessibility_record.business_address, "252 7th Ave")
        self.assertEqual(accessibility_record.street_number, "252")
        self.assertEqual(accessibility_record.street_name, "7th Ave")
        self.assertEqual(accessibility_record.city, "Brooklyn")
        self.assertEqual(accessibility_record.postcode, "11215")

    def test_create_accessibility_record_no_postcode(self):
        accessibility_record = create_accessibility_record(
            restaurant_name="Just Salad",
            compliant=1,
            business_address="252 7th Ave",
            street_number="252",
            street_name="7th Ave",
            city="Brooklyn",
        )
        self.assertIsNotNone(accessibility_record)
        self.assertEqual(accessibility_record.restaurant_name, "Just Salad")
        self.assertEqual(accessibility_record.compliant, 1)
        self.assertEqual(accessibility_record.business_address, "252 7th Ave")
        self.assertEqual(accessibility_record.street_number, "252")
        self.assertEqual(accessibility_record.street_name, "7th Ave")
        self.assertEqual(accessibility_record.city, "Brooklyn")
        self.assertEqual(accessibility_record.postcode, "")


class InspectionRecordsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.inspection_records = create_inspection_records(
            restaurant_inspection_id="24111",
            restaurant_name="Tacos El Paisa",
            postcode="10040",
            business_address="1548 St. Nicholas btw West 187th street "
            "and west 188th "
            "street, Manhattan, NY",
            is_roadway_compliant="Compliance",
            skipped_reason="No Seating",
            inspected_on=datetime(2020, 10, 21, 12, 30, 30),
        )
        self.restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="16",
        )

    def test_get_valid_restaurant_inspections(self):
        request = self.factory.get("restaurant:inspection_history")
        request.restaurant = self.restaurant
        response = get_inspection_info(request, self.restaurant.id)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_restaurant_inspections(self):
        request = self.factory.get("restaurant:inspection_history")
        request.restaurant = self.restaurant
        self.restaurant.id = -1
        response = get_inspection_info(request, self.restaurant.id)
        self.assertEqual(response.status_code, 404)


class BaseTest(TestCase):
    def setUp(self):
        self.user_register_url = "user:register"
        self.c = Client()
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("pass123")
        self.dummy_user.save()
        self.dummy_user_questionnaire = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now(),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )

        return super().setUp


class UserQuestionnaireFormTests(BaseTest):
    def test_no_business_id(self):
        self.form_no_business_id = {
            "restaurant_business_id": "",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_business_id)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_user_id(self):
        self.form_no_user_id = {
            "restaurant_business_id": "",
            "user_id": "",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_user_id)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_safety_level(self):
        self.form_no_safety_level = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_safety_level)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_temperature_required(self):
        self.form_no_temperature_required = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_temperature_required)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_contact_info_required(self):
        self.form_no_contact_info_required = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_contact_info_required)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_employee_mask(self):
        self.form_no_employee_mask = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_employee_mask)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_capacity_compliant(self):
        self.form_no_capacity_compliant = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "",
            "distance_compliant": "true",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_capacity_compliant)
        self.assertFalse(questionnaire_form.is_valid())

    def test_no_distance_compliant(self):
        self.form_no_distance_compliant = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "saved_on": str(datetime.now()),
            "safety_level": "5",
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "",
        }
        questionnaire_form = QuestionnaireForm(self.form_no_distance_compliant)
        self.assertFalse(questionnaire_form.is_valid())

    def test_form_valid(self):
        self.form_valid = {
            "restaurant_business_id": "WavvLdfdP6g8aZTtbBQHTw",
            "user_id": "1",
            "safety_level": "5",
            "saved_on": datetime.now(),
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        form = QuestionnaireForm(self.form_valid)
        self.assertTrue(form.is_valid())

    def leave_rating(self):
        self.form = {
            "content": "test",
            "rating": "2",
            "rating_safety": "1",
            "rating_entry": "1",
            "rating_door": "1",
            "rating_table": "1",
            "rating_bathroom": "1",
            "rating_path": "1",
        }
        form = QuestionnaireForm(self.form)
        response = self.c.post("/restaurant/profile/1/", form)
        self.assertEqual(response.status_code, 302)

    def test_form_submission(self):
        create_restaurant(
            "random_name",
            "random_address",
            None,
            "random_postcode",
            "U8C69ISrhGTTubjqoVgZYg",
        )
        self.form = {
            "restaurant_business_id": "U8C69ISrhGTTubjqoVgZYg",
            "user_id": "1",
            "safety_level": "5",
            "saved_on": datetime.now(),
            "temperature_required": "true",
            "contact_info_required": "true",
            "employee_mask": "true",
            "capacity_compliant": "true",
            "distance_compliant": "true",
        }
        form = QuestionnaireForm(self.form)
        response = self.c.post("/restaurant/profile/1/", self.form)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)


class SearchFilterFormTests(BaseTest):
    def test_search_filter(self):
        search_filter_form = {
            "keyword": "chicken",
            "neighbourhood": ["Chelsea and Clinton"],
            "category": ["korean"],
            "price_1": True,
            "price_2": True,
            "price_3": True,
            "price_4": True,
            "rating": [1, 2, 3],
            "All": True,
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

    def test_search_filter_covid_compliant(self):
        search_filter_form = {
            "keyword": "",
            "neighbourhood": [],
            "category": [],
            "price_1": False,
            "price_2": False,
            "price_3": False,
            "price_4": False,
            "rating": [],
            "All": False,
            "COVIDCompliant": True,
            "MOPDCompliant": False,
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

    def test_search_filter_mopd_compliant(self):
        search_filter_form = {
            "keyword": "",
            "neighbourhood": [],
            "category": [],
            "price_1": False,
            "price_2": False,
            "price_3": False,
            "price_4": False,
            "rating": [],
            "All": False,
            "COVIDCompliant": False,
            "MOPDCompliant": True,
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)


# class RestaurantViewFormTests(BaseTest):
#     def test_restaurant_profile_view_questionnaire(self):
#         create_restaurant(
#             "random_name",
#             "random_address",
#             None,
#             "random_postcode",
#             "U8C69ISrhGTTubjqoVgZYg",
#         )
#         self.questionnaire_form = {
#             "restaurant_business_id": "U8C69ISrhGTTubjqoVgZYg",
#             "user_id": "1",
#             "safety_level": "5",
#             "saved_on": datetime.now(),
#             "temperature_required": "true",
#             "contact_info_required": "true",
#             "employee_mask": "true",
#             "capacity_compliant": "true",
#             "distance_compliant": "true",
#             "content": "",
#         }
#         form = QuestionnaireForm(self.questionnaire_form)
#         response = self.c.post("/restaurant/profile/1/", self.questionnaire_form)
#         self.assertTrue(form.is_valid())
#         self.assertEqual(response.status_code, 302)


class RestaurantViewTests(TestCase):
    """ Test Restaurant Views """

    def setUp(self):
        self.factory = RequestFactory()
        business_id = "WavvLdfdP6g8aZTtbBQHTw"
        neighborhood = "Upper East Side"
        price = "$$"
        rating = 4.0
        img_url = "https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg"
        latitude = 40.8522129
        longitude = -73.8290069

        details = create_yelp_restaurant_details(
            business_id,
            neighborhood,
            price,
            rating,
            img_url,
            latitude,
            longitude,
        )
        self.restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=details,
            postcode="10040",
            business_id="16",
        )

    def test_get_valid_restaurant_profile(self):
        request = self.factory.get("restaurant:profile")
        request.restaurant = self.restaurant
        request.user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        response = get_restaurant_profile(request, self.restaurant.id)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_restaurant_profile(self):
        request = self.factory.get("restaurant:profile")
        request.restaurant = self.restaurant
        self.restaurant.id = -1
        response = get_restaurant_profile(request, self.restaurant.id)
        self.assertEqual(response.status_code, 404)

    def test_valid_get_landing_page(self):
        request = self.factory.get("restaurant:browse")
        request.user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        response = get_landing_page(request, 6)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_profile_view_save_favorite(self):
        create_restaurant(
            "random_name",
            "random_address",
            None,
            "random_postcode",
            "U8C69ISrhGTTubjqoVgZYg",
        )
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("pass123")
        self.dummy_user.save()
        self.c = Client()
        self.c.login(username="myuser", password="pass123")

        url = reverse(
            "restaurant:save_favorite_restaurant", args=["U8C69ISrhGTTubjqoVgZYg"]
        )
        response = self.c.post(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.dummy_user.favorite_restaurants.all().count() == 1)

    def test_restaurant_profile_view_delete_favorite(self):
        create_restaurant(
            "random_name",
            "random_address",
            None,
            "random_postcode",
            "U8C69ISrhGTTubjqoVgZYg",
        )
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("pass123")
        self.dummy_user.save()
        self.c = Client()
        self.c.login(username="myuser", password="pass123")
        url = reverse(
            "restaurant:delete_favorite_restaurant", args=["U8C69ISrhGTTubjqoVgZYg"]
        )
        response = self.c.post(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.dummy_user.favorite_restaurants.all().count() == 0)

    def test_get_faqs_list(self):
        create_faq(
            "What are the benefits of becoming a registered user?",
            "save favorite restaurants, add user preferences, edit user profile, get recommendations.",
        )
        request = self.factory.get("restaurant:faqs")
        request.user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        response = get_faqs_list(request)
        self.assertEqual(response.status_code, 200)


class RestaurantUtilsTests(TestCase):
    def test_merge_yelp_info(self):
        restaurant_info = MockResponse(
            json.dumps(
                {
                    "id": "WavvLdfdP6g8aZTtbBQHTw",
                    "name": "Gary Danko",
                    "phone": "+14157492060",
                    "display_phone": "(415) 749-2060",
                    "review_count": 5296,
                    "rating": 4.5,
                    "price": "$$$$",
                    "img_url": "test_url.com",
                    "image_url": "test_url.com",
                }
            ),
            200,
        )
        restaurant_reviews = MockResponse(
            json.dumps(
                {
                    "reviews": [
                        {
                            "id": "xAG4O7l-t1ubbwVAlPnDKg",
                            "rating": 5,
                            "text": "Went back again to this place since the last "
                            "time i visited the bay area 5 "
                            "months ago, and nothing has changed. Still the "
                            "sketchy Mission, "
                            "Still the cashier...",
                            "time_created": "2016-08-29 00:41:13",
                        },
                        {
                            "id": "1JNmYjJXr9ZbsfZUAgkeXQ",
                            "rating": 4,
                            "text": 'The "restaurant" is inside a small deli so there '
                            "is no sit down area. Just grab "
                            "and go.\n\nInside, they sell individually "
                            "packaged ingredients so that you "
                            "can...",
                            "time_created": "2016-09-28 08:55:29",
                        },
                        {
                            "id": "SIoiwwVRH6R2s2ipFfs4Ww",
                            "rating": 4,
                            "text": "Dear Mission District,\n\nI miss you and your "
                            "many delicious late night food "
                            "establishments and vibrant atmosphere.  I miss "
                            "the way you sound and smell on "
                            "a...",
                            "time_created": "2016-08-10 07:56:44",
                        },
                    ],
                    "total": 3,
                    "possible_languages": ["en"],
                }
            ),
            200,
        )
        self.assertEqual(
            merge_yelp_info(restaurant_info, restaurant_reviews),
            {
                "info": json.loads(restaurant_info.content),
                "reviews": json.loads(restaurant_reviews.content),
            },
        )

    def test_get_restaurant_info_yelp(self):
        business_id = "WavvLdfdP6g8aZTtbBQHTw"
        response = get_restaurant_info_yelp(business_id)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["id"], business_id)

    def test_get_restaurant_reviews_yelp(self):
        business_id = "WavvLdfdP6g8aZTtbBQHTw"
        response = get_restaurant_reviews_yelp(business_id)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual("reviews" in data, True)

    @mock.patch("restaurant.utils.get_restaurant_reviews_yelp")
    @mock.patch("restaurant.utils.get_restaurant_info_yelp")
    def test_query_yelp(
        self, mock_get_restaurant_info_yelp, mock_get_restaurant_reviews_yelp
    ):
        business_id = "WavvLdfdP6g8aZTtbBQHTw"
        mock_get_restaurant_info_yelp.return_value = MockResponse(
            json.dumps({"id": business_id}), 200
        )
        mock_get_restaurant_reviews_yelp.return_value = MockResponse(
            json.dumps({"reviews": 1}), 200
        )
        data = query_yelp(business_id)
        self.assertIsNotNone(data)
        self.assertEqual(data["info"]["id"], business_id)
        self.assertEqual(data["reviews"], {"reviews": 1})

    def test_query_yelp_business_id_empty(self):
        business_id = None
        self.assertEqual(query_yelp(business_id), None)

    def test_get_restaurant_list(self):
        create_restaurant(
            "Gary Danko", "somewhere in LIC", None, "11101", "WavvLdfdP6g8aZTtbBQHTw"
        )
        create_inspection_records(
            restaurant_inspection_id="27555",
            restaurant_name="Gary Danko",
            postcode="11101",
            business_address="somewhere in LIC",
            is_roadway_compliant="Compliant",
            skipped_reason="Nan",
            inspected_on=datetime(2020, 10, 24, 17, 36),
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        YelpRestaurantDetails.objects.create(business_id="WavvLdfdP6g8aZTtbBQHTw")
        data = get_restaurant_list(1, 1)
        self.assertEqual(data[0]["yelp_info"]["id"], "WavvLdfdP6g8aZTtbBQHTw")

    def test_get_latest_feedback(self):
        questionnaire_old = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now(),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        questionnaire_new = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now() + timedelta(hours=1),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        latest_feedback = get_latest_feedback("WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(latest_feedback, model_to_dict(questionnaire_new))
        self.assertNotEqual(latest_feedback, model_to_dict(questionnaire_old))

    def test_get_average_safety_rating(self):
        UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="1",
            saved_on=datetime.now(),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="2",
            saved_on=datetime.now() + timedelta(hours=1),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="3",
            saved_on=datetime.now() + timedelta(hours=2),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        average_safety = get_average_safety_rating("WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(average_safety, "2.0")

    def test_check_restaurant_saved(self):
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("Dinesafely123")
        self.dummy_user.save()
        self.temp_rest = create_restaurant(
            "random_name",
            "random_address",
            None,
            "random_postcode",
            "U8C69ISrhGTTubjqoVgZYg",
        )
        self.dummy_user.favorite_restaurants.add(
            Restaurant.objects.get(business_id="U8C69ISrhGTTubjqoVgZYg")
        )
        self.assertTrue(check_restaurant_saved(self.dummy_user, 1))

    def test_questionnaire_report(self):
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("Dinesafely123")
        self.dummy_user.save()
        self.temp_rest = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_inspection = InspectionRecords.objects.create(
            restaurant_inspection_id="24111",
            restaurant_name="Tacos El Paisa",
            postcode="10040",
            business_address="1548 St. Nicholas btw West 187th street "
            "and west 188th "
            "street, Manhattan, NY",
            is_roadway_compliant="Compliant",
            skipped_reason="No Seating",
            inspected_on=datetime(2020, 10, 21, 12, 30, 30),
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_user_questionnaire = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now(),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        latest_inspection_status, valuable_questionnaire_list = questionnaire_report(
            "WavvLdfdP6g8aZTtbBQHTw"
        )
        self.assertEqual(latest_inspection_status, "Compliant")
        self.assertEqual(valuable_questionnaire_list[0], self.temp_user_questionnaire)

    def test_questionnaire_statistics(self):
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("Dinesafely123")
        self.dummy_user.save()
        self.temp_rest = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_inspection = InspectionRecords.objects.create(
            restaurant_inspection_id="24111",
            restaurant_name="Tacos El Paisa",
            postcode="10040",
            business_address="1548 St. Nicholas btw West 187th street "
            "and west 188th "
            "street, Manhattan, NY",
            is_roadway_compliant="Compliant",
            skipped_reason="No Seating",
            inspected_on=datetime(2020, 10, 21, 12, 30, 30),
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_user_questionnaire_1 = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="5",
            saved_on=datetime.now(),
            temperature_required="true",
            contact_info_required="true",
            employee_mask="true",
            capacity_compliant="true",
            distance_compliant="true",
        )
        self.temp_user_questionnaire_2 = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="1",
            saved_on=datetime.now(),
            temperature_required="false",
            contact_info_required="false",
            employee_mask="false",
            capacity_compliant="false",
            distance_compliant="false",
        )
        self.temp_user_questionnaire_3 = UserQuestionnaire.objects.create(
            restaurant_business_id="WavvLdfdP6g8aZTtbBQHTw",
            user_id="1",
            safety_level="3",
            saved_on=datetime.now(),
            temperature_required="false",
            contact_info_required="false",
            employee_mask="false",
            capacity_compliant="false",
            distance_compliant="false",
        )
        statistics_dict = questionnaire_statistics("WavvLdfdP6g8aZTtbBQHTw")
        self.assertEqual(statistics_dict["valuable_avg_safety_rating"], "3.0")
        self.assertEqual(statistics_dict["temp_check_true"], 1)
        self.assertEqual(statistics_dict["contact_info_required_true"], 1)
        self.assertEqual(statistics_dict["employee_mask_true"], 1)
        self.assertEqual(statistics_dict["capacity_compliant_true"], 1)
        self.assertEqual(statistics_dict["distance_compliant_true"], 1)


class IntegratedInspectionRestaurantsTests(TestCase):
    """ Test Restaurant Views """

    def test_valid_get_latest_inspections(self):
        restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="16",
        )
        InspectionRecords.objects.create(
            restaurant_inspection_id="24111",
            restaurant_name="Tacos El Paisa",
            postcode="10040",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            is_roadway_compliant="Compliant",
            skipped_reason="No Seating",
            inspected_on=datetime(2020, 10, 21, 12, 30, 30),
        )
        target_inspection = InspectionRecords.objects.create(
            restaurant_inspection_id="24112",
            restaurant_name="Tacos El Paisa",
            postcode="10040",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            is_roadway_compliant="Non-Compliant",
            skipped_reason="No Seating",
            inspected_on=datetime(2020, 10, 22, 12, 30, 30),
        )

        latest_inspection = get_latest_inspection_record(
            restaurant.restaurant_name,
            restaurant.business_address,
            restaurant.postcode,
        )

        q_mopd = Restaurant.objects.get(
            restaurant_name=restaurant.restaurant_name,
            business_address=restaurant.business_address,
        )
        mopd_status = q_mopd.mopd_compliance_status

        record = model_to_dict(target_inspection)
        record["inspected_on"] = record["inspected_on"].strftime("%Y-%m-%d %I:%M %p")
        record["mopd_compliance"] = mopd_status

        self.assertEqual(latest_inspection, record)

    @mock.patch("restaurant.utils.InspectionRecords.objects.filter")
    def test_get_latest_inspections_empty(self, mock_records):
        mock_records.return_value = InspectionRecords.objects.none()

    def test_invalid_get_inspection_info(self):
        restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="16",
        )
        latest_inspection = get_latest_inspection_record(
            restaurant.restaurant_name,
            restaurant.business_address,
            restaurant.postcode,
        )
        self.assertEqual(latest_inspection, None)


class GetFilteredRestaurantsTests(TestCase):
    """ Test Filter Restaurants module"""

    def test_get_filtered_restaurants(self):
        cat = Categories.objects.create(category="wine_bar", parent_category="bars")
        business_id = "WavvLdfdP6g8aZTtbBQHTw"
        neighborhood = "Upper East Side"
        price = "$$"
        rating = 4.0
        img_url = "https://s3-media1.fl.yelpcdn.com/bphoto/C4emY32GDusdMCybR6NmpQ/o.jpg"
        latitude = 40.8522129
        longitude = -73.8290069
        page = 0
        limit = 4

        details = create_yelp_restaurant_details(
            business_id,
            neighborhood,
            price,
            rating,
            img_url,
            latitude,
            longitude,
        )

        details.category.add(cat)
        details.save()
        create_restaurant(
            business_id=business_id,
            business_address="fake addres",
            yelp_detail=None,
            postcode="11111",
            restaurant_name="Test Italian Restaurant",
        )
        filtered_restaurants = get_filtered_restaurants(
            price=["$$"],
            neighborhood=["Upper East Side"],
            rating=[4.0],
            page=page,
            limit=limit,
        )

        self.assertEqual(details.business_id, filtered_restaurants[0].business_id)


class RestaurantRecommendationsTest(TestCase):
    """ Test Recommend Restaurants module"""

    def setUp(self):
        Categories.objects.create(category="chinese", parent_category="chinese")
        Categories.objects.create(category="wine-bar", parent_category="bars")
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        category_list = ["chinese", "wine-bar"]
        for category in category_list:
            self.dummy_user.preferences.add(Categories.objects.get(category=category))

        self.dummy_user2 = get_user_model().objects.create(
            username="myuser2",
            email="abcd@gmail.com",
        )

        self.factory = RequestFactory()

    def test_recommendation(self):

        categories = [
            category.category for category in self.dummy_user.preferences.all()
        ]
        categories.sort()
        self.assertEqual(len(self.dummy_user.preferences.all()), 2)
        self.assertEqual(categories[0], "chinese")
        self.assertEqual(categories[1], "wine-bar")
        self.assertIsNotNone(self.dummy_user2.preferences.all())
        self.assertEqual(len(self.dummy_user2.preferences.all()), 0)

    def test_index_view_recommendation(self):
        # test user with preferences
        request1 = self.factory.get("index")
        request1.user = self.dummy_user
        response1 = index(request1)
        self.assertEqual(response1.status_code, 200)

        # test user without preferences
        request2 = self.factory.get("index")
        request2.user = self.dummy_user2
        response2 = index(request2)
        self.assertEqual(response2.status_code, 200)


@mock.patch("user.models.Review.objects")
class EditCommentTests(BaseTest):
    def test_edit_comment(self, queryset):
        queryset.delete.return_value = None
        queryset.filter.return_value = queryset
        response = self.c.get(
            "/restaurant/profile/restaurant_id/comment/comment_id/delete"
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_comment(self, queryset):
        queryset.get.return_value = mock.Mock(spec=Review)
        response = self.c.get(
            "/restaurant/profile/restaurant_id/comment/comment_id/put"
        )
        self.assertEqual(response.status_code, 302)


class CreateCommentTest(BaseTest):
    @mock.patch("user.models.Review.objects")
    @mock.patch("user.models.Comment.__init__", mock.Mock(return_value=None))
    @mock.patch("user.models.Comment.save", mock.Mock(return_value=None))
    def test_edit_comment(self, queryset):
        queryset.get.return_value = None
        response = self.c.get(
            "/restaurant/profile/restaurant_id/comment_edit/review_id"
        )
        self.assertEqual(response.status_code, 302)


class DeleteCommentTest(BaseTest):
    @mock.patch("user.models.Comment.objects")
    def test_delete_comment(self, queryset):
        queryset.delete.return_value = None
        queryset.filter.return_value = queryset
        response = self.c.get(
            "/restaurant/profile/restaurant_id/comment_delete/comment_id"
        )
        self.assertEqual(response.status_code, 302)


class CommentTest(TestCase):
    def setUp(self):
        self.c = Client()
        # Initialize dummy user
        self.dummy_user = get_user_model().objects.create(
            username="testuser",
            email="test@gmail.com",
        )
        self.dummy_user.set_password("test1234Comment")
        self.dummy_user.save()

        # Initialize temp restaurant
        self.temp_restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_restaurant.save()

        # Initialize temp review
        self.temp_review = create_review(
            self.dummy_user,
            self.temp_restaurant,
            "review for tests",
            5,
        )
        self.temp_review.save()

    def test_delete_comment(self):
        self.dummy_comment = create_comment(
            self.dummy_user, self.temp_review, "comment for test deleting comment"
        )
        rest_id = self.temp_restaurant.id
        comm_id = self.dummy_comment.id
        print("test comment:", self.dummy_comment)
        delete_url = (
            "/restaurant/profile/" + str(rest_id) + "/comment_delete/" + str(comm_id)
        )
        response = self.c.get(delete_url)
        self.assertEqual(response.status_code, 302)


class ReportTests(TestCase):
    def setUp(self):
        self.c = Client()
        # Initialize 2 test users & 1 admin
        self.user1 = get_user_model().objects.create(
            username="user1",
            email="test1@gmail.com",
        )
        self.user1.set_password("test1234Report")
        self.user1.save()

        self.user2 = get_user_model().objects.create(
            username="user2",
            email="test2@gmail.com",
        )
        self.user2.set_password("test4321Report")
        self.user2.save()

        self.admin = get_user_model().objects.create(
            username="admin",
            email="admin@gmail.com",
        )
        self.admin.set_password("test1234Admin")
        self.admin.is_superuser = True
        self.admin.is_staff = True
        self.admin.save()

        # Initialize temp restaurant
        self.temp_restaurant = create_restaurant(
            restaurant_name="Tacos El Paisa",
            business_address="1548 St. Nicholas btw West 187th street and west 188th "
            "street, Manhattan, NY",
            yelp_detail=None,
            postcode="10040",
            business_id="WavvLdfdP6g8aZTtbBQHTw",
        )
        self.temp_restaurant.save()

        # Initialize temp review
        self.temp_review = create_review(
            self.user1,
            self.temp_restaurant,
            "review for tests",
            5,
        )
        self.temp_review.save()

        # Initialize temp comment
        self.temp_comment = create_comment(
            self.user2, self.temp_review, "comment for test report functions"
        )
        self.temp_comment.save()

    def test_report_review_model(self):
        report_ticket_review = create_report_review(
            self.user2, self.temp_review, "hate speech"
        )
        self.assertIsNotNone(report_ticket_review)
        self.assertEqual(report_ticket_review.user.id, self.user2.id)
        self.assertEqual(report_ticket_review.review.id, self.temp_review.id)
        self.assertEqual(report_ticket_review.reason, "hate speech")

    def test_report_comment_model(self):
        report_ticket_comment = create_report_comment(
            self.user1, self.temp_comment, "racist speech"
        )
        self.assertIsNotNone(report_ticket_comment)
        self.assertEqual(report_ticket_comment.user.id, self.user1.id)
        self.assertEqual(report_ticket_comment.id, self.temp_comment.id)
        self.assertEqual(report_ticket_comment.reason, "racist speech")

    def test_report_review_view(self):
        self.c.login(username="user2", password="test4321Report")
        rest_id = self.temp_restaurant.id
        review_id = self.temp_review.id
        url = "/restaurant/report/" + str(rest_id) + "/review/" + str(review_id)
        form = {
            "reason": "hate speech",
        }
        response = self.c.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.c.logout()

    def test_report_comment_view(self):
        self.c.login(username="user1", password="test1234Report")
        rest_id = self.temp_restaurant.id
        comm_id = self.temp_comment.id
        url = "/restaurant/report/" + str(rest_id) + "/comment/" + str(comm_id)
        form = {
            "reason": "racist speech",
        }
        response = self.c.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.c.logout()

    def test_hide_review(self):
        test_review = create_review(
            self.user1,
            self.temp_restaurant,
            "review for hide review tests, I'm hate speech",
            5,
        )
        test_review.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_review(self.user2, test_review, "hate speech")
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        review_id = test_review.id
        url = "/restaurant/report/review/hide/" + str(review_id)

        # test as normal user
        self.c.login(username="user2", password="test4321Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Review.objects.filter(review=test_review)
        test_review = Review.objects.get(pk=review_id)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(test_review.hidden, False)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Review.objects.filter(review=test_review)
        test_review = Review.objects.get(pk=review_id)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(test_review.hidden, True)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()

    def test_hide_comment(self):
        test_comment = create_comment(
            self.user2,
            self.temp_review,
            "comment for test hiding comments, I'm hate speech",
        )
        test_comment.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_comment(
                self.user1, test_comment, "hate speech"
            )
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        comment_id = test_comment.id
        url = "/restaurant/report/comment/hide/" + str(comment_id)

        # test as normal user
        self.c.login(username="user1", password="test1234Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Comment.objects.filter(comment=test_comment)
        test_comment = Comment.objects.get(pk=comment_id)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(test_comment.hidden, False)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Comment.objects.filter(comment=test_comment)
        test_comment = Comment.objects.get(pk=comment_id)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(test_comment.hidden, True)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()

    def test_ignore_review_report(self):
        test_review = create_review(
            self.user1,
            self.temp_restaurant,
            "review for hide review tests, I'm hate speech",
            5,
        )
        test_review.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_review(self.user2, test_review, "hate speech")
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        review_id = test_review.id
        url = "/restaurant/report/review/ignore/" + str(review_id)

        # test as normal user
        self.c.login(username="user2", password="test4321Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Review.objects.filter(review=test_review)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Review.objects.filter(review=test_review)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()

    def test_ignore_comment_report(self):
        test_comment = create_comment(
            self.user2,
            self.temp_review,
            "comment for test hiding comments, I'm hate speech",
        )
        test_comment.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_comment(
                self.user1, test_comment, "hate speech"
            )
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        comment_id = test_comment.id
        url = "/restaurant/report/comment/ignore/" + str(comment_id)

        # test as normal user
        self.c.login(username="user1", password="test1234Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Comment.objects.filter(comment=test_comment)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Comment.objects.filter(comment=test_comment)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()

    def test_delete_review_report(self):
        test_review = create_review(
            self.user1,
            self.temp_restaurant,
            "review for delete review tests, I'm hate speech",
            5,
        )
        test_review.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_review(self.user2, test_review, "hate speech")
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        review_id = test_review.id
        url = "/restaurant/report/review/delete/" + str(review_id)

        # test as normal user
        self.c.login(username="user2", password="test4321Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Review.objects.filter(review_id=review_id)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Review.objects.filter(review_id=review_id)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()

    def test_delete_comment_report(self):
        test_comment = create_comment(
            self.user2,
            self.temp_review,
            "comment for test delete comments, I'm hate speech",
        )
        test_comment.save()
        report_tickets_before = []
        for i in range(3):
            report_ticket = create_report_comment(
                self.user1, test_comment, "hate speech"
            )
            report_ticket.save()
            report_tickets_before.append(report_ticket)

        comment_id = test_comment.id
        url = "/restaurant/report/comment/delete/" + str(comment_id)

        # test as normal user
        self.c.login(username="user1", password="test1234Report")
        response1 = self.c.get(url)
        report_tickets1 = Report_Ticket_Comment.objects.filter(comment_id=comment_id)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(report_tickets1.exists(), True)

        self.c.logout()

        # test as admin
        self.c.login(username="admin", password="test1234Admin")
        response2 = self.c.get(url)
        report_tickets2 = Report_Ticket_Comment.objects.filter(comment_id=comment_id)

        self.assertEqual(response2.status_code, 302)
        self.assertEqual(report_tickets2.exists(), False)

        self.c.logout()


class FAQTest(TestCase):
    """ Test FAQ Model"""

    def setUp(self):
        self.faq1 = FAQ.objects.create(
            question="This is a sample question test",
            answer="This is a sample answer test",
        )

        self.faq2 = FAQ.objects.create(
            question="Here is a second test for a question",
            answer="Here is a second test for a test",
        )

        self.faq3 = FAQ.objects.create(
            question="This a sample question for test3",
            answer="This a sample answer for test3",
        )

    def test_str_representation(self):
        correct = "{} {}".format(self.faq1.question, self.faq1.answer)
        self.assertEqual(str(self.faq1), correct)

        correct = "{} {}".format(self.faq2.question, self.faq2.answer)
        self.assertEqual(str(self.faq2), correct)

        correct = "{} {}".format(self.faq3.question, self.faq3.answer)
        self.assertEqual(str(self.faq3), correct)

    def test_question_field(self):
        question1 = getattr(self.faq1, "question")
        question2 = getattr(self.faq2, "question")
        question3 = getattr(self.faq3, "question")

        self.assertEqual("This is a sample question test", question1)
        self.assertEqual("Here is a second test for a question", question2)
        self.assertEqual("This a sample question for test3", question3)

    def test_answer_field(self):
        answer1 = getattr(self.faq1, "answer")
        answer2 = getattr(self.faq2, "answer")
        answer3 = getattr(self.faq3, "answer")

        self.assertEqual("This is a sample answer test", answer1)
        self.assertEqual("Here is a second test for a test", answer2)
        self.assertEqual("This a sample answer for test3", answer3)

    def test_question_max_length(self):
        max_length = self.faq1._meta.get_field("question").max_length

        self.assertEqual(max_length, 200)


class SortTest(TestCase):
    """ Test Sort by rating/price/distance Feature """

    def setUp(self):
        self.factory = RequestFactory()

        # Create 1st restaurant
        business_id = "5qWjq_Qv6O6-iGdbBZb0tg"
        neighborhood = None
        price = "$"
        rating = 5.0
        img_url = "https://s3-media3.fl.yelpcdn.com/bphoto/pol6YeUS-47wemNAP6V2Mg/o.jpg"
        latitude = 40.80211
        longitude = -73.95665

        details_1 = create_yelp_restaurant_details(
            business_id,
            neighborhood,
            price,
            rating,
            img_url,
            latitude,
            longitude,
        )
        self.restaurant1 = create_restaurant(
            restaurant_name="Paint N Pour Nyc",
            business_address="2080 FREDERICK DOUGLASS BLVD",
            yelp_detail=details_1,
            postcode="10026",
            business_id="5qWjq_Qv6O6-iGdbBZb0tg",
        )

        # Create 2nd restaurant
        business_id = "blaTQKod-nz94F3Fm_ZoYQ"
        neighborhood = None
        price = "$$$"
        rating = 4.5
        img_url = "https://s3-media3.fl.yelpcdn.com/bphoto/xafcmRm6DDvcg7PYDrwICA/o.jpg"
        latitude = 40.80251
        longitude = -73.95355

        details_2 = create_yelp_restaurant_details(
            business_id,
            neighborhood,
            price,
            rating,
            img_url,
            latitude,
            longitude,
        )
        self.restaurant2 = create_restaurant(
            restaurant_name="Osteria Laura NYC",
            business_address="1890 Adam Clayton Powell Jr. Blvd.",
            yelp_detail=details_2,
            postcode="10026",
            business_id="blaTQKod-nz94F3Fm_ZoYQ",
        )

        # Create 3rd restaurant
        business_id = "DzlCEhXW6OadK6ETcmJpwQ"
        neighborhood = None
        price = "$$"
        rating = 4.0
        img_url = "https://s3-media4.fl.yelpcdn.com/bphoto/zyKuc6OmXL8W-gWnu9sMHw/o.jpg"
        latitude = 40.8022697271481
        longitude = -73.9567852020264

        details_3 = create_yelp_restaurant_details(
            business_id,
            neighborhood,
            price,
            rating,
            img_url,
            latitude,
            longitude,
        )
        self.restaurant3 = create_restaurant(
            restaurant_name="67 Orange Street",
            business_address="2082 Frederick Douglass Blvd",
            yelp_detail=details_3,
            postcode="10027",
            business_id="DzlCEhXW6OadK6ETcmJpwQ",
        )

        self.c = Client()
        self.dummy_user = get_user_model().objects.create(
            username="myuser",
            email="abcd@gmail.com",
        )
        self.dummy_user.set_password("pass123")
        self.dummy_user.save()

    def test_sort_by_distance(self):
        # Test sort form can be successfully submitted in browse
        # For anonymous user
        search_filter_form = {
            "form_sort": "distance",
            "form_location": "Central Park North, New York, NY, USA",
            "form_geocode": "40.7992147,-73.954758",
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)
        # For registered user
        self.c.login(username="myuser", password="pass123")
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)
        self.c.logout()

        # Test restaurants' order is correct if sort by distance
        # Order should be restaurant1, restaurant2, restaurant3
        filtered_restaurants = get_filtered_restaurants(
            page=0,
            limit=3,
            sort_option="distance",
            user_geocode="40.7992147,-73.954758",
        )
        self.assertEqual(
            self.restaurant1.business_id, filtered_restaurants[0].business_id
        )
        self.assertEqual(
            self.restaurant2.business_id, filtered_restaurants[1].business_id
        )
        self.assertEqual(
            self.restaurant3.business_id, filtered_restaurants[2].business_id
        )

        # Test check user location
        default_location = "Central Park North, New York, NY, USA"
        default_geocode = "40.7992147,-73.954758"
        form_location = "Updated Location Address, New York, NY, USA"
        form_geocode = "40.6941113,-73.98287069999999"
        # For registered user
        request = self.factory.get("restaurant:browse")
        request.user = self.dummy_user
        # - should return default location and geocode for the first time (location & geocode hasn't been setup)
        response_location, response_geocode = check_user_location(
            request.user, None, None
        )
        self.assertEqual(response_location, default_location)
        self.assertEqual(response_geocode, default_geocode)
        # - should update current_location & current_geocode in user model for the second time
        # - should return updated location & geocode
        response_location, response_geocode = check_user_location(
            request.user, form_location, form_geocode
        )
        self.assertEqual(response_location, form_location)
        self.assertEqual(response_geocode, form_geocode)
        self.assertEqual(response_location, self.dummy_user.current_location)
        self.assertEqual(response_geocode, self.dummy_user.current_geocode)

        # For anonymous user
        request = self.factory.get("restaurant:browse")
        request.user = AnonymousUser()
        # - should return default location and geocode for the first time
        response_location, response_geocode = check_user_location(
            request.user, None, None
        )
        self.assertEqual(response_location, default_location)
        self.assertEqual(response_geocode, default_geocode)
        # - should return updated location and geocode if changed location
        response_location, response_geocode = check_user_location(
            request.user, form_location, form_geocode
        )
        self.assertEqual(response_location, form_location)
        self.assertEqual(response_geocode, form_geocode)

    def test_sort_by_price(self):
        # Test sort form of pricelow and pricehigh can be successfully submitted in browse
        search_filter_form = {
            "form_sort": "pricelow",
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

        search_filter_form = {
            "form_sort": "pricehigh",
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

        # Test restaurants' order is correct if sort by pricelow
        # Order should be restaurant1, restaurant3, restaurant2
        filtered_restaurants = get_filtered_restaurants(
            page=0,
            limit=3,
            sort_option="pricelow",
        )
        self.assertEqual(
            self.restaurant1.business_id, filtered_restaurants[0].business_id
        )
        self.assertEqual(
            self.restaurant3.business_id, filtered_restaurants[1].business_id
        )
        self.assertEqual(
            self.restaurant2.business_id, filtered_restaurants[2].business_id
        )

        # Test restaurants' order is correct if sort by pricehigh
        # Order should be restaurant2, restaurant3, restaurant1
        filtered_restaurants = get_filtered_restaurants(
            page=0,
            limit=3,
            sort_option="pricehigh",
        )
        self.assertEqual(
            self.restaurant2.business_id, filtered_restaurants[0].business_id
        )
        self.assertEqual(
            self.restaurant3.business_id, filtered_restaurants[1].business_id
        )
        self.assertEqual(
            self.restaurant1.business_id, filtered_restaurants[2].business_id
        )

    def test_sort_by_rating(self):
        # Test sort form of ratedlow and ratedhigh can be successfully submitted in browse
        search_filter_form = {
            "form_sort": "ratedlow",
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

        search_filter_form = {
            "form_sort": "ratedhigh",
        }
        response = self.c.post(
            "/restaurant/search_filter/restaurants_list/1", search_filter_form
        )
        self.assertEqual(response.status_code, 200)

        # Test restaurants' order is correct if sort by ratedlow
        # Order should be restaurant3, restaurant2, restaurant1
        filtered_restaurants = get_filtered_restaurants(
            page=0,
            limit=3,
            sort_option="ratedlow",
        )
        self.assertEqual(
            self.restaurant3.business_id, filtered_restaurants[0].business_id
        )
        self.assertEqual(
            self.restaurant2.business_id, filtered_restaurants[1].business_id
        )
        self.assertEqual(
            self.restaurant1.business_id, filtered_restaurants[2].business_id
        )

        # Test restaurants' order is correct if sort by ratedhigh
        # Order should be restaurant1, restaurant2, restaurant3
        filtered_restaurants = get_filtered_restaurants(
            page=0,
            limit=3,
            sort_option="ratedhigh",
        )
        self.assertEqual(
            self.restaurant1.business_id, filtered_restaurants[0].business_id
        )
        self.assertEqual(
            self.restaurant2.business_id, filtered_restaurants[1].business_id
        )
        self.assertEqual(
            self.restaurant3.business_id, filtered_restaurants[2].business_id
        )
