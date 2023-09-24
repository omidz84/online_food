from rest_framework import serializers
from .models import User, UserProfile
from . import validators


class UserCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=11, validators=[validators.check_phone])


#  ------------------------------------------------------------


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ['phoneNumber', 'code']

    def create(self, validated_data):
        user = User.objects.create(phoneNumber=validated_data['phoneNumber'])

# -----------


class UserCreateRefreshSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()

#  ------------------------------------------------------------


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


#  ------------------------------------------------------------


class UserLogoutSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()