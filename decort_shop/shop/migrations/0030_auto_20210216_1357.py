# Generated by Django 3.1.6 on 2021-02-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_auto_20210216_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='product',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]