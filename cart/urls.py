from django.urls import path

from . import views


app_name = 'cart'
urlpatterns = [
    path('add/', views.AddToCartView.as_view(), name='add'),
    path('show/', views.ShowCartView.as_view(), name='show'),
    path('remove/', views.RemoveInCartView.as_view(), name='remove'),
    path('save/', views.SaveCartView.as_view(), name='save'),
    path('orders/', views.ShowOrdersView.as_view(), name='orders'),
]
