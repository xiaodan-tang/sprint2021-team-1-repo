"""dinesafelysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dinesafelysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403

urlpatterns = [
    path("", views.index, name="index"),
    path("terms/", views.terms, name="terms"),
    path("restaurant/", include("restaurant.urls")),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("accounts/", include("allauth.urls")),
    path("chatbot/", include("chatbot.urls")),
]

handler404 = "dinesafelysite.views.custom_error_404"  # noqa: F811
handler500 = "dinesafelysite.views.custom_error_500"  # noqa: F811
handler403 = "dinesafelysite.views.custom_error_403"  # noqa: F811


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
