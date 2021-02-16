# Generated by Django 3.1.6 on 2021-02-16 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_auto_20210216_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='source',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='currency',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_source',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='executed',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='reserved',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
