from django.contrib import admin
from .models import MyUser, UserProfile

# Register your models here.

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass