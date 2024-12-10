from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class SheetTemplate(models.Model):

    sheet_template_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField("date was created", auto_now_add=True)

    # FIELDS BELOW ARE USED TO CREATE A TEMPLATE FORM;

    # ========== CHARACTER CUSTOMIZATION OPTIONS ========== #

    # String arrays;
    available_classes = models.JSONField(default=list)  # Ex.: ["warrior", "mage"]
    available_races = models.JSONField(default=list)    # Ex.: ["elf", "dwarf"]
    background = models.JSONField(default=list)         # Ex.: ["ideals", "personality"]
    attributes = models.JSONField(default=list)         # Ex.: ["strength", "dexterity"]

    # Types for the form to be generated are declared with default values. 
    # They should be empty string, 0 (int) or false (boolean);
    stats = models.JSONField(default=dict)           # Ex.: {"hp": 0, "dimension": "", "poisoned": false}

    # ========== INVENTORY DEFINITION ========== #

    # Values should be empty string, 0 (int), false (boolean) or empty array
    # Ex.: charWeaponTemplate = {"name": "", 
    #                            "type": "", 
    #                            "price": 0, 
    #                            "damage": 0,
    #                            "broken": False,
    #                            "effects": []}
    weapon_template = models.JSONField(default=dict)
    equipment_template = models.JSONField(default=dict)
    consumable_template = models.JSONField(default=dict)
    quest_item_template = models.JSONField(default=dict)

# Created from a POST using some of the user's templates;
class CharacterSheet(models.Model):

    template = models.ForeignKey(SheetTemplate, on_delete=models.CASCADE)

    creation_date = models.DateTimeField("date was created", auto_now_add=True)

    # Basic components (should be default in template creation);
    # Don't change (see generate_character_sheet_form_inputs in forms.py)
    name = models.CharField(max_length=200, default="")
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)

    template_instance = models.JSONField(default=dict)