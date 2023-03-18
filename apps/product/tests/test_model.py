from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from apps.product.models import Brand, Category, CPUModel, GPUModel
from django.utils.encoding import force_str


class BrandTestCase(TestCase):
    fixtures = ['brand.json']

    def test_brand_str(self):
        brand = Brand.objects.get(pk=1)
        self.assertEqual(str(brand), 'AMD')


class CategoryTestCase(TestCase):
    fixtures = ['category.json']

    # Проблемы с кириллицей
    # def test_category_str(self):
    #     category = Category.objects.get(pk=1)
    #     self.assertEqual(force_str(category), 'Процессоры')


class CPUModelTestCase(TestCase):
    fixtures = ['brand.json', 'category.json', 'cpu.json']

    def test_cpu_str(self):
        cpu = CPUModel.objects.get(pk=1)
        self.assertEqual(str(cpu), 'AMD Ryzen 3 5500')

    def test_cpu_full_name(self):
        cpu = CPUModel.objects.get(pk=1)
        self.assertEqual(cpu.get_full_name(), 'AMD Ryzen 3 5500')

    def test_cpu_slug(self):
        cpu = CPUModel.objects.get(pk=1)
        self.assertEqual(cpu.slug, 'amd-ryzen-3-5500')


class GPUModelTestCase(TestCase):
    fixtures = ['brand.json', 'category.json', 'gpu.json']

    def test_gpu_str(self):
        gpu = GPUModel.objects.get(pk=1)
        self.assertEqual(str(gpu), 'NVIDIA GeForce RTX 2060')

    def test_gpu_full_name(self):
        gpu = GPUModel.objects.get(pk=1)
        self.assertEqual(gpu.get_full_name(), 'NVIDIA GeForce RTX 2060')

    def test_gpu_slug(self):
        gpu = GPUModel.objects.get(pk=1)
        self.assertEqual(gpu.slug, 'nvidia-geforce-rtx-2060')
