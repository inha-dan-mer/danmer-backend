from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    #path('login', views.Login.as_view()),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.AccessTokenObtainView.as_view(), name='token_obtain'),
    #path('api/token/', views.MyTokenView.as_view(), name='token_obtain_pair'),
]