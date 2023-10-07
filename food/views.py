from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import FoodCategorySerializer, FoodCategoryViewSerializer,\
    FoodSerializer
from .models import FoodCategory, Food
from core.utils import translate
from core.permisions import IsAdmin, IsAdminOrReadOnly


# region CRUD of food category
class FoodCategoryCreate(generics.ListCreateAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    # permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_queryset().filter(parent=None)
        serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


# -------------------------------------------------------------------


class DetailFoodCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    # permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(None, status.HTTP_204_NO_CONTENT)
# endregion


# -------------------------------------------------------------------


class FoodCategoryView(generics.GenericAPIView):
    queryset = FoodCategory.objects.filter
    serializer_class = FoodCategoryViewSerializer

    def post(self, request):
        translate(request)
        try:
            parent_id = request.data['food_category_id']
            instance = self.queryset(parent=parent_id)
            serializer = FoodCategorySerializer(instance, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"msg": [_('this category_id does not exist')]}, status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------


class CreatFoodView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    # permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        translate(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


# -------------------------------------------------------------------


class DetailFoodView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    # permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        translate(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(None, status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------


class FoodViewInEachCategory(generics.GenericAPIView):
    queryset = Food.objects.filter
    serializer_class = FoodCategoryViewSerializer

    def post(self, request):
        translate(request)
        category_id = request.data['food_category_id']
        instance = self.queryset(category=category_id)
        serializer = FoodSerializer(instance, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
