from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField('Бренд', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    slug = models.SlugField('Слаг', max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class BaseProductModel(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 verbose_name='Категория')
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Бренд')
    slug = models.SlugField('Слаг', max_length=32, unique=True, blank=True)

    class Meta:
        abstract = True


class CPUModel(BaseProductModel):
    name = models.CharField('Название',
                            help_text='Пример: Ryzen <sub>7 7900x</sub>',
                            max_length=16)

    series = models.CharField('Серия',
                              help_text='Пример: <sub>Ryzen</sub> 7 <sub>7900x</sub>',
                              max_length=20)

    generation = models.CharField('Поколение',
                                  help_text='Пример: <sub>Ryzen 7</sub> 7<sub>900x</sub>',
                                  max_length=3)

    model = models.CharField('Модель',
                             help_text='Пример: <sub>Ryzen 7 7</sub>900x',
                             max_length=8)

    price = models.PositiveIntegerField('Цена')

    def get_full_name(self):
        return f'{self.brand.name} {self.name} {self.series} {self.generation}{self.model}'

    def save(self, **kwargs):
        full_name = self.get_full_name()
        self.slug = slugify(full_name)
        super().save(**kwargs)

    def __str__(self):
        return self.get_full_name()


