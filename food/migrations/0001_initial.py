# Generated by Django 4.2.5 on 2023-09-24 20:20

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
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='food.foodcategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Food category',
                'verbose_name_plural': 'Food categories',
            },
        ),
    ]
