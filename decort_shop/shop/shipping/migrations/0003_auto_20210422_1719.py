# Generated by Django 3.1.7 on 2021-04-22 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0002_auto_20210420_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='NovaPoshtaCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=300, null=True)),
                ('source_region', models.CharField(blank=True, max_length=300, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'NovaPoshtaCity',
                'verbose_name_plural': 'NovaPoshtaCities',
            },
        ),
        migrations.CreateModel(
            name='NovaPoshtaRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=300, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'NovaPoshtaRegion',
                'verbose_name_plural': 'NovaPoshtaRegions',
            },
        ),
        migrations.CreateModel(
            name='NovaPoshtaStreet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=300, null=True)),
                ('source_city', models.CharField(blank=True, max_length=300, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('street_type', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping.novaposhtacity')),
            ],
            options={
                'verbose_name': 'NovaPoshtaStreet',
                'verbose_name_plural': 'NovaPoshtaStreets',
            },
        ),
        migrations.AddField(
            model_name='novaposhtacity',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping.novaposhtaregion'),
        ),
        migrations.CreateModel(
            name='NovaPoshtaBranche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=300, null=True)),
                ('source_city', models.CharField(blank=True, max_length=300, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('branche_type', models.CharField(blank=True, max_length=300, null=True)),
                ('max_weight_place', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('max_weight', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping.novaposhtacity')),
            ],
            options={
                'verbose_name': 'NovaPoshtaBranche',
                'verbose_name_plural': 'NovaPoshtaBranches',
            },
        ),
    ]
