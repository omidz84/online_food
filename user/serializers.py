from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import UserType, MyUser, UserProfile, Address
from . import validators


# The serializer "UserTypeSerializer" is for defining a model (table) for registering type of users
# 1: admin, 2: delivery, 3:customer.


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = "__all__"

#  ------------------------------------------------------------


# The serializer "UserCodeSerializer" is for creating a form to send code to the user who wants to
# "log in" or "register".


class UserCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[validators.check_phone])

#  ------------------------------------------------------------

# The serializer "UserSerializer" is for creating a form to "log in" or "register".


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ['phone_number', 'code']

    def create(self, validated_data):
        user = MyUser.objects.create(phone_number=validated_data['phone_number'])

# -----------

# The serializer "UserCreateRefreshSerializer" is for creating a form to create a new access token.


class UserCreateRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

#  ------------------------------------------------------------

# The serializer "UserProfileSerializer" is for creating a form to fill in the user profile.


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


#  ------------------------------------------------------------

# The serializer "UserLogoutSerializer" is for creating a form to "logout".


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

#  ------------------------------------------------------------


class MyUserSerializers(serializers.ModelSerializer):
    type = UserTypeSerializer(read_only=True)

    class Meta:
        model = MyUser
        fields = ['phone_number', 'type']


#  ------------------------------------------------------------


class AddressSerializers(GeoFeatureModelSerializer):

    class Meta:
        model = Address
        geo_field = "location"
        fields = ['address', 'user', 'location']


#  ------------------------------------------------------------


class UserAddressViewSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)



