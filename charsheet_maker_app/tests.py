from django.test import TestCase

from .forms import check_is_nonempty_strings_array
from .forms import check_is_valid_stats_template
from .forms import check_is_valid_item_template

from .forms import validate_sheet_template_form_input_content

# Unit tests for testing the data validation for sheet template creation form data;
# Ex.: The "attributes" field should be only a list of strings;
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

from django.test import Client
from django.contrib.auth.models import User
from charsheet_maker_app.models import SheetTemplate
from charsheet_maker_app.models import CharacterSheet
from django.urls import reverse

class IndexViewTests(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_not_logged_users_get_redirected_to_django_auth_app_from_which_they_would_be_redirected_to_their_template_list(self):

        response = self.client.get(reverse("charsheet_maker_app:index"))

        self.assertRedirects(response, 
                             f"/accounts/login/?next={reverse("charsheet_maker_app:index")}")

    def test_user_logged_in_gets_his_sheet_template_link_list(self):

        user = User.objects.create_user(username="test user",
                                        password="12345")
        sheet_templates = [
            SheetTemplate.objects.create(
                sheet_template_owner=user,
                template_name=f"test template {i}",
                available_classes=["warrior", "mage"],
                available_races=["orc", "human"],
                background=["ideals", "personality"],
                attributes=["strength", "dexterity"],
                stats={"hp": 0, "mana": 0, "asleep": False},
                weapon_template={"name": "", "damage": 0, "broken": False},
                equipment_template={"name": "", "armor": 0},
                consumable_template={"name": "", "effects": []},
                quest_item_template={"name": "", "quest": "", "description": ""}
            ) for i in range(3)
        ]

        self.client.login(username="test user", password="12345")

        response = self.client.get(reverse("charsheet_maker_app:index"))

        self.assertContains(response, status_code=200, text="<title>CharSheetMaker - Templates</title>")
        
        # ========== Check if links for each template with their names are present ========== # 
        for i in range(3):
            self.assertContains(response, status_code=200, 
                                text=f"<a href=\"{reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_templates[i].id,))}\">" 
                                + f"{sheet_templates[i].template_name}</a>")
        
class SheetTemplateDetailViewTests(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_not_logged_users_get_redirected_to_django_auth_app_from_which_they_would_be_redirected_to_the_wanted_template_page(self):

        # dummy object necessary for template creation;
        user = User.objects.create_user(username="test user",
                                        password="12345")
        sheet_template = SheetTemplate.objects.create(
            sheet_template_owner=user,
            template_name="test template",
            available_classes=["warrior", "mage"],
            available_races=["orc", "human"],
            background=["ideals", "personality"],
            attributes=["strength", "dexterity"],
            stats={"hp": 0, "mana": 0, "asleep": False},
            weapon_template={"name": "", "damage": 0, "broken": False},
            equipment_template={"name": "", "armor": 0},
            consumable_template={"name": "", "effects": []},
            quest_item_template={"name": "", "quest": "", "description": ""}
        )

        response = self.client.get(reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_template.id,)))

        self.assertRedirects(response, 
                             f"/accounts/login/?next={reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_template.id, ))}")

    def test_logged_users_that_do_not_own_the_template_get_response_forbidden(self):

        user = User.objects.create_user(username="test user",
                                        password="12345")
        sheet_template = SheetTemplate.objects.create(
            sheet_template_owner=user,
            template_name="test template",
            available_classes=["warrior", "mage"],
            available_races=["orc", "human"],
            background=["ideals", "personality"],
            attributes=["strength", "dexterity"],
            stats={"hp": 0, "mana": 0, "asleep": False},
            weapon_template={"name": "", "damage": 0, "broken": False},
            equipment_template={"name": "", "armor": 0},
            consumable_template={"name": "", "effects": []},
            quest_item_template={"name": "", "quest": "", "description": ""}
        )

        user2 = User.objects.create_user(username="test user 2",
                                        password="12345")

        self.client.login(username="test user 2", password="12345")

        response =  self.client.get(reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_template.id,)))

        self.assertEqual(response.status_code, 403)

    def test_sheet_template_detail_view_displays_correct_template_object_fields_and_its_types(self):

        user = User.objects.create_user(username="test user",
                                        password="12345")
        sheet_template = SheetTemplate.objects.create(
            sheet_template_owner=user,
            template_name="test template",
            available_classes=["warrior", "mage"],
            available_races=["orc", "human"],
            background=["ideals", "personality"],
            attributes=["strength", "dexterity"],
            stats={"hp": 0, "mana": 0, "asleep": False},
            weapon_template={"name": "", "damage": 0, "broken": False},
            equipment_template={"name": "", "armor": 0},
            consumable_template={"name": "", "effects": []},
            quest_item_template={"name": "", "quest": "", "description": ""}
        )

        # ========== User has to log in to view his template sheets ========== #
        self.client.login(username="test user", password="12345")

        response = self.client.get(reverse("charsheet_maker_app:sheet_template_detail", args=(sheet_template.id,)))

        self.assertEqual(response.status_code, 200)

        # ========== Check if correct page by title ========== #
        self.assertContains(response, text="<title>CharSheetMaker - Sheet template</title>", html=True)

        # ========== Check if correct template name in header ========== #
        self.assertContains(response, text=f"<h1>Sheet template {sheet_template.template_name}</h1>", html=True)

        # ========== Check if correct owner name ========== #
        self.assertContains(response, text=f"<p><strong>Owner:</strong> {user.username}</p>", html=True)

        # ========== Check default fields ========== #
        for field in ["Name", "Experience", "Level", "Gold"]:
            self.assertContains(response, text=f"<li>{field}</li>", html=True)

        # ========== Check custom fields ========== #

        # Classes;
        for ind, cls in enumerate(sheet_template.available_classes):
            self.assertContains(response, text=f"<li id=\"class-{ind}\">{cls}</li>", html=True)

        # Races;
        for ind, race in enumerate(sheet_template.available_races):
            self.assertContains(response, text=f"<li id=\"race-{ind}\">{race}</li>", html=True)

        # Background;
        for ind, background in enumerate(sheet_template.background):
            self.assertContains(response, text=f"<li id=\"background-{ind}\">{background}</li>", html=True)
        
        # Attributes;
        for ind, attr in enumerate(sheet_template.attributes):
            self.assertContains(response, text=f"<li id=\"attribute-{ind}\">{attr}</li>", html=True)

        def get_field_type_displayed(value):

            if value == "":
                return "text"
            elif isinstance(value, bool):
                return "true or false"
            elif value == 0:
                return "number"
            else:
                return "list"

        # Stats;
        for ind, (attr, default_value) in enumerate(sheet_template.stats.items()):
            self.assertContains(response, text=f"<li id=\"stat-{ind}\">{attr} - {get_field_type_displayed(default_value)}</li>", html=True)

        # Weapon definition;
        for ind, (attr, default_value) in enumerate(sheet_template.weapon_template.items()):
            self.assertContains(response, text=f"<li id=\"weapon-attr-{ind}\">{attr} - {get_field_type_displayed(default_value)}</li>", html=True)

        # Equipment definition;
        for ind, (attr, default_value) in enumerate(sheet_template.equipment_template.items()):
            self.assertContains(response, text=f"<li id=\"equipment-attr-{ind}\">{attr} - {get_field_type_displayed(default_value)}</li>", html=True)

        # Consumable definition;
        for ind, (attr, default_value) in enumerate(sheet_template.consumable_template.items()):
            self.assertContains(response, text=f"<li id=\"consumable-attr-{ind}\">{attr} - {get_field_type_displayed(default_value)}</li>", html=True)

        # Quest Item definition;
        for ind, (attr, default_value) in enumerate(sheet_template.quest_item_template.items()):
            self.assertContains(response, text=f"<li id=\"quest-item-attr-{ind}\">{attr} - {get_field_type_displayed(default_value)}</li>", html=True)

class CharacterSheetDetailViewTests(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_character_sheet_detail_view_displays_correct_sheet_object_fields_and_base_template_link(self):

        user = User.objects.create_user(username="test user",
                                        password="12345")
        sheet_template = SheetTemplate.objects.create(
            sheet_template_owner=user,
            template_name="test template",
            available_classes=["warrior", "mage"],
            available_races=["orc", "human"],
            background=["ideals", "personality"],
            attributes=["strength", "dexterity"],
            stats={"hp": 0, "mana": 0, "asleep": False},
            weapon_template={"name": "", "damage": 0, "broken": False},
            equipment_template={"name": "", "armor": 0},
            consumable_template={"name": "", "effects": []},
            quest_item_template={"name": "", "quest": "", "description": ""}
        )
        character_sheet = CharacterSheet.objects.create(
            template=sheet_template,
            name="test character",
            experience=100,
            level=3,
            gold=50,
            char_class="warrior",
            race="orc",
            background={"ideals": "dying in battle is honorous", "personality": "likes to fight"},
            attributes={"strength": 15, "dexterity": 10},
            stats={"hp": 100, "mana": 30, "asleep": True},
            weapons={0: {"name": "sword", "damage": 10, "broken": False}, 1: {"name": "spear", "damage": 5, "broken": True}},
            equipments={3: {"name": "helmet", "armor": 3}, 1: {"name": "chest", "armor": 5}, 2: {"name": "boots", "armor": 2}},
            consumables={1: {"name": "super potion", "effects": ["restores 100 hp", "restores 100 mana"]}},
            quest_items={0: {"name": "mysterious book", "quest": "prologue", "description": "this book holds secrets"}}
        )

        # ========== User has to log in to view his sheets ========== #
        self.client.login(username="test user", password="12345")

        response = self.client.get(reverse("charsheet_maker_app:character_sheet_detail", args=(character_sheet.id,)))

        self.assertEqual(response.status_code, 200)

        # ========== Check if correct page by title ========== #
        self.assertContains(response, text="<title>CharSheetMaker - Character Sheet</title>", html=True)

        # ========== Check if correct character name in header ========== #
        self.assertContains(response, text=f"<h1>{character_sheet.name}'s Sheet</h1>", html=True)

        # ========== Check if correct owner name ========== #
        self.assertContains(response, text=f"<p><strong>Owner:</strong> {user.username}</p>", html=True)

        # ========== Check character info ========== #
        self.assertContains(response, text=f'<input type="text" name="name" value="{character_sheet.name}"', html=False)
        self.assertContains(response, text=f'<input type="number" name="experience" value="{character_sheet.experience}"', html=False)
        self.assertContains(response, text=f'<input type="number" name="level" value="{character_sheet.level}"', html=False)
        self.assertContains(response, text=f'<input type="number" name="gold" value="{character_sheet.gold}"', html=False)

        # Character class option is selected, others not;
        self.assertContains(response, text=f'<option value="{character_sheet.char_class}" selected>{character_sheet.char_class}</option>', html=True)
        for c in sheet_template.available_classes:
            if c != character_sheet.char_class:
                self.assertContains(response, text=f'<option value="{c}">{c}</option>', html=True)

        # Character race option is selected, others not;
        self.assertContains(response, text=f'<option value="{character_sheet.race}" selected>{character_sheet.race}</option>', html=True)
        for c in sheet_template.available_races:
            if c != character_sheet.race:
                self.assertContains(response, text=f'<option value="{c}">{c}</option>', html=True)

        # Background;
        for name, value in character_sheet.background.items():
            self.assertContains(response, text=f'<input type="text" name="background-{name}" value="{value}"', html=False)

        # Attributes;
        for name, value in character_sheet.attributes.items():
            self.assertContains(response, text=f'<input type="number" name="attribute-{name}" value="{value}"', html=False)

        def get_html_input_type(value):

            if isinstance(value, str):
                return "text"
            elif isinstance(value, bool):
                return "checkbox"
            elif isinstance(value, int):
                return "number"
            else:
                return "text"

        # Stats;
        for name, value in character_sheet.stats.items():
            html_input_type = get_html_input_type(value)
            if html_input_type == "checkbox":
                self.assertContains(response, text=f'<input type="{html_input_type}" name="stat-{name}" id="id_stat-{name}" {"checked" if value else ""}')
            else:
                self.assertContains(response, text=f'<input type="{html_input_type}" name="stat-{name}" value="{value}"')

        # ========== Check character inventory ========== #

        def get_item_opening_html_list_tag(item_id, item_type):
            return f'<ul id="{item_type}-{item_id}">'       

        def get_item_attribute_rendered_as_html_list_item(item_id, item_type, attribute, value):
            return f'<li id="{item_type}-{item_id}-{attribute}">{attribute} - {value}</li>'

        # Weapons;
        for id, weapon in character_sheet.weapons.items():
            self.assertContains(response, 
                                text=get_item_opening_html_list_tag(item_id=id, item_type="weapon"),
                                html=False)
            for weapon_attr, val in weapon.items():
                self.assertContains(response, 
                                    text=get_item_attribute_rendered_as_html_list_item(
                                            item_id=id, item_type="weapon", attribute=weapon_attr, value=val
                                        ), 
                                    html=True)

        # Equipments;
        for id, equipment in character_sheet.equipments.items():
            self.assertContains(response, 
                                text=get_item_opening_html_list_tag(item_id=id, item_type="equipment"),
                                html=False)
            for equipment_attr, val in equipment.items():
                self.assertContains(response, 
                                    text=get_item_attribute_rendered_as_html_list_item(
                                            item_id=id, item_type="equipment", attribute=equipment_attr, value=val
                                        ), 
                                    html=True)

        # Consumables;
        for id, consumable in character_sheet.consumables.items():
            self.assertContains(response, 
                                text=get_item_opening_html_list_tag(item_id=id, item_type="consumable"),
                                html=False)
            for consumable_attr, val in consumable.items():
                self.assertContains(response, 
                                    text=get_item_attribute_rendered_as_html_list_item(
                                            item_id=id, item_type="consumable", attribute=consumable_attr, value=val
                                        ), 
                                    html=True)

        # Quest Items;
        for id, quest_item in character_sheet.quest_items.items():
            self.assertContains(response, 
                                text=get_item_opening_html_list_tag(item_id=id, item_type="quest_item"),
                                html=False)
            for quest_item_attr, val in quest_item.items():
                self.assertContains(response, 
                                    text=get_item_attribute_rendered_as_html_list_item(
                                            item_id=id, item_type="quest_item", attribute=quest_item_attr, value=val
                                        ), 
                                    html=True)