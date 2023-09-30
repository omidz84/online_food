from django.contrib import admin

from .models import MyUser, UserProfile

# Register your models here.


# Introducing the models to Django admin site.
# In app "user", we have defined two models: MyUser, UserProfile.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass