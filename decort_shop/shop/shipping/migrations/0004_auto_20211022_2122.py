# Generated by Django 3.2.8 on 2021-10-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0003_auto_20210422_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novaposhtabranche',
            name='source',
        ),
        migrations.RemoveField(
            model_name='novaposhtabranche',
            name='source_city',
        ),
        migrations.RemoveField(
            model_name='novaposhtacity',
            name='source',
        ),
        migrations.RemoveField(
            model_name='novaposhtacity',
            name='source_region',
        ),
        migrations.RemoveField(
            model_name='novaposhtaregion',
            name='source',
        ),
        migrations.RemoveField(
            model_name='novaposhtastreet',
            name='source',
        ),
        migrations.RemoveField(
            model_name='novaposhtastreet',
            name='source_city',
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='city_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='latitude',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='longitude',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='name_ru',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='wh_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtabranche',
            name='wh_type_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtacity',
            name='area_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtacity',
            name='city_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtacity',
            name='city_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtacity',
            name='name_ru',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtaregion',
            name='area_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtaregion',
            name='center',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtaregion',
            name='center_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtastreet',
            name='city_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtastreet',
            name='street_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='novaposhtastreet',
            name='street_type_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
