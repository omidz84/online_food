# Generated by Django 4.2.5 on 2023-09-28 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foods', models.JSONField(default=list, verbose_name='foods')),
                ('final_price', models.JSONField(default=list, verbose_name='final price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(db_index=True, max_length=1000, unique=True, verbose_name='status')),
            ],
            options={
                'verbose_name': 'status',
            },
        ),
        migrations.CreateModel(
            name='LogStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cart.cart', verbose_name='cart_id')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cart.status', verbose_name='status_id')),
            ],
            options={
                'verbose_name': 'log status',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='cart.status', verbose_name='status'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.myuser', verbose_name='user'),
        ),
    ]
