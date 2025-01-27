# Generated by Django 5.1.3 on 2024-12-09 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charsheet_maker_app', '0009_alter_charactersheet_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheettemplate',
            name='attributes',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='sheettemplate',
            name='available_classes',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='sheettemplate',
            name='available_races',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='sheettemplate',
            name='background',
            field=models.CharField(max_length=500),
        ),
    ]
