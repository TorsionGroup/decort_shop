# Generated by Django 3.2.8 on 2021-10-08 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_rename_manufacturerid_manufacturerbrand_manufacturer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='manufacturer_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.manufacturerbrand'),
        ),
    ]
