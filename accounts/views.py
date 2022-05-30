from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core import cache 
from .serializers import UserSerializer, AccessTokenObtainSerializer
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
#import arrow
# Create your views here.

User = get_user_model()

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




@permission_classes([AllowAny])
class SignupView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            User.objects.create(**serializer.data)
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)

