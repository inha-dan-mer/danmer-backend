from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('dancing',views.TutorVideoViewSet)
router.register('practice',views.TuteeVideoViewSet)

urlpatterns = [
    path('',include(router.urls)),
    #path('practice/', views.TuteeVideoPostAPI.as_view(), name='tutee_video_post')
    #path("videos/", views.TutorVideoAPI.as_view(), name='TutorVideoList'),
]