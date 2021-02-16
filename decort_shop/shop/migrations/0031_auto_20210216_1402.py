# Generated by Django 3.1.6 on 2021-02-16 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20210216_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='saletask',
            name='customer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='saletask',
            name='product',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]