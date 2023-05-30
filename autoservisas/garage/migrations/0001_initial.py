# Generated by Django 4.2.1 on 2023-05-30 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(db_index=True, max_length=100, verbose_name='license_plate')),
                ('vin', models.CharField(db_index=True, max_length=100, verbose_name='vin')),
                ('customer', models.TextField(db_index=True, max_length=100, verbose_name='customer')),
            ],
            options={
                'verbose_name': 'car',
                'verbose_name_plural': 'cars',
                'ordering': ['license_plate'],
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100, verbose_name='brand')),
                ('model', models.CharField(max_length=100, verbose_name='model')),
            ],
            options={
                'verbose_name': 'car model',
                'verbose_name_plural': 'car models',
                'ordering': ['brand', 'model'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, db_index=True, null=True, verbose_name='date')),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=18, null=True, verbose_name='price')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='garage.car', verbose_name='car')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ['date', 'id'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='garage.carmodel', verbose_name='model'),
        ),
    ]
