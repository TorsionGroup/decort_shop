# Generated by Django 3.1.7 on 2021-04-16 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0017_auto_20210416_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=300, null=True)),
                ('is_visible', models.BooleanField(default=0)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_sale_customer', to='shop.customer')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_sale_product', to='shop.product')),
            ],
            options={
                'verbose_name': 'PromoSale',
                'verbose_name_plural': 'PromoSales',
            },
        ),
    ]
