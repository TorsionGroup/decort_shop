# Generated by Django 3.1.7 on 2021-04-20 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20210416_1434'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customercontact',
            name='source_id',
        ),
        migrations.AddField(
            model_name='customercontact',
            name='birthday',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='phone',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='source',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customercontact',
            name='source_customer',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='api_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='code',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='customeragreement',
            name='number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customercard',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.customer'),
        ),
        migrations.AlterField(
            model_name='customercard',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='customercontact',
            name='is_user',
            field=models.BooleanField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='customercontact',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customerdiscount',
            name='criteria_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
