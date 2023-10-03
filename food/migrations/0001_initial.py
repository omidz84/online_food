# Generated by Django 4.2.5 on 2023-10-03 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, db_collation='utf8_persian_ci', unique=True,
                                          verbose_name='slug')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to='food.foodcategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Food category',
                'verbose_name_plural': 'Food categories',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.IntegerField(db_index=True, verbose_name='price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image')),
                ('count', models.SmallIntegerField(verbose_name='count')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, db_collation='utf8_persian_ci',
                                          max_length=100, unique=True, verbose_name='slug')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               to='food.foodcategory', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
        ),
    ]
