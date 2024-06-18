from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import PupsToStockCageFormSetFactory
from mouse_pilot_postgresql.model_factories import (
    BreedingCageFactory,
    MouseFactory,
    StrainFactory,
    UserFactory,
)
from wean_pups.forms import PupsToStockCageForm
from wean_pups.views import PupsToStockCageView


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


class PupsToStockCageViewGetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = BreedingCageFactory()
        cls.response = test_client.get(
            reverse("wean_pups:pups_to_stock_cage", args=[cls.cage.box_no])
        )
        cls.formset = cls.response.context["formset"]

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, "pups_to_stock_cage.html")

    def test_formset_in_context(self):
        self.assertIsNotNone(self.formset)

    def test_all_forms_in_formset_are_correct_type(self):
        assert all(isinstance(form, PupsToStockCageForm) for form in self.formset)

    def test_formset_contains_correct_number_of_forms(self):
        self.assertEqual(
            len(self.formset.forms), self.cage.male_pups + self.cage.female_pups
        )

    def test_invalid_box_no_in_url(self):
        response = test_client.get(
            reverse("wean_pups:pups_to_stock_cage", args=["invalid"])
        )
        self.assertEqual(response.status_code, 404)

    def test_not_passing_box_no_in_url(self):
        with self.assertRaises(NoReverseMatch):
            test_client.get(reverse("wean_pups:pups_to_stock_cage"))


class PupsToStockCageViewValidPostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(strain=cls.strain, sex="F")
        cls.father = MouseFactory(strain=cls.strain, sex="M")
        cls.cage = BreedingCageFactory(male_pups=3, female_pups=5)
        cls.formset = PupsToStockCageFormSetFactory.build(
            strain=cls.strain,
            mother=cls.mother.pk,
            father=cls.father.pk,
            num_males=cls.cage.male_pups,
            num_females=cls.cage.female_pups,
        )
        cls.mouse_count = Mouse.objects.count()
        cls.request = cls.factory.post(
            reverse("wean_pups:pups_to_stock_cage", args=[cls.cage.box_no]),
            cls.formset.data,
        )
        cls.request.user = test_user
        cls.response = PupsToStockCageView.as_view()(
            cls.request, box_no=cls.cage.box_no
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirect_url(self):
        self.assertEqual(
            self.response.url, reverse("breeding_cage:list_breeding_cages")
        )

    def test_mice_created(self):
        self.assertEqual(Mouse.objects.count(), self.mouse_count + 8)

    # If tube numbers given, correct assignment
    def test_pups_to_stock_cage_valid_data(self):
        pass


class PupsToStockCageViewInvalidPostTest(TestCase):
    def x(self):
        pass

    # Can't transfer from the same breeding cage twice

    # Error message displayed to user
