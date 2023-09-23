from django.contrib.gis.db import models
# Create your models here.


class Address(models.Model):
    address = models.TextField(verbose_name='آدرس')
    location = models.GeometryField(geography=True, null=True, blank=True, verbose_name='موقعیت')

