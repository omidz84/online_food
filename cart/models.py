from django.db import models
from django.utils.translation import gettext as _

from food.models import Food
from user.models import MyUser, Address


# Create your models here.


class Status(models.Model):
    status = models.CharField(max_length=1000, unique=True, db_index=True, verbose_name=_('status'))

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = _('status')


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT, verbose_name=_('user'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, db_index=True, verbose_name=_('status'), default=1)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_('address'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    def __str__(self):
        return f'{self.user} / {self.created_at}'

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart'), related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name=_('food'))
    price = models.IntegerField(verbose_name=_('price'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    total_price = models.IntegerField()

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.food.name}'


class LogStatus(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart_id'))
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=_('status_id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return f'{self.cart_id} / {self.status_id}'

    class Meta:
        verbose_name = _('log status')
