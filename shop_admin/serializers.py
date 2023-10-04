from rest_framework import serializers

from user.models import UserProfile
from user.validators import check_phone

# ------------------------------------------------------------------------------------------


class AdminSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[check_phone])


# ------------------------------------------------------------------------------------------


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"
