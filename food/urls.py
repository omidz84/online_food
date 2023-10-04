from django.urls import path, re_path

from . import views


urlpatterns = [
    path('category/add/', views.FoodCategoryCreate.as_view(), name='add_category'),
    re_path(r'category/detail/(?P<slug>[^/]+)/?$', views.DetailFoodCategoryView.as_view(), name='category_detail'),
    path('category/', views.FoodCategoryView.as_view(), name='category_view'),
    path('', views.FoodViewInEachCategory.as_view(), name='food_view_in_each_category'),
    path('add/', views.CreatFoodView.as_view(), name='add_food'),
    re_path('detail/(?P<slug>[^/]+)/?$', views.DetailFoodView.as_view(), name='food_detail')
]
