# Generated by Django 5.1.3 on 2025-01-03 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charsheet_maker_app', '0011_alter_sheettemplate_attributes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='charactersheet',
            name='inventory',
            field=models.JSONField(default=dict),
        ),
    ]
