from rest_framework import serializers

from user.models import MyUser, UserProfile
from user import validators


class AdminSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, validators=[validators.check_phone])

    class Meta:
        model = MyUser
        fields = ["phone_number"]


# ---------------------------------------------------------------------------------


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
