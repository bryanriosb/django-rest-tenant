# Generated by Django 3.0 on 2021-04-06 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210324_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalproduct',
            old_name='mesure_unit',
            new_name='measure_unit',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='mesure_unit',
            new_name='measure_unit',
        ),
    ]
