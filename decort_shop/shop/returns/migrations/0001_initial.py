# Generated by Django 3.1.7 on 2021-04-20 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0017_auto_20210416_1434'),
        ('customers', '0002_auto_20210420_1149'),
        ('orders', '0003_auto_20210420_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProformReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=300, null=True)),
                ('source_customer', models.CharField(blank=True, max_length=300, null=True)),
                ('source_agreement', models.CharField(blank=True, max_length=300, null=True)),
                ('source_order', models.CharField(blank=True, max_length=300, null=True)),
                ('comment', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customeragreement')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'verbose_name': 'ProformReturn',
                'verbose_name_plural': 'ProformReturns',
            },
        ),
    ]