from django.urls import reverse
from django.test import TestCase
from apps.user.models import User

from apps.product.models import CPUModel


class CPUListViewTestCase(TestCase):
    fixtures = ['brand.json', 'category.json', 'cpu.json']

    def setUp(self):
        self.url = reverse('product:cpu')
        self.username = 'testuser'
        self.password = '12345'
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_cpu_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/includes/cpu-list.html')
        self.assertEqual(len(response.context['products']), CPUModel.objects.all().count())

    def test_cpu_list_view_filter_by_num_cores(self):
        num_cores_min = 4
        num_cores_max = 8
        response = self.client.get(self.url, {'min_num_cores': num_cores_min, 'max_num_cores': num_cores_max})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/includes/cpu-list.html')

        for cpu in response.context['products']:
            self.assertTrue(num_cores_min <= cpu.num_cores <= num_cores_max)

    def test_cpu_list_view_filter_by_clock_speed(self):
        clock_speed_min = 3000
        clock_speed_max = 3500
        response = self.client.get(self.url, {'min_clock_speed': clock_speed_min, 'max_clock_speed': clock_speed_max})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/includes/cpu-list.html')

        for cpu in response.context['products']:
            self.assertTrue(clock_speed_min <= cpu.clock_speed <= clock_speed_max)

    def test_cpu_list_view_search_query(self):
        query = 'Intel'
        response = self.client.get(self.url, {'q': query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/includes/cpu-list.html')

        for cpu in response.context['products']:
            self.assertIn(query.lower(), cpu.get_full_name().lower())
