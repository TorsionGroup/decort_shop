# Generated by Django 3.1.7 on 2021-04-16 11:34

import creditcards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0016_auto_20210402_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('number', models.CharField(blank=True, max_length=250, null=True)),
                ('is_status', models.BooleanField()),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('is_active', models.BooleanField(default=1, null=True)),
                ('source_id', models.CharField(blank=True, max_length=300, null=True)),
                ('api_available', models.BooleanField(default=0, null=True)),
                ('api_token', models.CharField(blank=True, max_length=250, null=True)),
                ('customer', models.CharField(blank=True, max_length=300, null=True)),
                ('currency', models.CharField(blank=True, max_length=300, null=True)),
                ('price_type', models.CharField(blank=True, max_length=300, null=True)),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreement_currency', to='shop.currency')),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreement_customer', to='shop.customer')),
                ('price_type_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreement_price_type', to='shop.pricetype')),
            ],
            options={
                'verbose_name': 'CustomerAgreement',
                'verbose_name_plural': 'CustomerAgreements',
            },
        ),
        migrations.CreateModel(
            name='CustomerPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('source_id', models.CharField(blank=True, max_length=300, null=True)),
                ('add', models.CharField(blank=True, max_length=500, null=True)),
                ('customer', models.CharField(blank=True, max_length=500, null=True)),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='point_customer', to='shop.customer')),
            ],
            options={
                'verbose_name': 'CustomerPoint',
                'verbose_name_plural': 'CustomerPoints',
            },
        ),
        migrations.CreateModel(
            name='CustomerDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=300, null=True)),
                ('criteria_type', models.CharField(blank=True, max_length=250, null=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('customer', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement', models.CharField(blank=True, max_length=300, null=True)),
                ('price_type', models.CharField(blank=True, max_length=300, null=True)),
                ('brand', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_customer_agreement', to='customers.customeragreement')),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_customer_customer', to='shop.customer')),
                ('price_type_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount_customer_price_type', to='shop.pricetype')),
            ],
            options={
                'verbose_name': 'CustomerDiscount',
                'verbose_name_plural': 'CustomerDiscounts',
            },
        ),
        migrations.CreateModel(
            name='CustomerContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_user', models.BooleanField(default=1)),
                ('source_id', models.CharField(blank=True, max_length=300, null=True)),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_customer', to='shop.customer')),
            ],
            options={
                'verbose_name': 'CustomerContact',
                'verbose_name_plural': 'CustomerContacts',
            },
        ),
        migrations.CreateModel(
            name='CustomerCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('card', creditcards.models.CardNumberField(max_length=25)),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_customer', to='shop.customer')),
            ],
            options={
                'verbose_name': 'CustomerCard',
                'verbose_name_plural': 'CustomerCard',
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('past_due', models.DecimalField(decimal_places=2, default=0, max_digits=15, null=True)),
                ('customer', models.CharField(blank=True, max_length=300, null=True)),
                ('currency', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement', models.CharField(blank=True, max_length=300, null=True)),
                ('agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balance_agreement', to='customers.customeragreement')),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balance_currency', to='shop.currency')),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balance_customer', to='shop.customer')),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
            },
        ),
    ]
