from .models import SheetTemplate, CharacterSheet
from django import forms

template_form_examples = {

    "available_classes": 
    ('Define what classes options players will have. Ex: ["warrior", "mage"]'),
    "available_races":
    ('Define what races options players will have. Ex: ["elf", "dwarf"]'),
    "background": 
    ('Define what are the constitutes of a character\'s background. Ex: ["ideals", "personality"]'),

    "attributes": ('Define the attributes of a character. Ex: ["strength", "dexterity"]'),

    "stats": ('Define the stats of a character. Ex: {"hp": 0, "dimension": "", "poisoned": false}'),

    "weapon_template": 
    ('Define weapon attributes with default values.' 
    + '\nEx.: {"name": "", "type": "", "price": 0, "damage": 0, "broken": False, "effects": []}'),
    "equipment_template": 
    ('Define equipment attributes with default values.'
     + '\nEx.: {"name": "", "type": "", "price": 0, "armor": 0, "effects": []}'),
    "consumable_template":
    ('Define consumable attributes with default values here.' 
     + '\nEx.: {"name": "", "type": "", "price": 0, "effects": []}'),
    "quest_item_template": 
    ('Define quest items attributes with default values here.' 
     + '\nEx.: {"name": "", "type": "", "description": ""}'),
}

# Returns a dict of error messages str (input) -> list[str];
def validate_sheet_template_form_input_content(form_cleaned_data):

    fields_error_messages = {}

    # Validate available_classes, available_races, background, and attributes content;
    error_messages = check_is_nonempty_strings_array(form_cleaned_data["available_classes"])
    if len(error_messages) != 0:
        fields_error_messages["available_classes"] = error_messages
    error_messages = check_is_nonempty_strings_array(form_cleaned_data["available_races"])
    if len(error_messages) != 0:
        fields_error_messages["available_races"] = error_messages
    error_messages = check_is_nonempty_strings_array(form_cleaned_data["background"])
    if len(error_messages) != 0:
        fields_error_messages["background"] = error_messages
    error_messages = check_is_nonempty_strings_array(form_cleaned_data["attributes"])
    if len(error_messages) != 0:
        fields_error_messages["attributes"] = error_messages

    # Validate stats content;
    error_messages = check_is_valid_stats_template(form_cleaned_data["stats"])
    if len(error_messages) != 0:
        fields_error_messages["stats"] = error_messages

    # Validate item templates content;
    error_messages =  check_is_valid_item_template(form_cleaned_data["weapon_template"])
    if len(error_messages) != 0:
        fields_error_messages["weapon_template"] = error_messages
    error_messages = check_is_valid_item_template(form_cleaned_data["equipment_template"])
    if len(error_messages) != 0:
        fields_error_messages["equipment_template"] = error_messages
    error_messages = check_is_valid_item_template(form_cleaned_data["consumable_template"])
    if len(error_messages) != 0:
        fields_error_messages["consumable_template"] = error_messages
    error_messages = check_is_valid_item_template(form_cleaned_data["quest_item_template"])
    if len(error_messages) != 0:
        fields_error_messages["quest_item_template"] = error_messages

    return fields_error_messages

# For available classes, races, background and attributes;
# Returns list of error messages for input;
def check_is_nonempty_strings_array(python_from_json) -> bool:

    error_messages = []

    if not isinstance(python_from_json, list):
        error_messages.append("Input is not a valid array")
        return error_messages

    for i, value in enumerate(python_from_json):
        if not isinstance(value, str):
            error_messages.append(f"{i + 1}-th item ({value}) is not a string")
            continue
        if len(value) == 0:
            error_messages.append(f"{i + 1}-th item is empty")

    return error_messages

# For stats;
# Returns list of error messages for input;
def check_is_valid_stats_template(python_from_json) -> bool:

    error_messages = []

    if not isinstance(python_from_json, dict):
        error_messages.append("Input is not a json object")
        return error_messages
    
    for i, (k, v) in enumerate(python_from_json.items()):

        if k is None:
            error_messages.append(f"Key {k} is not a string")
            continue

        if not isinstance(k, str):
            error_messages.append(f"Key {k} is not a string")
        elif k == "":
            error_messages.append(f"{i + 1}-th key is empty")
            continue

        if isinstance(v, str):
            if v != "":
                error_messages.append(f"String value of {k} should be empty")
        elif isinstance(v, bool):
            if v != False:
                error_messages.append(f"Boolean value of {k} should be false")
        elif isinstance(v, int):
            if v != 0:
                error_messages.append(f"Number value of {k} should be 0")
        else:
            error_messages.append(f"Value of {k} should be string, number or boolean")

    return error_messages

# For weapons, equipments, consumables and quest items;
# Returns list of error messages for input;
def check_is_valid_item_template(python_from_json) -> bool:

    error_messages = []

    if not isinstance(python_from_json, dict):
        error_messages.append("Input is not a json object")
        return error_messages
    
    for i, (k, v) in enumerate(python_from_json.items()):

        if k is None:
            error_messages.append(f"Key {k} is not a string")
            continue

        if not isinstance(k, str):
            error_messages.append(f"Key {k} is not a string")
        elif k == "":
            error_messages.append(f"{i + 1}-th key is empty")
            continue

        if isinstance(v, str):
            if v != "":
                error_messages.append(f"String value of {k} should be empty")
        elif isinstance(v, bool):
            if v != False:
                error_messages.append(f"Boolean value of {k} should be false")
        elif isinstance(v, int):
            if v != 0:
                error_messages.append(f"Number value of {k} should be 0")
        elif isinstance(v, list): 
            if v != []:
                error_messages.append(f"Array value of {k} should have no elements")
        else:
            error_messages.append(f"Value of {k} should be string, number, boolean or array")

    return error_messages

class SheetTemplateForm(forms.ModelForm):

    class Meta:
        model = SheetTemplate
        exclude = ["sheet_template_owner", "creation_date"]

        widgets = {
            field: forms.Textarea(attrs={"placeholder": placeholder, "rows": 4})
            for field, placeholder in template_form_examples.items()
        }

# Danger: model basic 4 fields hardcoded here;
def generate_character_sheet_form_inputs(template_object):
    return None

# Returns a dict of error messages str (input) -> list[str];
def validate_character_sheet_form_input_content(template_object, form_cleaned_data):
    return {}

class CharacterSheetFormExceptSheetTemplate(forms.Form):

    name = forms.CharField(max_length=200, initial="")
    experience = forms.IntegerField(initial=0)
    level = forms.IntegerField(initial=0)
    gold = forms.IntegerField(initial=0)