from django.db import models
from django.utils.translation import gettext as _

from user.models import MyUser
from cart.models import Cart


class Delivery(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, db_index=True, verbose_name=_('User'))
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, db_index=True, verbose_name=_('Cart'))
    is_delivered = models.BooleanField(default=False, verbose_name=_('Delivered / Not Delivered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        return f'user: {self.user} / cart: {self.cart}'

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")
