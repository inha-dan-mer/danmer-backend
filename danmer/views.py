from django.shortcuts import render
from .models import Feedback,TuteeVideoPost,TutorVideoPost
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TutorVideoPostSerializer, TuteeVideoPostSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser

from danmer import serializers

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

class TutorVideoViewSet(viewsets.ModelViewSet):
    queryset = TutorVideoPost.objects.all()
    serializer_class = TutorVideoPostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    

class TuteeVideoViewSet(viewsets.ModelViewSet):
    queryset = TuteeVideoPost.objects.all()
    serializer_class = TuteeVideoPostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

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
