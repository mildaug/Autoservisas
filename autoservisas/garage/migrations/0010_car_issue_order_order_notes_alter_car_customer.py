# Generated by Django 4.2.1 on 2023-06-06 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('garage', '0009_car_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='issue',
            field=tinymce.models.HTMLField(blank=True, max_length=1000, null=True, verbose_name='issue'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_notes',
            field=tinymce.models.HTMLField(blank=True, max_length=1000, null=True, verbose_name='order_notes'),
        ),
        migrations.AlterField(
            model_name='car',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
    ]
