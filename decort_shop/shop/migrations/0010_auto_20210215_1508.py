# Generated by Django 3.1.6 on 2021-02-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210215_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricetype',
            name='enabled',
            field=models.BooleanField(default=1, null=True),
        ),
    ]
