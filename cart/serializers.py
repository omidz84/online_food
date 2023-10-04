from rest_framework import serializers

from food.models import Food, FoodCategory
from .models import Cart, Status, CartItem
from user.serializers import MyUserSerializers


class CartAddSerializers(serializers.Serializer):
    food_id = serializers.IntegerField(required=True)


# -----------------------------------------------------


class SaveCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user']


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
    user = MyUserSerializers(read_only=True)
    # items = FoodCartSerializer(read_only=True, many=True)
    status = StatusSerializers(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
