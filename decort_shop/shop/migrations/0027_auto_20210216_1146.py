# Generated by Django 3.1.6 on 2021-02-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_customerdiscount_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='dropshippingwallet',
            name='agreement',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='dropshippingwallet',
            name='order',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='dropshippingwallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='dropshippingwallet',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='dropshippingwallet',
            name='debit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='pricebuffer',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]