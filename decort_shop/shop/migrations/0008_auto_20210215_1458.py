# Generated by Django 3.1.6 on 2021-02-15 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210215_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='deficit_available',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='no_show_balance',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='online_reserve',
            field=models.BooleanField(default=0, null=True),
        ),
    ]
