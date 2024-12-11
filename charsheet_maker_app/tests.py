from django.test import TestCase

from .forms import check_is_nonempty_strings_array
from .forms import check_is_valid_stats_template
from .forms import check_is_valid_item_template

from .forms import validate_sheet_template_form_input_content

class SheetTemplateValidationTests(TestCase):

    def test_check_is_nonempty_strings_array___not_array(self):

        data = {}
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, ["Input is not a valid array"])

        data = ""
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, ["Input is not a valid array"])

    def test_check_is_nonempty_strings_array___with_empty_str_elements(self):

        data = [""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, ["1-th item is empty"])

        data = ["strenght", "dexterity", "inteligence", "carisma", ""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, ["5-th item is empty"])

        data = ["", "dexterity", "", "carisma", ""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, ["1-th item is empty", 
                                          "3-th item is empty", 
                                          "5-th item is empty"])

    def test_check_is_nonempty_strings_array___with_nonstr_elements(self):

        data = [1]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, [f"1-th item ({data[0]}) is not a string"])

        data = ["strenght", "dexterity", "inteligence", "carisma", {}]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, [f"5-th item ({data[4]}) is not a string"])

        data = [True, "dexterity", {}, "carisma", 0]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, [f"1-th item ({data[0]}) is not a string", 
                                          f"3-th item ({data[2]}) is not a string",
                                          f"5-th item ({data[4]}) is not a string"])

    def test_check_is_nonempty_strings_array___valid_array(self):

        data = ["strenght", "dexterity", "inteligence", "carisma", "faith"]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(error_messages, [])



    def test_check_is_valid_stats_template__not_json_object(self):

        data = []
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Input is not a json object"])

        data = ""
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Input is not a json object"])

    def test_check_is_valid_stats_template__with_empty_str_keys(self):

        data = {"": 0}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["1-th key is empty"])

        data = {"hp": 0, "exp": 0, "poisoned": False, "stunned": False, "": 0}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["5-th key is empty"])

        # dictionaries do not support repeated keys;
        data = {"": 0, "exp": 0, "": False, "stunned": False, "": 0}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["1-th key is empty"])

    def test_check_is_valid_stats_template__with_nonstr_keys(self):
        
        data = {1: ""}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Key 1 is not a string"])

        data = {"hp": 0, "exp": 0, "poisoned": False, "stunned": False, 5: 0}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Key 5 is not a string"])

        data = {1: 0, "exp": 0, 3: False, "stunned": False, 5: 0}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Key 1 is not a string", 
                                          "Key 3 is not a string",
                                          "Key 5 is not a string"])

    def test_check_is_valid_stats_template__with_non_valid_value_types(self):

        data = {"hp": []}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Value of hp should be string, number or boolean"])

        data = {"hp": 0, "exp": 0, "poisoned": None}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Value of poisoned should be string, number or boolean"])

        data = {"hp": [], "exp": 0, "poisoned": {}}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Value of hp should be string, number or boolean", 
                                          "Value of poisoned should be string, number or boolean"])

    def test_check_is_valid_stats_template__with_non_default_values(self):

        data = {"dimension": "overworld"}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["String value of dimension should be empty"])

        data = {"dimension": "", "hp": 0, "exp": 0, "poisoned": -1}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["Number value of poisoned should be 0"])

        data = {"dimension": "overworld", "hp": 0, "exp": 0, "poisoned": -1, "stunned": True}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, ["String value of dimension should be empty", 
                                          "Number value of poisoned should be 0",
                                          "Boolean value of stunned should be false"])

    def test_check_is_valid_stats_template__with_valid_object(self):
        
        data = {"dimension": "", "hp": 0, "exp": 0, "poisoned": False, "stunned": False}
        error_messages = check_is_valid_stats_template(data)
        self.assertEqual(error_messages, [])

    

    def test_check_is_valid_item_template__not_json_object(self):

        data = []
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Input is not a json object"])

        data = ""
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Input is not a json object"])

    def test_check_is_valid_item_template__with_empty_str_keys(self):

        data = {"": 0}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["1-th key is empty"])

        data = {"name": "", "type": "", "effects": [], "description": "", "": 0}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["5-th key is empty"])

        # dictionaries do not support repeated keys;
        data = {"": "", "type": "", "": [], "description": "", "": 0}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["1-th key is empty"])

    def test_check_is_valid_item_template__with_nonstr_keys(self):
        
        data = {1: ""}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Key 1 is not a string"])

        data = {"name": "", "type": "", "effects": [], "description": "", 5: 0}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Key 5 is not a string"])

        data = {1: "", "type": "", 3: [], "description": "", 5: 0}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Key 1 is not a string", 
                                          "Key 3 is not a string",
                                          "Key 5 is not a string"])

    def test_check_is_valid_item_template__with_non_valid_value_types(self):

        data = {"name": None}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Value of name should be string, number, boolean or array"])

        data = {"name": 0, "type": 0, "effects": None}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Value of effects should be string, number, boolean or array"])

        data = {"hp": None, "exp": 0, "effects": {}}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Value of hp should be string, number, boolean or array", 
                          "Value of effects should be string, number, boolean or array"])

    def test_check_is_valid_item_template__with_non_default_values(self):
        
        data = {"name": "name"}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["String value of name should be empty"])

        data = {"name": "", "type": "", "effects": ["bleed", "stun"]}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["Array value of effects should have no elements"])

        data = {"name": "name", "type": "", "effects": ["bleed", "stun"], "description": "", "price": 1000, "broken": True}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, ["String value of name should be empty", 
                                          "Array value of effects should have no elements",
                                          "Number value of price should be 0",
                                          "Boolean value of broken should be false"])

    def test_check_is_valid_item_template__with_valid_object(self):

        data = {"name": "", "type": "", "effects": [], "description": "", "price": 0, "broken": False}
        error_messages = check_is_valid_item_template(data)
        self.assertEqual(error_messages, [])



    def test_validate_sheet_template_form_input_content__one_error_each_field(self):

        form_cleaned_data = {
            "available_classes": [""],
            "available_races": [1],
            "background": [False],
            "attributes": 1,
            "stats": {"": "", 1: ""},
            "weapon_template": {"": 1},
            "equipment_template": {None: 1},
            "consumable_template": {False: 1},
            "quest_item_template": [],
        }
        fields_error_messages = validate_sheet_template_form_input_content(form_cleaned_data)
        
        self.assertEqual(["1-th item is empty"], fields_error_messages["available_classes"])
        
        self.assertEqual(["1-th item (1) is not a string"], fields_error_messages["available_races"])
        
        self.assertEqual(["1-th item (False) is not a string"], fields_error_messages["background"])
        
        self.assertEqual(["Input is not a valid array"], fields_error_messages["attributes"])
        
        self.assertEqual(["1-th key is empty", "Key 1 is not a string"], fields_error_messages["stats"])
        
        self.assertEqual(["1-th key is empty"], fields_error_messages["weapon_template"])
        
        self.assertEqual(["Key None is not a string"], fields_error_messages["equipment_template"])
        
        self.assertEqual(["Key False is not a string", 
                          "Number value of False should be 0"], 
                          fields_error_messages["consumable_template"])
        
        self.assertEqual(["Input is not a json object"], fields_error_messages["quest_item_template"])

    def test_validate_sheet_template_form_input_content__valid_content(self):
        
        form_cleaned_data = {
            "available_classes": ["warrior", "mage"],
            "available_races": ["nord", "dark elf"],
            "background": ["origin", "objective"],
            "attributes": ["one-handed combat", "archery"],
            "stats": {"dimension": "", "hp": 0, "stunned": False},
            "weapon_template": {"name": "", "type": "", "damage": 0, "broken": False, "effects": []},
            "equipment_template": {"name": "", "armor": 0, "effects": []},
            "consumable_template": {"name": "", "price": 0, "effects": []},
            "quest_item_template": {"name": "", "description": ""},
        }
        fields_error_messages = validate_sheet_template_form_input_content(form_cleaned_data)
        self.assertEqual(fields_error_messages, {})