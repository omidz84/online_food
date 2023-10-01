from django.urls import path

from . import views


urlpatterns = [
    path('create/category/', views.FoodCategoryCreate.as_view(), name='create_category'),
    path('update/category/<slug:slug>', views.DetailFoodCategoryView.as_view(), name='edit_category'),
    path('category/', views.FoodCategoryView.as_view(), name='category_view'),
    path('', views.FoodViewInEachCategory.as_view(), name='food_view_in_each_category'),
    path('create/food/', views.CreatFoodView.as_view(), name='create_food')
]
