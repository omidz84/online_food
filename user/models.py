from django.contrib.gis.db import models as model
from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify

from . import validators


# Create your models here.
# We have two models (tables) in app "user": MyUser, UserProfile.

class UserType(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_("Title of User"))

    class Meta:
        verbose_name = _("User Type")

    def __str__(self):
        return f"{self.title}"

# -------------------------------------------------------------------------------------


class MyUser(models.Model):

    phone_number = models.CharField(max_length=11, validators=[validators.check_phone], unique=True, db_index=True,
                                    verbose_name=_("Mobile Phone Number"))
    type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, default=3, verbose_name=_("Type of User"))

    class Meta:
        verbose_name = _("User")

    def __str__(self):
        return f"Type: {self.type} -- Phone Number: {self.phone_number}"


# -------------------------------------------------------------------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, verbose_name=_("User Id"))
    first_name = models.CharField(max_length=200, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=200, verbose_name=_("Last Name"))
    birth_date = models.DateField(max_length=200, db_index=True, verbose_name=_("Data of Birth"))
    slug = models.SlugField(max_length=200, db_index=True, blank=True, verbose_name=_("Slug"))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.phone_number)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("User Profile")

    def __str__(self):
        return f"َUser: {self.user} -- Name: {self.first_name} {self.last_name}"

# ----------------------------------------------------------------------------------------


class Address(models.Model):
    address = model.TextField(verbose_name='آدرس')
    location = model.GeometryField(geography=True, null=True, blank=True, verbose_name='موقعیت')
