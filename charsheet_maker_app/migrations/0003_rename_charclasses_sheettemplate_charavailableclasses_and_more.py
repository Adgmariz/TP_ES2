# Generated by Django 5.1.3 on 2024-11-27 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charsheet_maker_app', '0002_charactersheet_experience_charactersheet_gold_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sheettemplate',
            old_name='charClasses',
            new_name='charAvailableClasses',
        ),
        migrations.RenameField(
            model_name='sheettemplate',
            old_name='charRaces',
            new_name='charAvailableRaces',
        ),
    ]
