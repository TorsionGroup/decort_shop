# Generated by Django 3.1.7 on 2021-03-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210320_0947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catalogcategory',
            old_name='slug',
            new_name='url',
        ),
    ]
