# Generated by Django 3.1.6 on 2021-02-16 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20210215_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeragreement',
            name='currency',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customeragreement',
            name='customer',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customeragreement',
            name='price_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='api_available',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='is_active',
            field=models.BooleanField(default=1, null=True),
        ),
    ]