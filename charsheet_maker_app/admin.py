from django.contrib import admin

# Register your models here.
from .models import SheetTemplate, CharacterSheet

admin.site.register(SheetTemplate)

admin.site.register(CharacterSheet)