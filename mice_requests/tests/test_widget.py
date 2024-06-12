from django.test import TestCase

from mice_requests.forms import ReadOnlyMiceField
from mice_requests.tests.utils import get_hidden_input_value


class ReadOnlyMiceFieldTestCase(TestCase):
    def setUp(self):
        self.widget = ReadOnlyMiceField()

    def test_render_hidden_input_with_single_value(self):
        rendered = self.widget.render("mice", ["mouse1"])
        actual_value = get_hidden_input_value(rendered, "mice")
        self.assertEqual(actual_value, "mouse1")

    def test_render_with_multiple_values(self):
        expected_values = ["mouse1", "mouse2", "mouse3"]
        rendered = self.widget.render("mice", expected_values)
        actual_values = [
            get_hidden_input_value(rendered, "mice", index=i)
            for i in range(len(expected_values))
        ]
        self.assertEqual(actual_values, expected_values)

    def test_render_with_none(self):
        rendered = self.widget.render("mice", None)
        self.assertEqual(rendered, "")

    def test_value_from_datadict_with_querydict(self):
        value = self.widget.value_from_datadict(
            {"mice": ["mouse1", "mouse2"]}, {}, "mice"
        )
        self.assertEqual(value, ["mouse1", "mouse2"])

    def test_value_from_datadict_with_dict(self):
        value = self.widget.value_from_datadict(
            {"mice": ["mouse1", "mouse2"]}, {}, "mice"
        )
        self.assertEqual(value, ["mouse1", "mouse2"])

    def test_value_from_datadict_with_none(self):
        value = self.widget.value_from_datadict({}, {}, "mice")
        self.assertEqual(value, [])

    def test_value_from_datadict_with_single_value(self):
        value = self.widget.value_from_datadict({"mice": "mouse1"}, {}, "mice")
        self.assertEqual(value, ["mouse1"])
