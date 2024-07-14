from django.http import HttpRequest
from django.test import TestCase
from datetime import date, timedelta

from main.filters import MouseFilter
from main.model_factories import MouseFactory
from mice_repository.models import Mouse


class MouseFilterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(sex="M", earmark="TL", dob=date.today() - timedelta(days=10)),
            MouseFactory(sex="F", earmark="TL", dob=date.today() - timedelta(days=20)),
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
        )

    def test_empty_filter(self):
        filter_instance = MouseFilter({}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs),
            [self.mouse1, self.mouse2, self.mouse3, self.mouse4],
        )

    def test_sex_filter(self):
        filter_instance = MouseFilter({"sex": "M"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse3])

    def test_earmark_filter(self):
        filter_instance = MouseFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])

    def test_min_age_filter(self):
        filter_instance = MouseFilter({"min_age": "5"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])

    def test_max_age_filter(self):
        filter_instance = MouseFilter({"max_age": "15"}, queryset=Mouse.objects.all())
        print(filter_instance.qs)
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse3, self.mouse4])

    def test_min_and_max_age_filter_combined(self):
        filter_instance = MouseFilter(
            {"min_age": "5", "max_age": "15"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse1])

    def test_combined_filters(self):
        filter_instance = MouseFilter(
            {"sex": "M", "earmark": "TL"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse1])

    def test_no_matching_mice(self):
        filter_instance = MouseFilter({"earmark": "TR"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [])

    def test_clear_after_filter(self):
        filter_instance = MouseFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])
        filter_instance = MouseFilter({"clear": ""}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs),
            [self.mouse1, self.mouse2, self.mouse3, self.mouse4],
        )

    def test_filter_replace_another_filter(self):
        filter_instance = MouseFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])
        filter_instance = MouseFilter({"sex": "F"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse2, self.mouse4])


class GetFilteredMiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mouse1 = MouseFactory(sex="M")
        cls.mouse2 = MouseFactory(sex="F")
        cls.mice_qs = Mouse.objects.all()

    def setUp(self):
        self.request = HttpRequest()

    def test_get_filtered_mice_without_search(self):
        result = MouseFilter.get_filtered_mice(self.mice_qs, self.request)
        self.assertEqual(list(result), list(Mouse.objects.all()))

    def test_get_filtered_mice_with_search(self):
        self.request.GET = {"search": "true", "sex": "M"}
        result = MouseFilter.get_filtered_mice(self.mice_qs, self.request)
        self.assertEqual(list(result), [self.mouse1])


class GetFilterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MouseFactory.create_batch(2)
        cls.mice_qs = Mouse.objects.all()

    def setUp(self):
        self.request = HttpRequest()

    def test_get_filter_form_without_search(self):
        result = MouseFilter.get_filter_form(self.mice_qs, self.request)
        self.assertEqual(result.data, {})

    def test_get_filter_form_with_search(self):
        self.request.GET = {"search": "true", "sex": "M"}
        result = MouseFilter.get_filter_form(self.mice_qs, self.request)
        self.assertEqual(result.data, {"search": "true", "sex": "M"})

    def test_get_filter_form_returns_instance(self):
        result = MouseFilter.get_filter_form(self.mice_qs, self.request)
        self.assertIsInstance(result, MouseFilter)
