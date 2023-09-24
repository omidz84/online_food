from django.urls import path

from . import views


urlpatterns = [
    path('create/category/', views.FoodCategoryView.as_view(), name='create_category'),
    path('update/category/<pk>', views.DetailFoodCategoryView.as_view(), name='create_category')

]
