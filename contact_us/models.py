from django.db import models
from django.utils.translation import gettext as _

from user.validators import check_phone


class ContactUs(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))
    phone_number = models.CharField(max_length=11, validators=[check_phone], db_index=True,
                                    verbose_name=_('phone number'))
    full_name = models.CharField(max_length=50, verbose_name=_('full_name'))
    is_read_by_admin = models.BooleanField(default=False, verbose_name=_('is read by admin'))
    response = models.TextField(null=True, blank=True, default='', verbose_name=_('response'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('contact us')

    def __str__(self):
        return f'{self.title}/{self.phone_number}'

