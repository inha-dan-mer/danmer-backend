from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers


urlpatterns = [
    path('login', views.Login.as_view()),
]