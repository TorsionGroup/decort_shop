# Generated by Django 3.1.7 on 2021-04-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_delete_waitlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]