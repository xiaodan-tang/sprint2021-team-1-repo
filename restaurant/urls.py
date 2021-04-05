from django.urls import path

from restaurant import views

app_name = "restaurant"
urlpatterns = [
    path("faqs", views.get_faqs_list, name="faqs"),
    path("profile/<restaurant_id>/", views.get_restaurant_profile, name="profile"),
    path(
        "inspection_records/<restaurant_id>",
        views.get_inspection_info,
        name="inspection_history",
    ),
    path("", views.get_landing_page, name="browse"),
    path("<page>", views.get_landing_page, name="browse"),
    path(
        "search_filter/restaurants_list/<page>",
        views.get_restaurants_list,
        name="restaurants_list",
    ),
    path(
        "save/favorite/restaurant/<business_id>",
        views.save_favorite_restaurant,
        name="save_favorite_restaurant",
    ),
    path(
        "delete/favorite/restaurant/<business_id>",
        views.delete_favorite_restaurant,
        name="delete_favorite_restaurant",
    ),
    # Reviews & Comments
    path(
        "profile/<restaurant_id>/comment/<comment_id>/<action>",
        views.edit_review,
        name="edit_review",
    ),
    path(
        "profile/<restaurant_id>/user_comment/<comment_id>/<action>",
        views.edit_user_review,
        name="edit_user_review",
    ),
    path(
        "profile/<restaurant_id>/comment_edit/<review_id>",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "profile/<restaurant_id>/comment_delete/<comment_id>",
        views.delete_comment,
        name="delete_comment",
    ),
    # Reports related urls
    path(
        "report/<restaurant_id>/review/<review_id>",
        views.report_review,
        name="report_review",
    ),
    path(
        "report/<restaurant_id>/comment/<comment_id>",
        views.report_comment,
        name="report_comment",
    ),
    path("report/review/hide/<int:review_id>", views.hide_review, name="hide_review"),
    path(
        "report/review/ignore/<int:review_id>",
        views.ignore_review_report,
        name="ignore_review_report",
    ),
    path(
        "report/review/delete/<int:review_id>",
        views.delete_review_report,
        name="delete_review_report",
    ),
    path(
        "report/comment/hide/<int:comment_id>",
        views.hide_comment,
        name="hide_comment",
    ),
    path(
        "report/comment/ignore/<int:comment_id>",
        views.ignore_comment_report,
        name="ignore_comment_report",
    ),
    path(
        "report/comment/delete/<int:comment_id>",
        views.delete_comment_report,
        name="delete_comment_report",
    ),
    # Ask the community
    path(
        "profile/<restaurant_id>/ask_community/",
        views.get_ask_community_page,
        name="ask_community",
    ),
    path(
        "profile/<restaurant_id>/ask_community/<question_id>",
        views.answer_community_question,
        name="answer_community",
    ),
    # Others
    path("chatbot/keywordtest", views.chatbot_keyword, name="chatbottest"),
]
