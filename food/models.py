from django.db import models
from django.utils.translation import gettext as _


class FoodCategory(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name=_('title'), unique=True)
    description = models.CharField(max_length=500, verbose_name=_('description'), null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name=_('parent'), null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name=_('image'), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Food category')
        verbose_name_plural = _('Food categories')

