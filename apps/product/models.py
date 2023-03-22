from django.db import models
from django.template.defaultfilters import slugify

from apps.comparison.models import CPUComparison, GPUComparison


class Brand(models.Model):
    name = models.CharField("Бренд", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "бренд"
        verbose_name_plural = "бренды"


class Category(models.Model):
    name = models.CharField("Категория", max_length=100)
    slug = models.SlugField("Слаг", max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class BaseProductModel(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория"
    )
    brand = models.ForeignKey(
        "Brand",
        on_delete=models.CASCADE,
        verbose_name="Производитель",
        help_text="Введите производителя процессора",
    )
    slug = models.SlugField("Слаг", max_length=32, unique=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        raise NotImplementedError(
            f"Не объявлен метод get_full_name в классе {self.__class__.__name__}"
        )

    def get_comparison_model(self):
        raise NotImplementedError(
            f"Не объявлен метод get_full_name в классе {self.__class__.__name__}"
        )

    def save(self, **kwargs):
        full_name = self.get_full_name()
        self.slug = slugify(full_name)
        super().save(**kwargs)

    class Meta:
        abstract = True


class CPUModel(BaseProductModel):
    family = models.CharField(
        max_length=50, verbose_name="Семейство", help_text="Пример: Ryzen 9"
    )
    model = models.CharField(
        max_length=50, verbose_name="Модель", help_text="Пример: 5900x"
    )
    num_cores = models.PositiveIntegerField(
        verbose_name="Количество ядер", help_text="Введите количество ядер процессора"
    )
    base_clock = models.PositiveIntegerField(
        verbose_name="Тактовая частота",
        help_text="Введите тактовую частоту процессора в MHz",
    )

    def get_comparison_model(self):
        return CPUComparison

    def get_full_name(self):
        return f"{self.brand.name} {self.family} {self.model}"

    class Meta:
        ordering = ("brand", "family", "model")


class GPUModel(BaseProductModel):
    family = models.CharField(
        max_length=50, verbose_name="Семейство", help_text="Пример: GeForce RTX"
    )
    model = models.CharField(
        max_length=50, verbose_name="Модель", help_text="Пример: 3080"
    )
    base_clock = models.PositiveIntegerField(
        verbose_name="Базовая тактовая частота",
        help_text="Введите базовую тактовую частоту видеокарты в GHz",
    )
    boost_clock = models.PositiveIntegerField(
        verbose_name="Максимальная тактовая частота",
        help_text="Введите максимальную тактовую частоту видеокарты в GHz",
    )

    def get_comparison_model(self):
        return GPUComparison

    def get_full_name(self):
        return f"{self.brand.name} {self.family} {self.model}"

    class Meta:
        ordering = ("family", "model")
