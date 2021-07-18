# Generated by Django 3.2.5 on 2021-07-18 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_product_category_id'),
        ('cart', '0002_auto_20210410_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_cart', to='shop.product'),
        ),
    ]
