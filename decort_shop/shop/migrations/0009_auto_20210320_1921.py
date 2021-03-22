# Generated by Django 3.1.7 on 2021-03-20 17:21

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210320_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogcategory',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='catalogcategory',
            name='parent_source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='catalogcategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='shop.catalogcategory'),
        ),
    ]