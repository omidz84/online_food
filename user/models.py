from django.contrib.gis.db import models as model
from django.db import models
from django.utils.translation import gettext as _

from . import validators


# Create your models here.


class MyUser(models.Model):

    class Type(models.TextChoices):
        admin = "1"
        customer = "2"
        delivery = "3"

    phoneNumber = models.CharField(max_length=11, validators=[validators.check_phone], unique=True, db_index=True,
                                   verbose_name=_("Phone Number"))
    type = models.CharField(choices=Type.choices, default=Type.customer, verbose_name=_("Type of User"))

    class Meta:
        verbose_name = _("Table of Users")

    def __str__(self):
        return f"Type: {self.type} -- Phone Number: {self.phoneNumber}"


class UserProfile(models.Model):
    userId = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, verbose_name=_("User Id"))
    fullName = models.CharField(max_length=200, blank=True, verbose_name=_("Full Name"))
    birthDate = models.DateField(max_length=200, blank=True, verbose_name=_("Data of Birth"))

    class Meta:
        verbose_name = _("Table of Users' Profile")

    def __str__(self):
        return f"{self.userId} -- {self.fullName}"


class Address(models.Model):
    address = model.TextField(verbose_name='آدرس')
    location = model.GeometryField(geography=True, null=True, blank=True, verbose_name='موقعیت')

