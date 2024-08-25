from datetime import date, timedelta

from django.http import HttpRequest
from django.test import TestCase

from main.filters import MouseFilter
from main.model_factories import MouseFactory, StrainFactory, ProjectFactory
from mice_repository.models import Mouse
from strain.models import Strain



class MouseFilterSexTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
        )

    def test_sex_filter_m(self):
        filter_instance = MouseFilter({"sex": "M"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse3])

    def test_sex_filter_f(self):
        filter_instance = MouseFilter({"sex": "F"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse2, self.mouse4])

    def test_sex_filter_null(self):
        filter_instance = MouseFilter({"sex": None}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), list(Mouse.objects.all()))

class MouseFilterStrainTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.strain1, cls.strain2, cls.strain3 = (
            StrainFactory(strain_name="TestStrain1"), 
            StrainFactory(strain_name="TestStrain2"), 
            StrainFactory(strain_name="TestStrain3"),
        )
        cls.project = ProjectFactory(project_name="TestProject")
        cls.project.strains.add(cls.strain2, cls.strain3)
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(strain=cls.strain1),
            MouseFactory(strain=cls.strain2),
            MouseFactory(strain=cls.strain2),
            MouseFactory(strain=cls.strain2),
        )

    def test_strain_filter_1(self):
        filter_instance = MouseFilter(
            {"strain": "TestStrain2"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse2, self.mouse3, self.mouse4]) 

    # All strains in filter field when looking at the mice_repository
    def test_strain_choices_mice_repository_fields(self):
        correct_strains = list(Strain.objects.values_list("strain_name", flat=True))
        filter_instance = MouseFilter(queryset=Mouse.objects.all())
        strain_choices = [c for _, c in filter_instance.filters["strain"].field.choices][1:]
        self.assertEqual(strain_choices, correct_strains)

    # Only strains associated with a project in filter field when viewing a project
    def test_strain_choices_filter_project_fields(self):
        correct_strains = list(self.project.strains.all().values_list("strain_name", flat=True))
        filter_instance = MouseFilter(queryset=Mouse.objects.all(), project=self.project)
        strain_choices = [c[1] for c in filter_instance.filters["strain"].field.choices][1:]
        self.assertEqual(strain_choices, correct_strains)


# USE .QS to CHANGE TO QUERYSET
class MouseFilterAgeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(dob=date.today() - timedelta(days=10)),
            MouseFactory(dob=date.today() - timedelta(days=20)),
            MouseFactory(),
            MouseFactory(),
        )

    def test_min_age_filter(self):
        filter_instance = MouseFilter({"min_age": "5"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])

    def test_max_age_filter(self):
        filter_instance = MouseFilter({"max_age": "15"}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs), [self.mouse1, self.mouse3, self.mouse4]
        )

    def test_min_and_max_age_filter_combined(self):
        filter_instance = MouseFilter(
            {"min_age": "5", "max_age": "15"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse1])


class MouseFilterEarmarkTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(earmark="TL"),
            MouseFactory(earmark="TL"),
            MouseFactory(earmark="BR"),
            MouseFactory(earmark="BR"),
        )

    def test_earmark_filter(self):
        filter_instance = MouseFilter({"earmark": "TL"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [self.mouse1, self.mouse2])

    def test_no_matching_mice(self):
        filter_instance = MouseFilter({"earmark": "TR"}, queryset=Mouse.objects.all())
        self.assertEqual(list(filter_instance.qs), [])


class MouseFilterCombinationTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1, cls.mouse2, cls.mouse3, cls.mouse4 = (
            MouseFactory(sex="M", earmark="TL"),
            MouseFactory(sex="F", earmark="TL"),
            MouseFactory(sex="M"),
            MouseFactory(sex="F"),
        )

    def test_empty_filter(self):
        filter_instance = MouseFilter({}, queryset=Mouse.objects.all())
        self.assertEqual(
            list(filter_instance.qs),
            [self.mouse1, self.mouse2, self.mouse3, self.mouse4],
        )

    def test_combined_filters(self):
        filter_instance = MouseFilter(
            {"sex": "M", "earmark": "TL"}, queryset=Mouse.objects.all()
        )
        self.assertEqual(list(filter_instance.qs), [self.mouse1])

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

    # Filter form responds with all mice from given group if "search" keyword is not in HTTP request
    def test_get_filtered_mice_without_search(self):
        result = MouseFilter.get_filtered_mice(self.mice_qs, self.request)
        self.assertEqual(list(result), list(Mouse.objects.all()))

    # Filter form responds with subset of mice from given group if "search" is in HTTP request
    def test_get_filtered_mice_with_search(self):
        self.request.GET = {"search": "true", "sex": "M"}
        result = MouseFilter.get_filtered_mice(self.mice_qs, self.request)
        self.assertEqual(list(result), [self.mouse1])


# Filter form retains populated fields after searching
# e.g. After search for all male mice, "Sex" field should still read "M" after page load
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
