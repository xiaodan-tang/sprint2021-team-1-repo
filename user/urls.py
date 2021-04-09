from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.post_logout, name="logout"),
    path("register", views.register, name="register"),
    path(
        "reset_password/<base64_id>/<token>",
        views.reset_password_link,
        name="reset_password",
    ),
    path(
        "verification/<base64_id>/<token>",
        views.verify_user_link,
        name="verify_user_link",
    ),
    path("forget_password", views.forget_password, name="forget_password"),
    path("verification", views.forget_password, name="verification"),
    path("profile", views.profile, name="profile"),
    path("view_history", views.view_history, name="view_history"), #view history
    path("facing_page/<int:user_id>", views.user_facing, name="user_facing"),
    path("user_reviews", views.user_reviews, name="user_reviews"),
    path("update_password", views.update_password, name="update_password"),
    path(
        "add/preference/user",
        views.add_preference,
        name="add_preference",
    ),
    path(
        "delete/preference/user/<preference_type>/<value>",
        views.delete_preference,
        name="delete_preference",
    ),
    path("contact_form", views.contact_form, name="contact_form"),
    path("request_received", views.request_received, name="request_received"),
    path("admin_comment", views.show_report, name="admin_comment"),
]
