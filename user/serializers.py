from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import MyUser, UserProfile, Address
from . import validators


class UserCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=11, validators=[validators.check_phone])


#  ------------------------------------------------------------


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ['phoneNumber', 'code']

    def create(self, validated_data):
        user = MyUser.objects.create(phoneNumber=validated_data['phoneNumber'])

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


class AddressSerializers(GeoFeatureModelSerializer):

    class Meta:
        model = Address
        geo_field = "location"
        fields = '__all__'
