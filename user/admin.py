# Register your models here.
from django.contrib import admin
from .models import (
    DineSafelyUser,
    User_Profile,
    Review,
)

admin.site.register(DineSafelyUser)
admin.site.register(User_Profile)
admin.site.register(Review)
