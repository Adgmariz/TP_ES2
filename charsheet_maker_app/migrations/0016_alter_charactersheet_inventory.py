# Generated by Django 5.1.3 on 2025-01-03 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charsheet_maker_app', '0015_alter_charactersheet_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactersheet',
            name='inventory',
            field=models.JSONField(default=list),
        ),
    ]