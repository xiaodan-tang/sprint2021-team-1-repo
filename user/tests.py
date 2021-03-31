from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Preferences, RestaurantQuestion, RestaurantAnswer
from restaurant.tests import create_restaurant
from .forms import (
    UserCreationForm,
    ResetPasswordForm,
    GetEmailForm,
    UpdatePasswordForm,
    UserPreferenceForm,
    ContactForm,
    RestaurantQuestionForm,
    RestaurantAnswerForm,
)
from .utils import send_reset_password_email, send_feedback_email
from django.test import Client
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes


# Create your tests here.


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
        return super().setUp


class TestUserModel(BaseTest):
    def test_create_user(self):
        temp_user = get_user_model().objects.create_user("xiong")
        self.assertEqual(temp_user.username, "xiong")


class TestUserCreationForm(BaseTest):
    # def test_form_no_username(self):
    #     self.user_no_username = {
    #         "username": "",
    #         "email": "abcd@gmail.com",
    #         "password1": "pass123",
    #         "password2": "pass123",
    #     }
    #     form = UserCreationForm(self.user_no_username)
    #     self.assertFalse(form.is_valid())

    # def test_form_no_email(self):
    #     self.user_no_email = {
    #         "username": "myuser",
    #         "email": "",
    #         "password1": "pass123",
    #         "password2": "pass123",
    #     }
    #     form = UserCreationForm(self.user_no_email)
    #     self.assertFalse(form.is_valid())

    # def test_form_password_dont_match(self):
    #     self.user_password_dont_match = {
    #         "username": "myuser",
    #         "email": "abcd@gmail.com",
    #         "password1": "pass123",
    #         "password2": "pa123",
    #     }
    #     form = UserCreationForm(self.user_password_dont_match)
    #     self.assertFalse(form.is_valid())

    def test_form_valid(self):
        self.user_valid = {
            "username": "myuser1",
            "email": "abcde@gmail.com",
            "password1": "dinesafelypass123",
            "password2": "dinesafelypass123",
        }
        form = UserCreationForm(self.user_valid)
        self.assertTrue(form.is_valid())

    # def test_form_username_exists(self):
    #     self.user_valid = {
    #         "username": "myuser",
    #         "email": "abcde@gmail.com",
    #         "password1": "pass123",
    #         "password2": "pass123",
    #     }
    #     form = UserCreationForm(self.user_valid)
    #     form.has_error("username", "Username already exists")

    # def test_form_email_exists(self):
    #     self.user_valid = {
    #         "username": "myuser1",
    #         "email": "abcd@gmail.com",
    #         "password1": "pass123",
    #         "password2": "pass123",
    #     }
    #     form = UserCreationForm(self.user_valid)
    #     form.has_error("email", "Email already exists")


class TestResetPasswordForm(BaseTest):
    def test_form_password_dont_match(self):
        self.user_password_dont_match = {
            "password1": "dinesafelyhardPass123",
            "password2": "padinesafelyhardPass1234",
        }
        form = ResetPasswordForm(self.user_password_dont_match)
        self.assertFalse(form.is_valid())

    def test_save_password(self):
        # self.test_save_password = {
        #     "password1": "pass123",
        #     "password2": "pass123",
        # }
        # form = ResetPasswordForm(self.test_save_password)
        user = self.dummy_user

        response = self.c.post(
            "/user/reset_password/"
            + urlsafe_base64_encode(force_bytes(user.pk))
            + "/"
            + PasswordResetTokenGenerator().make_token(user),
            {"password1": "dinesafely1234", "password2": "dinesafely1234"},
        )
        # redirect to login page after reset
        self.assertEqual(response.status_code, 302)


class TestGetEmailForm(BaseTest):
    def test_email_valid(self):
        email_form = {"email": self.dummy_user.email}
        form = GetEmailForm(email_form)
        self.assertEqual(form.is_valid(), True)

    def test_email_invalid(self):
        email_form = {"email": "fake@email.com"}
        form = GetEmailForm(email_form)
        self.assertFalse(form.is_valid())


class TestUpdatePasswordForm(BaseTest):
    def test_update_password_form_invalid(self):
        form_data = {
            "password_current": "pass123",
            "password_new": "123456",
            "password_confirm": "1234567",
        }
        form = UpdatePasswordForm(user=self.dummy_user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_verify_user(self):
        user = self.dummy_user

        response = self.c.post(
            "/user/verification/"
            + urlsafe_base64_encode(force_bytes(user.pk))
            + "/"
            + PasswordResetTokenGenerator().make_token(user)
        )
        # redirect to login page after reset
        self.assertEqual(response.status_code, 302)


class TestUserPreferenceForm(BaseTest):
    def test_user_pref_form_valid(self):
        form_data = {
            "category_list": [
                "pizza",
                "waffles",
            ],
            "rating_list": [
                "4",
                "5",
            ],
            "price_list": [
                "price_1",
                "price_2",
            ],
            "compliance_list": [
                "COVIDCompliant",
            ],
        }
        user_pref_form = UserPreferenceForm(data=form_data)
        self.assertTrue(user_pref_form.is_valid())


class TestContactForm(BaseTest):
    def test_contact_form_valid(self):
        form_data = {
            "email": self.dummy_user.email,
            "subject": "Test subject",
            "message": "Test message: hello world!!!",
        }
        feedback_form = ContactForm(form_data)
        self.assertTrue(feedback_form.is_valid())

    def test_contact_form_invalid_email(self):
        form_data = {
            "email": "hello world",
            "subject": "Test subject",
            "message": "Test message: hello world!!!",
        }
        feedback_form = ContactForm(form_data)
        self.assertFalse(feedback_form.is_valid())

    def test_contact_form_missing_email(self):
        form_data = {
            "subject": "Test subject",
            "message": "Test message: hello world!!!",
        }
        feedback_form = ContactForm(form_data)
        self.assertFalse(feedback_form.is_valid())

    def test_contact_form_missing_subject(self):
        form_data = {
            "email": self.dummy_user.email,
            "message": "Test message: hello world!!!",
        }
        feedback_form = ContactForm(form_data)
        self.assertFalse(feedback_form.is_valid())

    def test_contact_form_invalid_message(self):
        form_data = {
            "email": self.dummy_user.email,
            "subject": "Test subject",
        }
        feedback_form = ContactForm(form_data)
        self.assertFalse(feedback_form.is_valid())


class TestFacingPage(BaseTest):
    def test_facing_page(self):
        self.c.force_login(self.dummy_user)
        response = self.c.get("/user/facing_page/1")
        self.assertEqual(response.status_code, 200)

    def test_no_user_logged_in(self):
        response = self.c.get("/user/facing_page/1")
        self.assertEqual(response.status_code, 302)


class TestUtils(BaseTest):
    class MockRequest:
        host_name = "localhost"

        def get_host(self):
            return self.host_name

    def test_send_reset_password_email(self):
        self.assertEqual(
            send_reset_password_email(self.MockRequest(), self.dummy_user.email), 1
        )

    def test_send_feedback_email(self):
        subject = "Test subject"
        message = "Test message: hello world!!!"
        self.assertTrue(
            send_feedback_email(
                self.MockRequest(), self.dummy_user.email, subject, message
            )
        )


class TestUserRegisterView(BaseTest):
    def test_view_register_page(self):
        response = self.c.post(
            "/user/register",
            {
                "username": "user_test_for_register",
                "email": "abcde@gmail.com",
                "password1": "hardPass123",
                "password2": "hardPass123",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_view_register_page_w_profile(self):
        response = self.c.post(
            "/user/register",
            {
                "username": "user_test_for_register",
                "email": "abcde@gmail.com",
                "password1": "hardPass123",
                "password2": "hardPass123",
                "phone": "1234567890",
                "address1": "123 main street",
                "address2": "123 main street",
                "city": "New York City",
                "zip_code": "1234567",
                "state": "California",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test__register_page_invalid_request(self):
        response = self.c.get(
            "/user/register",
            {
                "username": "myuser3",
                "email": "abcde@gmail.com",
                "password1": "pass123",
                "password2": "pass123",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_logout_request(self):
        response = self.c.post("/user/logout")
        self.assertEqual(response.status_code, 302)

    def test_already_logged_in_register_page(self):
        self.c.force_login(self.dummy_user)
        response = self.c.get("/user/register")
        self.assertEqual(response.status_code, 302)


class TestUserLoginView(BaseTest):
    def test_already_logged_in_login_page(self):
        self.c.force_login(self.dummy_user)
        response = self.c.get("/user/login")
        self.assertEqual(response.status_code, 302)

    def test_view_login_page(self):
        self.credentials = {
            "username": "myuser17",
            "email": "abcdefg@gmail.com",
            "password": "pass123",
        }
        get_user_model().objects.create_user(**self.credentials)
        response = self.c.post("/user/login", self.credentials)

        self.assertEqual(response.status_code, 302)

    def test__login_page_invalid_request(self):
        response = self.c.get(
            "/user/login", {"username": "myuser", "password": "pass123"}
        )
        self.assertEqual(response.status_code, 200)


class TestUpdatePasswordView(BaseTest):
    def test_no_user_logged_in(self):
        response = self.c.get("/user/update_password")
        self.assertEqual(response.status_code, 302)

    def test_update_password_save(self):
        self.c.force_login(self.dummy_user)
        response = self.c.post(
            "/user/update_password",
            {
                "password_current": "pass123",
                "password_new": "ReallyHardPassword123!",
                "password_confirm": "ReallyHardPassword123!",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_update_password_invalid_form(self):
        self.c.force_login(self.dummy_user)
        response = self.c.post(
            "/user/update_password",
            {
                "password_current": "pass123",
                "password_new": "ReallyHardPassword123!",
                "password_confirm": "FakePassword!",
                "update_pass_form": "",
            },
        )
        self.assertEqual(response.status_code, 400)


class TestAccountDetailsView(BaseTest):
    def test_view_profile_user_not_logged_in(self):
        response = self.c.get("/user/profile")
        self.assertEqual(response.status_code, 302)

    def test_view_profile_user_logged_in(self):
        self.c.force_login(self.dummy_user)
        response = self.c.get("/user/profile")
        self.assertEqual(response.status_code, 200)

    def test_update_user_profile(self):
        self.c.force_login(self.dummy_user)
        response = self.c.post(
            "/user/profile",
            {
                "user_id": self.dummy_user.id,
                "username": self.dummy_user.username,
                "profile-pic": SimpleUploadedFile(
                    "test.jpg", b"file_content", content_type="image/jpg"
                ),
            },
        )
        self.assertEqual(response.status_code, 302)


class TestUserReviewsView(BaseTest):
    def test_no_user_logged_in(self):
        response = self.c.get("/user/user_reviews")
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        self.c.force_login(self.dummy_user)
        response = self.c.get("/user/user_reviews")
        self.assertEqual(response.status_code, 200)


class TestForgetPasswordView(BaseTest):
    def test_forget_password_valid_email(self):
        response = self.c.post(
            "/user/forget_password",
            {
                "email": "abcd@gmail.com",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_forget_password_invalid_email(self):
        response = self.c.post(
            "/user/forget_password",
            {
                "email": "fake_email",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_forget_password_no_post(self):
        response = self.c.get(
            "/user/forget_password",
            {
                "email": "fake_email",
            },
        )
        self.assertEqual(response.status_code, 200)


class TestAddPrefView(BaseTest):
    def test_add_pref_valid(self):
        self.c.login(username="myuser", password="pass123")
        p1 = Preferences.objects.create(
            preference_type="category", value="pizza", display_value="Pizza"
        )
        p2 = Preferences.objects.create(
            preference_type="rating", value="4", display_value="4 Stars"
        )
        url = reverse("user:add_preference")
        form_data = {
            "category_list": [
                "pizza",
            ],
            "rating_list": [
                "4",
            ],
        }
        user_pref_form = UserPreferenceForm(form_data)
        self.assertTrue(user_pref_form.is_valid())
        response = self.c.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(p1), "category: pizza")
        self.assertEqual(str(p2), "rating: 4")


class TestDeletePrefView(BaseTest):
    def test_del_pref_valid(self):
        self.c.login(username="myuser", password="pass123")
        url = reverse("user:delete_preference", args=["category", "pizza"])
        Preferences.objects.create(
            preference_type="category", value="pizza", display_value="Pizza"
        )
        Preferences.objects.create(
            preference_type="rating", value="4", display_value="4 Stars"
        )
        response = self.c.post(path=url)
        self.assertEqual(response.status_code, 200)


class TestContactFormView(BaseTest):
    def test_contact_form_valid_data(self):
        response = self.c.post(
            "/user/contact_form",
            {
                "email": "abcd@gmail.com",
                "subject": "hello world",
                "message": "testing testing",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_contact_form_invalid_email(self):
        response = self.c.post(
            "/user/contact_form",
            {
                "email": "fake email",
                "subject": "hello world",
                "message": "testing testing",
            },
        )
        flash_message = list(response.context["messages"])
        self.assertEqual(
            str(flash_message[0]), "Invalid or missing data in contact form!"
        )
        self.assertEqual(response.status_code, 200)

    def test_contact_form_missing_email(self):
        response = self.c.post(
            "/user/contact_form",
            {
                "subject": "hello world",
                "message": "testing testing",
            },
        )
        flash_message = list(response.context["messages"])
        self.assertEqual(
            str(flash_message[0]), "Invalid or missing data in contact form!"
        )
        self.assertEqual(response.status_code, 200)

    def test_contact_form_missing_data(self):
        response = self.c.post(
            "/user/contact_form",
            {},
        )
        flash_message = list(response.context["messages"])
        self.assertEqual(
            str(flash_message[0]), "Invalid or missing data in contact form!"
        )
        self.assertEqual(response.status_code, 200)

    def test_request_received(self):
        response = self.c.get(
            "/user/request_received",
            {},
        )
        self.assertEqual(response.status_code, 200)


class TestRestaurantQuestionModel(BaseTest):
    def test_restaurant_question_str_function(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        q1 = RestaurantQuestion.objects.create(
            user=self.dummy_user, restaurant=restaurant, question="Test question??"
        )
        self.assertEqual(str(q1), "myuser question for JUST SALAD")

    def test_question_related_name(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        RestaurantQuestion.objects.create(
            user=self.dummy_user, restaurant=restaurant, question="Test question??"
        )
        user_questions = self.dummy_user.questions.first()
        restaurant_questions = restaurant.questions.first()
        self.assertEqual(user_questions.question, "Test question??")
        self.assertEqual(restaurant_questions.question, "Test question??")


class TestRestaurantAnswerModel(BaseTest):
    def test_restaurant_answer_str_function(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        q1 = RestaurantQuestion.objects.create(
            user=self.dummy_user, restaurant=restaurant, question="Test question??"
        )
        a1 = RestaurantAnswer.objects.create(
            user=self.dummy_user, question=q1, text="test answer!!"
        )
        self.assertEqual(str(a1), "myuser answered myuser's question for JUST SALAD")

    def test_answers_related_name(self):
        restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        q1 = RestaurantQuestion.objects.create(
            user=self.dummy_user, restaurant=restaurant, question="Test question??"
        )
        RestaurantAnswer.objects.create(
            user=self.dummy_user, question=q1, text="test answer!!"
        )
        user_answers = self.dummy_user.answers.first()
        question_answers = q1.answers.first()
        self.assertEqual(user_answers.text, "test answer!!")
        self.assertEqual(question_answers.text, "test answer!!")


class TestRestaurantQuestionForm(BaseTest):
    def setUp(self):
        self.restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        super(TestRestaurantQuestionForm, self).setUp()

    def test_question_form_valid(self):
        form_data = {
            "question": "Test question",
        }
        question_form = RestaurantQuestionForm(
            self.dummy_user, self.restaurant, form_data
        )
        self.assertTrue(question_form.is_valid())
        question_form.save()
        question_list = RestaurantQuestion.objects.filter(restaurant=self.restaurant)
        self.assertEqual(question_list.count(), 1)
        self.assertEqual(question_list[0].question, "Test question")

    def test_question_form_invalid_question(self):
        form_data = {
            "question": "",
        }
        question_form = RestaurantQuestionForm(
            self.dummy_user, self.restaurant, form_data
        )
        self.assertFalse(question_form.is_valid())

        form_data = {}
        question_form = RestaurantQuestionForm(
            self.dummy_user, self.restaurant, form_data
        )
        self.assertFalse(question_form.is_valid())


class TestRestaurantAnswerForm(BaseTest):
    def setUp(self):
        super(TestRestaurantAnswerForm, self).setUp()
        self.restaurant = create_restaurant(
            restaurant_name="JUST SALAD",
            business_address="252 7th Ave",
            yelp_detail=None,
            postcode="11215",
            business_id="kasdjf09j2oijlkdjsf",
        )
        self.question = RestaurantQuestion.objects.create(
            user=self.dummy_user,
            restaurant=self.restaurant,
            question="Test question",
        )

    def test_answer_form_valid(self):
        form_data = {
            "answer": "Test answer",
        }
        answer_form = RestaurantAnswerForm(self.dummy_user, self.question, form_data)
        self.assertTrue(answer_form.is_valid())
        answer_form.save()
        answer_list = RestaurantAnswer.objects.filter(question=self.question)
        self.assertEqual(answer_list.count(), 1)
        self.assertEqual(answer_list[0].text, "Test answer")

    def test_answer_form_invalid_answer(self):
        form_data = {
            "answer": "",
        }
        answer_form = RestaurantAnswerForm(self.dummy_user, self.question, form_data)
        self.assertFalse(answer_form.is_valid())

        form_data = {}
        answer_form = RestaurantAnswerForm(self.dummy_user, self.question, form_data)
        self.assertFalse(answer_form.is_valid())
