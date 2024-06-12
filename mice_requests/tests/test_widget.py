from django.test import TestCase
from django.utils.safestring import mark_safe

from mice_requests.forms import ReadOnlyMiceField


class ReadOnlyMiceFieldTestCase(TestCase):
    def setUp(self):
        self.widget = ReadOnlyMiceField()

    def test_render_with_single_value(self):
        rendered = self.widget.render("mice", ["mouse1"])
        expected_html = mark_safe(
            '<input type="text" name="mice" value="mouse1" id="id_mice_0">'
        )
        self.assertHTMLEqual(rendered, expected_html)

    def test_render_with_multiple_values(self):
        rendered = self.widget.render("mice", ["mouse1", "mouse2", "mouse3"])
        expected_html = mark_safe(
            "\n".join(
                [
                    '<input type="text" name="mice" value="mouse1" id="id_mice_0">',
                    '<input type="text" name="mice" value="mouse2" id="id_mice_1">',
                    '<input type="text" name="mice" value="mouse3" id="id_mice_2">',
                ]
            )
        )
        self.assertHTMLEqual(rendered, expected_html)

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
