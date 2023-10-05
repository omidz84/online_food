from django.db import models
from django.utils.translation import gettext as _


class FoodCategory(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name=_('title'), unique=True)
    description = models.CharField(max_length=500, verbose_name=_('description'), null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('parent'), null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name=_('image'), null=True, blank=True)
    slug = models.SlugField(max_length=50, db_index=True, unique=True, blank=True, allow_unicode=True,
                            db_collation='utf8_persian_ci', verbose_name=_('slug'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Food category')
        verbose_name_plural = _('Food categories')


# ------------------------------------------------------------


class Food(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name=_('name'), unique=True)
    description = models.TextField(verbose_name=_('description'))
    price = models.IntegerField(db_index=True, verbose_name=_('price'))
    image = models.ImageField(upload_to='images/', verbose_name=_('image'), null=True, blank=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, db_index=True, verbose_name=_('category'))
    count = models.SmallIntegerField(verbose_name=_('count'))
    slug = models.SlugField(max_length=100, db_index=True, verbose_name=_('slug'), unique=True, blank=True,
                            allow_unicode=True, db_collation='utf8_persian_ci')

    def __str__(self):
        return f'{self.name} / {self.price}'

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')
