from django.test import TestCase
from .models import Brand, Category, CPUModel, GPUModel


class BrandModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Intel')

    def test_brand_name(self):
        self.assertEqual(str(self.brand), 'Intel')


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Processors', slug='processors')

    def test_category_name(self):
        self.assertEqual(str(self.category), 'Processors')

    def test_category_slug(self):
        self.assertEqual(self.category.slug, 'processors')


class CPUModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='AMD')
        self.category = Category.objects.create(name='Processors', slug='processors')
        self.cpu = CPUModel.objects.create(
            category=self.category,
            brand=self.brand,
            family='Ryzen 5',
            model='5600X',
            num_cores=6,
            clock_speed=3700
        )

    def test_cpu_family(self):
        self.assertEqual(self.cpu.family, 'Ryzen 5')

    def test_cpu_model(self):
        self.assertEqual(self.cpu.model, '5600X')

    def test_cpu_num_cores(self):
        self.assertEqual(self.cpu.num_cores, 6)

    def test_cpu_clock_speed(self):
        self.assertEqual(self.cpu.clock_speed, 3700)

    def test_cpu_full_name(self):
        self.assertEqual(self.cpu.get_full_name(), 'AMD Ryzen 5 5600X')

    def test_cpu_slug(self):
        self.assertEqual(self.cpu.slug, 'amd-ryzen-5-5600x')

    def test_cpu_sorting(self):
        cpu2 = CPUModel.objects.create(
            category=self.category,
            brand=self.brand,
            family='Ryzen 9',
            model='5950X',
            num_cores=16,
            clock_speed=3400
        )
        self.assertLess(self.cpu, cpu2)
        self.assertGreater(cpu2, self.cpu)
        self.assertEqual(self.cpu, self.cpu)


class GPUModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Nvidia')
        self.category = Category.objects.create(name='Graphics Cards', slug='graphics-cards')
        self.gpu = GPUModel.objects.create(
            category=self.category,
            brand=self.brand,
            family='GeForce RTX',
            model='3080',
            base_clock_speed=1.44,
            boost_clock_speed=1.71
        )

    def test_gpu_family(self):
        self.assertEqual(self.gpu.family, 'GeForce RTX')

    def test_gpu_model(self):
        self.assertEqual(self.gpu.model, '3080')

    def test_gpu_base_clock_speed(self):
        self.assertEqual(self.gpu.base_clock_speed, 1.44)

    def test_gpu_boost_clock_speed(self):
        self.assertEqual(self.gpu.boost_clock_speed, 1.71)

    def test_gpu_full_name(self):
        self.assertEqual(self.gpu.get_full_name(), 'Nvidia GeForce RTX 3080')

    def test_gpu_slug(self):
        self.assertEqual(self.gpu.slug, 'nvidia-geforce-rtx-3080')

    def test_gpu_sorting(self):
        gpu2 = GPUModel.objects.create(
            category=self.category,
            brand=self.brand,
            family='GeForce RTX',
            model='3070',
            base_clock_speed=1.50,
            boost_clock_speed=1.73
        )
        self.assertLess(self.gpu, gpu2)
        self.assertGreater(gpu2, self.gpu)
        self.assertEqual(self.gpu, self.gpu)
