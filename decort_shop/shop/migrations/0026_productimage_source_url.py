# Generated by Django 3.2.5 on 2021-07-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_auto_20210725_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='source_url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
