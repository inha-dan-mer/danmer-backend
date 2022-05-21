from django.shortcuts import render, get_object_or_404
from .models import Feedback, TuteeVideoPost, TutorVideoPost
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TutorVideoPostSerializer, TuteeVideoPostSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model

from danmer import serializers

from accounts.models import User


class TutorVideoViewSet(viewsets.ModelViewSet):
    queryset = TutorVideoPost.objects.all().order_by('-pk')
    serializer_class = TutorVideoPostSerializer

    # list
    def list(self, request, *args, **kwargs):
        try:
            print("list")
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
    def perform_create(self, serializer):
        serializer.save(user=get_object_or_404(get_user_model(), pk=1))


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            video = serializer.data
            return Response(video, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(status = 400)
            
    # detail
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status = 400)

    # delete
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status = 400)

    # update
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            video = serializer.data
            return Response(video, status = 200)
        except:
            return Response(status = 400)



class TuteeVideoViewSet(viewsets.ModelViewSet):
    queryset = TuteeVideoPost.objects.all().order_by('-pk')
    serializer_class = TuteeVideoPostSerializer

    # post

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            video = serializer.data
            return Response(video, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(status = 400)

    def perform_create(self, serializer):
        # 임시 유저 설정 
        user = get_object_or_404(get_user_model(), pk=1)
        print(user)
        print("tvid:", serializer.validated_data['tutor_video_id'])
        tutor_video = get_object_or_404(
            TutorVideoPost, pk=serializer.validated_data['tutor_video_id'])
        print(tutor_video)
        serializer.save(user=user, tutor_video=tutor_video)

    # list
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data, stauts = 200)

            serializer = self.get_serializer(queryset, many=True)
            video_list = serializer.data
            return Response(video_list, status = 200)
        except : 
            return Response(status = 400)
    # detail
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            video = serializer.data
            return Response(video, status=200)
        except:
            return Response(status = 400)

    # delete
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status = 400)

    # update
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            video = serializer.data
            return Response(video, status = 200)
        except:
            return Response(status = 400)



# class TuteeVideoPostAPI(APIView):
#     def post(self, request, *args, **kwargs):
#         print("starttttttttttttttttt")
#         serializer = TuteeVideoPostSerializer(data = request.data)
#         print(type(serializer))
#         if serializer.is_valid():
#             serializer.save(user = self.request.user)
#             return Response(serializer.data, status = 201)
#         return Response(serializer.errors, status = 400)


#         serializer = TutorVideoPostSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save(user = self.request.user)
#             return Response(serializer.data, status = status.HTTP_201_OK)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# class TutorVideoAPI(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def get(self, request):
#         queryset = TutorVideoPost.objects.all()
#         serializer = TutorVideoPostSerializer(queryset, many = True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = TutorVideoPostSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save(user = self.request.user)
#             return Response(serializer.data, status = status.HTTP_201_OK)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
