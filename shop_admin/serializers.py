from rest_framework import serializers

from user.models import UserProfile
from user.validators import check_phone
from .models import Delivery
# ------------------------------------------------------------------------------------------


class AdminSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[check_phone])


# ------------------------------------------------------------------------------------------


class AdminProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"

# ------------------------------------------------------------------------------------------


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


# ------------------------------------------------------------------------------------------


class DeliveryListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)   # user_id means پیک


# -------------------------------------------------------------------------------------------

class UpdateStatusDeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ["id", "is_delivered", "cart"]
        read_only_fields = ['cart']





