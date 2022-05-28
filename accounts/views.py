from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core import cache 
from .serializers import UserSerializer, UserLoginSerializer

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

#import arrow
# Create your views here.

User = get_user_model()

@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializers_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        # username, password
        serializer = self.get_serializer(data = request.data)
        
    
        if not serializer.is_valid(raise_exceptions=True):
            return Response(status=409)
        serializer.is_valid(raise_exceptions=True)
        user = serializer.validated_data
        print("user:",user)

        return Response(
            {
                "username" : user['username'],
                "token":user['token']
            },
            status=200)





# class SignupView(APIView):
#     def post(self,request):
#         username = request.data['username']
#         email = request.data['email']
#         password = request.data['password']
#         user = get_user_model().objects.create_user(username=username, email=email, password=password)
#         user.save()

#         token = Token.objects.create(user = user)
#         return Response({"token":token.key})

