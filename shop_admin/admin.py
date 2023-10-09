from django.contrib import admin
from .models import Delivery

# Register your models here.


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass