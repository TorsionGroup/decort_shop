# Generated by Django 3.1.7 on 2021-03-20 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_catalogcategory_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
