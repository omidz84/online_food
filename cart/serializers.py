from rest_framework import serializers

from .models import Cart


class CartAddSerializers(serializers.Serializer):
    food_id = serializers.IntegerField(required=True)


class SaveCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'foods', 'final_price', 'status']


class ShowOrdersSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

