from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core import cache
from danmer.models import TutorVideoPost, TuteeVideoPost
from danmer.serializers import TutorVideoPostSerializer, TuteeVideoPostSerializer
from .serializers import UserSerializer, AccessTokenObtainSerializer
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from django.contrib.auth.hashers import make_password
from django.conf import settings
import jwt

# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class ProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = jwt.decode(
            request.META["HTTP_X_AUTH_TOKEN"], settings.SECRET_KEY, algorithms="HS256"
        )
        uid = payload.get("user_id")
        user = get_object_or_404(User, pk=uid)
        tutor_video_list = TutorVideoPost.objects.filter(user=user)
        tutee_video_list = TuteeVideoPost.objects.filter(user=user)
        tutor_video_serializer = TutorVideoPostSerializer(tutor_video_list, many=True)
        tutee_vide_serializer = TuteeVideoPostSerializer(tutee_video_list, many=True)
        data = {
            "tutee_video_list": tutee_vide_serializer.data,
            "tutor_video_list": tutor_video_serializer.data,
        }
        return Response(data, status=200)


@permission_classes([AllowAny])
class AccessTokenObtainView(TokenViewBase):
    serializer_class = AccessTokenObtainSerializer


# @permission_classes([AllowAny])
# class Login(generics.GenericAPIView):
#     serializers_class = UserLoginSerializer
#     def post(self, request, *args, **kwargs):
#         # username, password
#         serializer = self.get_serializer(data = request.data)


#         if not serializer.is_valid(raise_exceptions=True):
#             return Response(status=409)
#         serializer.is_valid(raise_exceptions=True)
#         user = serializer.validated_data
#         print("user:",user)

#         return Response(
#             {
#                 "username" : user['username'],
#                 "token":user['token']
#             },
#             status=200)

# class UserCreateMixin(mixins.CreateModelMixin):
#     def perform_create(self, serializer):
#         print("pc:",serializer.data)
#         serializer.validated_data["password"] = make_password(serializer.validated_data['password'])
#         serializer.save()

# @permission_classes([AllowAny])
# class SignupView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
#     queryset =User.objects.all()
#     serializer_class = UserSerializer
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         print(serializer.validated_data["password"])
#         print(make_password(serializer.validated_data['password']))
#         serializer.validated_data["password"] = make_password(serializer.validated_data['password'])
#         print(serializer.validated_data["password"])

#         self.perform_create(serializer)
#         User.objects.create(**serializer.data)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def get(self, request, *args, **kwargs):
#         return self.list(request)

#     def post(self, request, *args, **kwargs):
#         return self.create(request)


@permission_classes([AllowAny])
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            User.objects.create_user(**serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
