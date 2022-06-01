from django.shortcuts import render, get_object_or_404
from .models import Feedback, TuteeVideoPost, TutorVideoPost
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TutorVideoPostSerializer, TuteeVideoPostSerializer, FeedbackSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model

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

from rest_framework.generics import ListCreateAPIView

@permission_classes([AllowAny])
def home(request):
    return render(request,'index.html')

## FIXME
@permission_classes([AllowAny])
class FeedbackAPIView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print("tvid :",serializer.validated_data['tutee_video_id'])
        print(type(serializer.validated_data['tutee_video_id']))
        data = serializer.validated_data['result_per_part']
        tutee_vid = serializer.validated_data['tutee_video_id']
        room_id = str(tutee_vid)
        send_event('room-{}'.format(room_id),'message',{"test":"fuckkkk"})
        send_event('room-{}'.format(room_id),'message',data)
        data = json.dumps(serializer.validated_data['result_per_part'], cls=DjangoJSONEncoder)+'\n'
        print("data:",data)
        return HttpResponse(data, content_type='application/json')
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # def get(self, request):
    #     # FIXME all feedback -> feed back of request user
    #     feedbacks = Feedback.objects.all()
    #     serializer = FeedbackSerializer(feedbacks, many=True)
    #     return Response(serializer.data)



    # def create(self, request, *args, **kwargs):
    #     print("create")
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     send_event('feedback-{}'.format(serializer.validated_data['tutee_video_id']),'message','helper')
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # send feedback and push event server
    # def post(self, request):
    #     serializer = FeedbackSerializer(data = request.data)
        
    #     if serializer.is_valid():
    #         print("data:",serializer.validated_data)
    #         data = json.dumps(serializer.validated_data['result_per_part'], cls=DjangoJSONEncoder)+'\n'
    #         send_event('feedback-{}'.format(serializer.validated_data['tutee_video_id']),'message','helper')
    #         return HttpResponse(data, content_type='application/json')
    #     return Response(status=400)



# def send_feedback(request, tutee_vid):
#     if request.method == 'GET':
#         last_id = get_current_event_id(['feedback-{}'.format(tutee_vid)])
#         try:
#             tutee_video_post = TuteeVideoPost.objects.get(pk = tutee_vid)
#             feedback = Feedback.objects.filter(post = tutee_video_post).order_by('-pk')[0]
#         except Feedback.DoesNotExist:
#             feedback =[]
#         data = json.dumps(
#             {
#                 'feedback': feedback,
#                 'last-event-id':last_id
#             },
#             cls = DjangoJSONEncoder
#         )+'\n'
#         return HttpResponse(data, content_type='application/json')
    
#     elif request.method == 'POST':
#         try: 
#             tutee_video_post = TuteeVideoPost.objects.get(pk = tutee_vid)
#         except TuteeVideoPost.DoesNotExist:
#             return Response(status = 400)


## FIXME
@permission_classes([AllowAny])
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
        print("user:",get_object_or_404(get_user_model(), pk=1))
        serializer.save(user=get_object_or_404(get_user_model(), pk=1))


    def create(self, request, *args, **kwargs):
        try:
            print("request data:", request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("before perform create")
            self.perform_create(serializer)
            print("after perform create")
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

## FIXME
@permission_classes([AllowAny])
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
        # temporary user
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



##test

