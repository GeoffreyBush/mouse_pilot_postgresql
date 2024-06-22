from django.http import HttpRequest
from django.test import TestCase

from mice_repository.models import Mouse
from mouse_pilot_postgresql.model_factories import MouseFactory, ProjectFactory
from projects.filters import ProjectFilter


class ProjectMouseFilterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = ProjectFactory()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(sex="M", earmark="TL"),
            MouseFactory(sex="F", earmark="TL"),
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
        )
        cls.project.mice.add(cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4)

    def test_empty_filter(self):
        filter_instance = ProjectFilter({}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs),
            [self.mouse1, self.mouse2, self.mouse3, self.mouse4],
        )

    def test_sex_filter(self):
        filter_instance = ProjectFilter({"sex": "M"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse3])

    def test_earmark_filter(self):
        filter_instance = ProjectFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])

    def test_combined_filters(self):
        filter_instance = ProjectFilter(
            {"sex": "M", "earmark": "TL"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse1])

    def test_no_matching_mice(self):
        filter_instance = ProjectFilter({"earmark": "TR"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [])

    def test_clear_after_filter(self):
        filter_instance = ProjectFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])
        filter_instance = ProjectFilter({"clear": ""}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs),
            [self.mouse1, self.mouse2, self.mouse3, self.mouse4],
        )

    def test_filter_replace_another_filter(self):
        filter_instance = ProjectFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])
        filter_instance = ProjectFilter({"sex": "F"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse2, self.mouse4])


class GetFilteredProjectMiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = ProjectFactory()
        cls.mouse1 = MouseFactory(project=cls.project, sex="M", earmark="TL")
        cls.mouse2 = MouseFactory(project=cls.project, sex="F", earmark="TR")

    def setUp(self):
        self.request = HttpRequest()

    def test_get_filtered_project_mice_without_search(self):
        result = ProjectFilter.get_filtered_project_mice(self.project, self.request)
        self.assertEqual(
            list(result),
            list(Mouse.objects.filter(project=self.project).order_by("_global_id")),
        )

    def test_get_filtered_project_mice_with_search(self):
        self.request.GET = {"search": "true", "sex": "M"}
        result = ProjectFilter.get_filtered_project_mice(self.project, self.request)
        self.assertEqual(list(result), [self.mouse1])


class GetFilterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = ProjectFactory()
        MouseFactory(project=cls.project, earmark="TL")
        MouseFactory(project=cls.project, earmark="TR")

    def setUp(self):
        self.request = HttpRequest()

    def test_get_filter_form_without_search(self):
        result = ProjectFilter.get_filter_form(self.project, self.request)
        self.assertEqual(result.data, {})

    def test_get_filter_form_with_search(self):
        self.request.GET = {"search": "true", "sex": "M"}
        result = ProjectFilter.get_filter_form(self.project, self.request)
        self.assertEqual(result.data, {"search": "true", "sex": "M"})

    def test_get_filter_form_returns_projectfilter_instance(self):
        result = ProjectFilter.get_filter_form(self.project, self.request)
        self.assertIsInstance(result, ProjectFilter)
