# Generated by Django 4.2.5 on 2023-10-08 08:12

from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='title')),
                ('body', models.TextField(verbose_name='body')),
                ('phone_number', models.CharField(db_index=True, max_length=11, validators=[user.validators.check_phone], verbose_name='phone number')),
                ('full_name', models.CharField(max_length=50, verbose_name='full_name')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name='is read by admin')),
                ('response', models.TextField(blank=True, default='', null=True, verbose_name='response')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'contact us',
                'verbose_name_plural': 'contacts us',
            },
        ),
    ]
