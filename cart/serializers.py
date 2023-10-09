from rest_framework import serializers

from food.models import Food, FoodCategory
from .models import Cart, Status, CartItem


class CartAddSerializers(serializers.Serializer):
    food_id = serializers.IntegerField(required=True)


# -----------------------------------------------------


class SaveCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'address']


# -----------------------------------------------------


class ShowOrdersPostSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


# -----------------------------------------------------


class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status']


# -----------------------------------------------------


class CategoryCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['id', 'title']


# -----------------------------------------------------


class FoodCartSerializer(serializers.ModelSerializer):
    category = CategoryCartSerializers(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'image', 'category']


# -----------------------------------------------------


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodCartSerializer(read_only=True, many=True)

    class Meta:
        model = CartItem
        fields = ['food', 'price', 'quantity']


# -----------------------------------------------------


class ShowOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


# -----------------------------------------------------


class DetailOrderSerializers(serializers.Serializer):
    cart_id = serializers.IntegerField(required=True)


class UpdateStatusCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'status']
