from django.http import HttpRequest
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from django.utils.http import urlencode

from mice_repository.models import Mouse
from mouse_pilot_postgresql.model_factories import (
    MouseFactory,
    ProjectFactory,
    UserFactory,
)
from mouse_pilot_postgresql.view_utils import paginate_queryset, get_query_params


class PaginateQuerysetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = ProjectFactory()
        cls.mice = MouseFactory.create_batch(25, project=cls.project)
        cls.paginate_by = 10

    def setUp(self):
        self.request = HttpRequest()
        self.ordered_queryset = Mouse.objects.all().order_by("_global_id")

    def test_valid_page(self):
        self.request.GET = {"page": "2"}
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        self.assertEqual(result.number, 2)

    def test_first_page_when_page_not_specified(self):
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        self.assertEqual(result.number, 1)

    def test_first_page_when_page_is_not_integer(self):
        self.request.GET = {"page": "invalid"}
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        self.assertEqual(result.number, 1)

    def test_last_page_when_page_out_of_range(self):
        self.request.GET = {"page": "1000"}
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        self.assertEqual(result.number, result.paginator.num_pages)

    def test_correct_number_of_items_per_page(self):
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        self.assertEqual(len(result.object_list), self.paginate_by)

    def test_correct_total_number_of_pages(self):
        result = paginate_queryset(self.ordered_queryset, self.request, self.paginate_by)
        expected_pages = -(-self.ordered_queryset.count() // self.paginate_by)
        self.assertEqual(result.paginator.num_pages, expected_pages)


class GetQueryParamsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_query_params_removes_page(self):
        request = self.factory.get('/?page=2&filter=active&sort=name')
        result = get_query_params(request)
        self.assertNotIn('page', result)

    def test_get_query_params_keeps_other_params(self):
        request = self.factory.get('/?page=2&filter=active&sort=name')
        result = get_query_params(request)
        self.assertEqual(result, {'filter': ['active'], 'sort': ['name']})

    def test_get_query_params_with_no_page(self):
        request = self.factory.get('/?filter=inactive&sort=date')
        result = get_query_params(request)
        self.assertEqual(len(result), 2)

    def test_get_query_params_with_empty_request(self):
        request = self.factory.get('/')
        result = get_query_params(request)
        self.assertEqual(len(result), 0)

    def test_get_query_params_with_multiple_values(self):
        request = self.factory.get('/?filter=active&filter=inactive&page=2')
        result = get_query_params(request)
        self.assertEqual(result.getlist('filter'), ['active', 'inactive'])

    def test_get_query_params_preserves_query_dict_type(self):
        request = self.factory.get('/?filter=active')
        result = get_query_params(request)
        self.assertIsInstance(result, type(request.GET))