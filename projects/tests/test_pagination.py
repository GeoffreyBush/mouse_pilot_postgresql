from django.test import TestCase
from django.http import HttpRequest
from projects.views import ShowProjectView
from mice_repository.models import Mouse
from mouse_pilot_postgresql.model_factories import ProjectFactory, MouseFactory


class PaginateProjectMiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = ShowProjectView()
        cls.project = ProjectFactory()
        cls.mice = MouseFactory.create_batch(25, project=cls.project)

    def setUp(self):
        self.request = HttpRequest()
        self.ordered_queryset = Mouse.objects.all().order_by('_global_id')

    def test_valid_page(self):
        self.request.GET['page'] = '2'
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 2)

    def test_first_page_when_page_not_specified(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 1)

    def test_first_page_when_page_is_not_integer(self):
        self.request.GET['page'] = 'invalid'
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 1)

    def test_last_page_when_page_out_of_range(self):
        self.request.GET['page'] = '1000'
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, result.paginator.num_pages)

    def test_correct_number_of_items_per_page(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(len(result.object_list), self.view.paginate_by)

    def test_correct_total_number_of_pages(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        expected_pages = -(-self.ordered_queryset.count() // self.view.paginate_by)
        self.assertEqual(result.paginator.num_pages, expected_pages)