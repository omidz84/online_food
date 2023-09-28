from rest_framework import serializers


class CartAddSerializers(serializers.Serializer):
    food_id = serializers.IntegerField(required=True)
