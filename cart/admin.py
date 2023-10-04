from django.contrib import admin
from .models import Cart, Status, LogStatus

# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(LogStatus)
class LogStatusAdmin(admin.ModelAdmin):
    pass
