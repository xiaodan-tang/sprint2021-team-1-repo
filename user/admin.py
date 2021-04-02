# Register your models here.
from django.contrib import admin
from .models import (
    DineSafelyUser,
    User_Profile,
    Review,
    Comment,
    Report_Ticket_Review,
    Report_Ticket_Comment,
    RestaurantQuestion,
    RestaurantAnswer,
)

admin.site.register(DineSafelyUser)
admin.site.register(User_Profile)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Report_Ticket_Review)
admin.site.register(Report_Ticket_Comment)
admin.site.register(RestaurantQuestion)
admin.site.register(RestaurantAnswer)
