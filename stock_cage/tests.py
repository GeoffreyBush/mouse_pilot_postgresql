from django.test import TestCase

from mice_repository.models import Mouse
from mouse_pilot_postgresql.form_factories import BatchFromBreedingCageFormFactory
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    StockCageFactory,
)
from wean_pups.forms import BatchFromBreedingCageForm
from stock_cage.models import StockCage
from website.models import Strain


class StockCageModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cage = StockCageFactory()
        cls.mouse1, cls.mouse2 = MouseFactory(stock_cage=cls.cage), MouseFactory(
            stock_cage=cls.cage
        )

    def test_stock_cage_factory_count(self):
        self.assertEqual(StockCage.objects.count(), 1)

    def test_stock_cage_pk(self):
        self.assertEqual(self.cage.pk, 1)

    # Test box_no equivalent when that information is provided by breeding wing

    def test_stock_mice(self):
        self.assertEqual(self.cage.mice.count(), 2)



