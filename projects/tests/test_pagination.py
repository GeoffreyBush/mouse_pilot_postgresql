from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlencode

from mice_repository.models import Mouse
from mouse_pilot_postgresql.model_factories import MouseFactory, ProjectFactory, UserFactory
from projects.views import ShowProjectView


class PaginateProjectMiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = ShowProjectView()
        cls.project = ProjectFactory()
        cls.mice = MouseFactory.create_batch(25, project=cls.project)

    def setUp(self):
        self.request = HttpRequest()
        self.ordered_queryset = Mouse.objects.all().order_by("_global_id")

    def test_valid_page(self):
        self.request.GET["page"] = "2"
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 2)

    def test_first_page_when_page_not_specified(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 1)

    def test_first_page_when_page_is_not_integer(self):
        self.request.GET["page"] = "invalid"
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, 1)

    def test_last_page_when_page_out_of_range(self):
        self.request.GET["page"] = "1000"
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(result.number, result.paginator.num_pages)

    def test_correct_number_of_items_per_page(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        self.assertEqual(len(result.object_list), self.view.paginate_by)

    def test_correct_total_number_of_pages(self):
        result = self.view.paginate_project_mice(self.ordered_queryset, self.request)
        expected_pages = -(-self.ordered_queryset.count() // self.view.paginate_by)
        self.assertEqual(result.paginator.num_pages, expected_pages)

class ShowProjectViewFilterPaginationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory(username="testuser")
        cls.client = Client()
        
    @classmethod
    def setUpTestData(cls):
        cls.project = ProjectFactory()
        cls.male_mice = MouseFactory.create_batch(15, project=cls.project, sex='M')
        cls.female_mice = MouseFactory.create_batch(15, project=cls.project, sex='F')

    def setUp(self):
        self.client.force_login(self.user)
        self.data = {
            'csrfmiddlewaretoken': 'dummytoken',
            'sex': 'M',
            'earmark': '',
            'search': ''
        }
        self.url = self.get_url()

    def get_url(self, page=None, **kwargs):
        url = reverse('projects:show_project', args=[self.project.project_name])
        if kwargs or page:
            params = kwargs.copy()
            if page:
                params['page'] = page
            url += f'?{urlencode(params)}'
        return url

    def test_initial_page_no_filter(self):
        response = self.client.get(self.get_url())
        self.assertEqual(len(response.context['project_mice']), 10)
        self.assertEqual(response.context['project_mice'].paginator.count, 30)

    def test_count_pagination_stats_after_filter_applied(self):
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context['project_mice'].number, 1)
        self.assertEqual(response.context['project_mice'].paginator.count, 15)

    def test_filter_applied_on_another_page(self):
        self.data["page"] = 2
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context['project_mice'].number, 2)
        self.assertEqual(len(response.context['project_mice']), 5)
        self.assertEqual(response.context['project_mice'].paginator.count, 15)

    def test_invalid_page_with_filter_shows_last_page(self):
        self.data["page"], self.data["sex"] = 999, 'F'
        response = self.client.get(self.url, data=self.data)
        self.assertEqual(response.context['project_mice'].number, 2)