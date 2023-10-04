from django.contrib import admin
from .models import Cart, Status, LogStatus, CartItem

# Register your models here.


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('food',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    inlines = (CartItemAdmin,)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(LogStatus)
class LogStatusAdmin(admin.ModelAdmin):
    pass


