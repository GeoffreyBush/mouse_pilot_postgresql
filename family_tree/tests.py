from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from main.model_factories import MouseFactory, UserFactory


def setUpModule():
    global test_user, test_client
    test_user = UserFactory(username="testuser")
    test_client = Client()
    test_client.force_login(test_user)


def tearDownModule():
    global test_user
    test_user.delete()


# switch "create" to "build" for mouse
class FamilyTreeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mouse1 = MouseFactory(sex="F")
        cls.mouse2 = MouseFactory(sex="M")
        cls.mouse3 = MouseFactory(
            sex="F",
            mother=cls.mouse1,
            father=cls.mouse2,
        )
        cls.response = test_client.get(
            reverse("family_tree:family_tree", args=[cls.mouse3.pk])
        )

    def test_http_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_svg_in_content(self):
        self.assertEqual(self.response["Content-Type"], "image/svg+xml")

    def test_svg_html_tags_in_content(self):
        self.assertIn("</svg>", self.response.content.decode())

    def test_tree_nodes(self):
        pass

    def test_tree_edges(self):
        pass

    def test_non_existent_mouse_throws_exception(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(reverse("family_tree:family_tree", args=[10]))

    """
    # Family tree returns correct response data
    def test_create_family_tree_data(self):
        response = self.client.get(reverse("family_tree", args=[self.mouse3]))
        self.assertEqual(response.status_code, 200)
        data = create_family_tree_data(self.mouse3)
        self.assertEqual(
            data,
            {
                "name": str(self.mouse3.id),
                "role": None,
                "parent": str(self.mouse1.id),
                "children": [
                    {"name": str(self.mouse1.id), "role": "Mother", "parent": None},
                    {"name": str(self.mouse2.id), "role": "Father", "parent": None},
                ],
            },
        )
        """
