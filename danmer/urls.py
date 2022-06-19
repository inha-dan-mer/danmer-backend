from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers
import django_eventstream

# tutor_list = views.TutorVideoViewSet.as_view({"get": "list"})
# tutor_datail = views.TutorVideoViewSet.as_view({"get": "retrieve"})

router = routers.DefaultRouter(trailing_slash=False)
router.register("dancing", views.TutorVideoViewSet)
router.register("practice", views.TuteeVideoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("deep/tutor", views.TutorCoordinatePostAPI.as_view()),
    path("deep/tutee", views.TuteeFeedbackPostAPI.as_view()),
    path(
        "feedback/<user_id>/sse",
        include(django_eventstream.urls),
        {"format-channels": ["feedback-{user_id}"]},
    ),
    path("none/feedback", views.NoneFeedbackVideoList.as_view()),
    path("feedback/<tutee_id>", views.FeedbackList.as_view()),
]
