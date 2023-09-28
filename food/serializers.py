from rest_framework import serializers

from .models import FoodCategory, Food


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = '__all__'


class FoodCategoryViewSerializer(serializers.Serializer):
    food_category_id = serializers.IntegerField()


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'
