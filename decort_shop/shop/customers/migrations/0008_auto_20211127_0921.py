# Generated by Django 3.2.9 on 2021-11-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20211126_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerpointgps',
            options={'verbose_name': 'CustomerPointGPS', 'verbose_name_plural': 'CustomerPointGPS'},
        ),
        migrations.AddField(
            model_name='customerpointgps',
            name='comments',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]