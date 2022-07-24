from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

# only access token test
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

User = get_user_model()


class AccessTokenObtainSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "password"
        ] = serializers.CharField()  # add fields "password" to token

    @classmethod
    def get_token(cls, user):  # create token
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token

    def validate(self, attrs):
        print(attrs)
        data = super().validate(attrs)

        # add token and username, userid to response data
        token = self.get_token(self.user)
        data["token"] = str(token)
        data["username"] = self.user.username
        data["user_id"] = self.user.pk
        print(data)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password")
        )  # for pw encryption
        print("vd:", validated_data)
        return User(**validated_data)


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
# }
