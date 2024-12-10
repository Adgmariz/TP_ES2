from django.test import TestCase

from .forms import check_is_nonempty_strings_array
from .forms import check_is_valid_stats_template
from .forms import check_is_valid_item_template

from .forms import validate_sheet_template_form_input_content

class SheetTemplateValidationTests(TestCase):

    def test_check_is_nonempty_strings_array___not_array(self):

        data = {}
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(["Input is not a valid array"], error_messages)

        data = ""
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(["Input is not a valid array"], error_messages)

    def test_check_is_nonempty_strings_array___with_empty_str_elements(self):

        data = [""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(["Array's 1-th item is empty"], error_messages)

        data = ["taetae", "weaw", "ew", "ewa", ""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(["Array's 5-th item is empty"], error_messages)

        data = ["", "awea", "", "rrawra", ""]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual(["Array's 1-th item is empty", 
                          "Array's 3-th item is empty", 
                          "Array's 5-th item is empty"], error_messages)

    def test_check_is_nonempty_strings_array___with_nonstr_elements(self):

        data = [1]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual([f"Array's 1-th item ({data[0]}) is not a string"], error_messages)

        data = ["aeaw", "kok", "awr", "eaw", {}]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual([f"Array's 5-th item ({data[4]}) is not a string"], error_messages)

        data = [True, "kok", {}, "eaw", 0]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual([f"Array's 1-th item ({data[0]}) is not a string", 
                          f"Array's 3-th item ({data[2]}) is not a string",
                          f"Array's 5-th item ({data[4]}) is not a string"], error_messages)

    def test_check_is_nonempty_strings_array___valid_array(self):

        data = ["weaw", "aweawe", "geag", "awa", "fawfaw", "awe"]
        error_messages = check_is_nonempty_strings_array(data)
        self.assertEqual([], error_messages)