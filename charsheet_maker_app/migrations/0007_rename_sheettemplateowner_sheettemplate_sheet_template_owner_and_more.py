# Generated by Django 5.1.3 on 2024-12-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charsheet_maker_app', '0006_charactersheet_creation_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sheettemplate',
            old_name='sheetTemplateOwner',
            new_name='sheet_template_owner',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charAttributes',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charAvailableClasses',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charAvailableRaces',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charBackground',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charConsumableTemplate',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charEquipmentTemplate',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charQuestItemTemplate',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charStatuses',
        ),
        migrations.RemoveField(
            model_name='sheettemplate',
            name='charWeaponTemplate',
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='attributes',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='available_classes',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='available_races',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='background',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='consumable_template',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='equipment_template',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='quest_item_template',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='statuses',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sheettemplate',
            name='weapon_template',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='charactersheet',
            name='template_instance',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='sheettemplate',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date was created'),
        ),
    ]
