# Generated by Django 3.1.6 on 2021-02-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20210215_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='create_date',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='income_date',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
