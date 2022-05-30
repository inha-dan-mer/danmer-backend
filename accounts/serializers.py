from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
# from rest_framework_jwt.settings import api_settings

# only access token test
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

class AccessTokenObtainSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def validate(self, attrs):
        data = super().validate(attrs)

        # add token and username to response data
        token = self.get_token(self.user)
        data["token"] = str(token)
        data["username"] = self.user.username
        return data


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username','email','password']

# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=20)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only = True)

#     def validate(self,data):
#         print(type(data))
#         print(data)
#         username = data.get("username", None)
#         password = data.get("password", None)
        # try:
        #     user = authenticate(username = username, password =password)
        #     payload = JWT_PAYLOAD_HANDLER(user)
        #     jwt_token = JWT_ENCODE_HANDLER(payload)
        #     update_last_login(None, user)
        # except User.DoesNotExist:
        #     raise serializers.ValidationError('User does not exist.')
        # return{
        #     'username':user.username,
        #     'token': jwt_token,
        #}