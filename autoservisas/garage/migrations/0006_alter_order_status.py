# Generated by Django 4.2.1 on 2023-06-02 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0005_alter_car_license_plate_alter_car_vin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[(0, 'Not started'), (1, 'In progress'), (2, 'Delivered'), (3, 'Canceled')], default=0, help_text='Statusas', max_length=1, verbose_name='status'),
        ),
    ]
