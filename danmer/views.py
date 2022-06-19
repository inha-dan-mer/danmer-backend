from django.shortcuts import render, get_object_or_404
from .models import TuteeVideoPost, TutorVideoPost
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    TutorVideoPostSerializer,
    TuteeVideoPostSerializer,
    TutorCoordinateSerializer,
    TuteeFeedbackSerializer,
    NoneFeedbackVideoSerializer,
)
from rest_framework import viewsets, status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.conf import settings
from danmer import serializers

from accounts.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

# SSE
import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import IntegrityError, transaction
from django.core.serializers.json import DjangoJSONEncoder
from django_eventstream import send_event, get_current_event_id

import boto3
import jwt
import requests

User = get_user_model()


@permission_classes([AllowAny])
class FeedbackList(APIView):
    def get(self, request, tutee_id=None):
        tutee_video = get_object_or_404(TuteeVideoPost, pk=tutee_id)
        tutor_video = tutee_video.tutor_video
        data = {
            "video_title": tutor_video.video_title,
            "tutee_id": tutee_id,
            "tutor_id": tutor_video.pk,
            "tutee_video_url": tutee_video.tutee_video.url,
            "tutor_video_url": tutor_video.video_url.url,
            "feedback_result": tutee_video.feedback_result,
        }
        return Response(data, status=200)


@permission_classes([AllowAny])
class NoneFeedbackVideoList(generics.ListAPIView):
    queryset = TuteeVideoPost.objects.filter(feedback_result={})
    serializer_class = NoneFeedbackVideoSerializer


# send tutor_video to deep server for coordinate file
def send_tutor_video(tutor_id, video_url):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {"video_url": video_url, "tutor_id": tutor_id}
    deep_server_url = "http://43.200.57.139:3000/api/process/tutor"
    response = requests.post(deep_server_url, data=json.dumps(data), headers=headers)
    return response.status_code


def send_tutee_video(coordinate_url, tutee_id, video_url):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "video_url": video_url,
        "tutee_id": tutee_id,
        "coordinate_url": coordinate_url,
    }
    deep_server_url = "http://43.200.57.139:3000/api/process/tutee"
    response = requests.post(deep_server_url, data=json.dumps(data), headers=headers)
    return response.status_code


@permission_classes([AllowAny])
class TutorVideoViewSet(viewsets.ModelViewSet):
    queryset = TutorVideoPost.objects.all().order_by("-pk")
    serializer_class = TutorVideoPostSerializer

    # list
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                print("serailizer.data:", serializer.data)
                print(type(serializer.data))
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            video_list = serializer.data
            return Response(video_list, status=200)
        except:
            return Response(status=400)

    # post
    def perform_create(self, serializer, payload):
        serializer.save(user=get_object_or_404(get_user_model(), pk=payload["user_id"]))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = jwt.decode(
            request.META["HTTP_X_AUTH_TOKEN"], settings.SECRET_KEY, algorithms="HS256"
        )
        self.perform_create(serializer, payload)
        headers = self.get_success_headers(serializer.data)
        video_data = serializer.data
        video = get_object_or_404(TutorVideoPost, pk=video_data["tutor_id"])
        send_tutor_video(video.pk, video.video_url.url)
        return Response(video_data, status=200, headers=headers)

    # detail
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status=400)

    # delete
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=400)

    # update
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status=400)


@permission_classes([AllowAny])
class TuteeVideoViewSet(viewsets.ModelViewSet):
    queryset = TuteeVideoPost.objects.all().order_by("-pk")
    serializer_class = TuteeVideoPostSerializer

    # post
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = jwt.decode(
                request.META["HTTP_X_AUTH_TOKEN"],
                settings.SECRET_KEY,
                algorithms="HS256",
            )
            self.perform_create(serializer, payload)
            headers = self.get_success_headers(serializer.data)
            print("headers", headers)
            video_data = serializer.data
            # send tuteevideo to deep_server
            video = get_object_or_404(TuteeVideoPost, pk=video_data["tutee_id"])
            send_tutee_video(
                video.tutor_video.coordinate_url,
                video.pk,
                video.tutee_video.url,
            )
            return Response(video_data, status=200, headers=headers)
        except KeyError:
            return Response(status=401)
        except:
            return Response(status=400)

    def perform_create(self, serializer, payload):
        # temporary user
        user = get_object_or_404(get_user_model(), pk=payload["user_id"])
        # print("tvid:", serializer.validated_data['tutor_video_id'])
        tutor_video = get_object_or_404(
            TutorVideoPost, pk=serializer.validated_data["tutor_video_id"]
        )
        serializer.save(user=user, tutor_video=tutor_video)

    # list
    def list(self, request, *args, **kwargs):
        try:
            payload = jwt.decode(
                request.META["HTTP_X_AUTH_TOKEN"],
                settings.SECRET_KEY,
                algorithms="HS256",
            )
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(user=payload["user_id"])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data, stauts=200)

            serializer = self.get_serializer(queryset, many=True)
            video_list = serializer.data
            return Response(video_list, status=200)
        except:
            return Response(status=400)

    # detail
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status=400)

    # delete
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=400)

    # update
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status=400)


# def update(self, request, *args, **kwargs):
tutor_update = TutorVideoViewSet.as_view({"post": "update"})


@permission_classes([AllowAny])
class TutorCoordinatePostAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TutorCoordinateSerializer(data=request.data)
        if serializer.is_valid():
            tutor_id = serializer.validated_data["tutor_id"]
            tutor_video = get_object_or_404(TutorVideoPost, pk=tutor_id)
            # tutor_serializer = TutorVideoPostSerializer(tutor_video, )
            tutor_video.coordinate_url = serializer.validated_data["coordinate_url"]
            tutor_video.save()
            # serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=400)


@permission_classes([AllowAny])
class TuteeFeedbackPostAPI(APIView):
    def dispatch(self, *args, **kwargs):
        response = super(TuteeFeedbackPostAPI, self).dispatch(*args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def post(self, request, *args, **kwargs):
        serializer = TuteeFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            tutee_id = serializer.validated_data["tutee_id"]
            tutee_video = get_object_or_404(TuteeVideoPost, pk=tutee_id)
            tutee_video.feedback_result = serializer.validated_data["feedback_result"]
            print(tutee_id, tutee_video)
            print(tutee_video.feedback_result)
            tutee_video.save()
            user_id = tutee_video.user.pk
            send_event(
                "feedback-{}".format(user_id),
                "message",
                {"status": "success", "user_id": user_id, "tutee_id": tutee_id},
            )
            return Response(status=200)
        return Response(serializer.errors, status=400)
