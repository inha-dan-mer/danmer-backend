from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers
import django_eventstream

tutor_list = views.TutorVideoViewSet.as_view({"get": "list"})
tutor_datail = views.TutorVideoViewSet.as_view({"get": "retrieve"})

router = routers.DefaultRouter(trailing_slash=False)
router.register("dancing", views.TutorVideoViewSet)
router.register("practice", views.TuteeVideoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("test/", tutor_list),
    path("test/<int:pk>/", tutor_datail),
    path("deep/tutor", views.TutorCoordinatePostAPI.as_view()),
    path("deep/tutee", views.TuteeFeedbackPostAPI.as_view()),
    # path('practice/', views.TuteeVideoPostAPI.as_view(), name='tutee_video_post')
    # path("videos/", views.TutorVideoAPI.as_view(), name='TutorVideoList'),
    # path('feedback/test', views.FeedbackAPIView.as_view()),
    path(
        "feedback/<user_id>/sse",
        include(django_eventstream.urls),
        {"format-channels": ["feedback-{user_id}"]},
    ),
]
