# Generated by Django 3.1.7 on 2021-03-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210320_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogcategory',
            name='url',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]