from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from website.tests.form_factories import BreedingCageFormFactory
from website.tests.model_factories import (
    BreedingCageFactory,
    StrainFactory,
    UserFactory,
)


class ListBreedingCagesTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")
        self.strain = StrainFactory()
        self.cage = BreedingCageFactory()

    # Access breeding wing dashboard logged in
    def test_list_breeding_cages_view_with_authenticated_user(self):
        response = self.client.get(reverse("list_breeding_cages"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_cages/list_breeding_cages.html")
        self.assertIn("mycages", response.context)
        self.assertIn(self.cage, response.context["mycages"])

    # Access breeding wing dashboard without logging in
    def test_list_breeding_cages_view_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("list_breeding_cages"))
        url = reverse("list_breeding_cages")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ViewBreedingCageTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.cage = BreedingCageFactory()
        self.client.login(username="testuser", password="testpassword")

    # Access breeding wing cage view logged in
    def test_view_breeding_cage_with_authenticated_user(self):
        response = self.client.get(
            reverse("view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_cages/view_breeding_cage.html")
        self.assertIn("mycage", response.context)
        self.assertEqual(response.context["mycage"], self.cage)

    # Access non-existent cage
    def test_view_non_existent_breeding_cage(self):
        self.client.login(username="testuser", password="testpassword")
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("view_breeding_cage", args=[10]))

    # Access breeding wing cage view without logging in
    def test_view_breeding_cage_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(
            reverse("view_breeding_cage", args=[self.cage.box_no])
        )
        self.assertEqual(response.status_code, 302)


class AddBreedingCageViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.client.login(username="testuser", password="testpassword")

    # Access Create Breeding Cage while logged in
    def test_create_breeding_cage_get_with_authenticated_user(self):
        response = self.client.get(reverse("add_breeding_cage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_cages/add_breeding_cage.html")

    # POST BreedingCageForm with valid data
    def test_create_breeding_cage_post_valid(self):
        data = BreedingCageFormFactory.valid_data()
        response = self.client.post(reverse("add_breeding_cage"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_breeding_cages"))

    # POST BreedingCageForm with invalid mother
    def test_create_breeding_cage_post_invalid(self):
        data = BreedingCageFormFactory.invalid_mother()
        response = self.client.post(reverse("add_breeding_cage"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "breeding_cages/add_breeding_cage.html")

    # Access add cage while not logged in
    def test_create_breeding_cage_get_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("add_breeding_cage"))
        url = reverse("add_breeding_cage")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


# Edit breeding cage view
