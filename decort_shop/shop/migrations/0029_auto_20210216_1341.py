# Generated by Django 3.1.6 on 2021-02-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_auto_20210216_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='currency',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='price_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]
