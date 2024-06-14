from django.test import TestCase, RequestFactory
from wean_pups.views import PupsToStockCageView
from mouse_pilot_postgresql.model_factories import UserFactory, BreedingCageFactory, MouseFactory, StrainFactory

class GetInitialDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.strain = StrainFactory()
        cls.mother = MouseFactory(strain=cls.strain, sex='F')
        cls.father = MouseFactory(strain=cls.strain, sex='M')

    def setUp(self):
        self.factory = RequestFactory()
        self.cage = BreedingCageFactory(
            mother=self.mother,
            father=self.father,
            male_pups=2,
            female_pups=3,
        )

    def test_initial_data_structure(self):
        view = self.setup_view()
        initial_data = view.get_initial_data()

        self.assertEqual(len(initial_data), 5)
        self.assertEqual(sum(1 for item in initial_data if item['sex'] == 'M'), 2)
        self.assertEqual(sum(1 for item in initial_data if item['sex'] == 'F'), 3)

    def test_initial_data_content(self):
        view = self.setup_view()
        initial_data = view.get_initial_data()

        for item in initial_data:
            self.assertIn(item['sex'], ['M', 'F'])
            self.assertEqual(item['strain'], self.cage.mother.strain)
            self.assertEqual(item['mother'], self.cage.mother)
            self.assertEqual(item['father'], self.cage.father)
            self.assertEqual(item['dob'], self.cage.date_born)

    def test_zero_pups(self):
        self.cage.male_pups = 0
        self.cage.female_pups = 0
        self.cage.save()

        view = self.setup_view()
        initial_data = view.get_initial_data()

        self.assertEqual(len(initial_data), 0)

    def test_only_male_pups(self):
        self.cage.male_pups = 2
        self.cage.female_pups = 0
        self.cage.save()

        view = self.setup_view()
        initial_data = view.get_initial_data()

        self.assertEqual(len(initial_data), 2)
        self.assertTrue(all(item['sex'] == 'M' for item in initial_data))

    def test_only_female_pups(self):
        self.cage.male_pups = 0
        self.cage.female_pups = 3
        self.cage.save()

        view = self.setup_view()
        initial_data = view.get_initial_data()

        self.assertEqual(len(initial_data), 3)
        self.assertTrue(all(item['sex'] == 'F' for item in initial_data))

    def setup_view(self):
        request = self.factory.get(f'/pups_to_stock_cage/{self.cage.box_no}')
        request.user = self.user
        view = PupsToStockCageView()
        view.dispatch(request, box_no=self.cage.box_no)
        return view