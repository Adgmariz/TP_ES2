from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class SheetTemplate(models.Model):

    sheetTemplateOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField("date was created")

    # ========== CHARACTER CUSTOMIZATION OPTIONS ========== #

    # JSON format example for the next JSON fields:
    # {
    #   "strenght": 0, "dexterity": 0, "carisma": 0
    # }
    # (fields are only initialized for type declaration)
    # (Some values could be suggested at time of template creation)

    # warrior, mage, ... (Empty String - to store description, etc)
    charAvailableClasses = models.JSONField()
    # Same as above.
    charAvailableRaces = models.JSONField()
    # strenght, dexterity ... (Integer)
    charAttributes = models.JSONField()
    # hp, armor, effects ... (Integer or Boolean)
    charStatuses = models.JSONField()
    # personality, ideals, ... (Empty String)
    charBackground = models.JSONField()

    # ========== INVENTORY DEFINITION ========== #

    # name, type, status?, price?, damage?, effect?, ... 
    # (Integer, Boolean, Empty String, Array, ...)
    charWeaponTemplate = models.JSONField()

    charEquipmentTemplate = models.JSONField()

    charConsumableTemplate = models.JSONField()

    charQuestItemTemplate = models.JSONField()

# Created from a POST using some of the user's templates;
class CharacterSheet(models.Model):

    template = models.ForeignKey(SheetTemplate, on_delete=models.CASCADE)

    creation_date = models.DateTimeField("date was created", default=now)

    # Basic components (should be default in template creation);
    name = models.CharField(max_length=200, default="")
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)

    # Based on SheetTemplate format.
    # Some values can be change, e.g. Inventory, while Race for example, cannot;
    template_instance = models.JSONField()