# Generated by Django 3.1.7 on 2021-04-16 11:34

import creditcards.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_auto_20210416_1434'),
        ('customers', '0001_initial'),
        ('shop', '0017_auto_20210416_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropshippingWalletTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime.today, null=True)),
                ('card', creditcards.models.CardNumberField(blank=True, max_length=25, null=True)),
                ('agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_transfer_agreement', to='customers.customeragreement')),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_transfer_currency', to='shop.currency')),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_transfer_order', to='orders.order')),
            ],
            options={
                'verbose_name': 'DropshippingWalletTransfer',
                'verbose_name_plural': 'DropshippingWalletTransfers',
            },
        ),
        migrations.CreateModel(
            name='DropshippingWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('order_order', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_wallet_agreement', to='customers.customeragreement')),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_wallet_currency', to='shop.currency')),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='d_wallet_order', to='orders.order')),
            ],
            options={
                'verbose_name': 'DropshippingWallet',
                'verbose_name_plural': 'DropshippingWallets',
            },
        ),
    ]
