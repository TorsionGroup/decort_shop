# Generated by Django 3.2.9 on 2021-11-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_auto_20211126_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpointgps',
            name='extra_street',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customerpointgps',
            name='house_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]