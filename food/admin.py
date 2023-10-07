from django.contrib import admin
from .models import Food, FoodCategory

# Register your models here.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodCategory)
class FoodCategory(admin.ModelAdmin):
    pass
