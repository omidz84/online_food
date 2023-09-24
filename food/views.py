from rest_framework import generics
from .serializers import FoodCategorySerializer
from .models import FoodCategory


class FoodCategoryView(generics.ListCreateAPIView):
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()


class DetailFoodCategoryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()


