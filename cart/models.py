from django.db import models
from django.utils.translation import gettext as _

from user.models import MyUser

# Create your models here.


class Status(models.Model):
    status = models.CharField(max_length=1000, unique=True, db_index=True, verbose_name=_('status'))

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = _('status')


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, verbose_name=_('user'))
    foods = models.JSONField(default=list, verbose_name=_('foods'))
    final_price = models.JSONField(default=list, verbose_name=_('final price'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, db_index=True, verbose_name=_('status'), default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return f'{self.user} / {self.created_at}'

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class LogStatus(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.PROTECT, verbose_name=_('cart_id'))
    status_id = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_('status_id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return f'{self.cart_id} / {self.status_id}'

    class Meta:
        verbose_name = _('log status')
