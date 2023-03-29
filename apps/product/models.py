from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

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
            f"Не объявлен метод get_full_name "
            f"в классе {self.__class__.__name__}"
        )

    @staticmethod
    def get_comparison_model():
        raise NotImplementedError(f"Не объявлен метод get_full_name ")

    def get_review_url(self):
        return reverse(
            "product:review:list-create",
            args=(self.category.slug, self.slug),
        )

    def save(self, **kwargs):
        full_name = self.get_full_name()
        self.slug = slugify(full_name)
        super().save(**kwargs)

    class Meta:
        abstract = True


class CPUModel(BaseProductModel):
    family = models.CharField(
        max_length=50,
        verbose_name="Семейство",
        help_text="Прим.: Ryzen 9",
    )
    model = models.CharField(
        max_length=50, verbose_name="Модель", help_text="Прим.: 5900x"
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Год выпуска",
    )

    SER = "Серверный"
    DES = "Настольный"
    MOB = "Мобильный"
    SEGMENT_CHOICES = (
        (SER, "Серверный"),
        (DES, "Настольный"),
        (MOB, "Мобильный"),
    )

    segment = models.CharField(
        "Сегмент",
        null=True,
        blank=True,
        max_length=10,
        choices=SEGMENT_CHOICES,
        default=DES,
    )

    socket = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Сокет",
    )
    cores = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Количество ядер",
    )
    threads = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Количество потоков",
    )
    base_clock = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Базовая частота",
    )
    boost_clock = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Максимальная частота",
    )
    unlocked_multiplier = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Разблокированный множитель",
        help_text="Имеет ли процессор разблокированный множитель для разгона",
    )
    architecture = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Архитектура",
        help_text="Прим.: Raptor Lake",
    )
    technology = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Техпроцесс",
    )
    tdp = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="TDP",
    )
    max_temperature = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Максимальная температура",
    )
    l1_cache = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Кэш L1",
        help_text="Объем кэша L1 в КБ",
    )
    l2_cache = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Кэш L2",
        help_text="Объем кэша L2 в КБ",
    )
    l3_cache = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Кэш L3",
        help_text="Объем кэша L3 в КБ",
    )
    integrated_graphics = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Встроенная графика",
    )
    memory_controller = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name="Тип памяти",
        help_text="Тип поддерживаемой памяти",
    )
    pcie = models.CharField(
        null=True,
        blank=True,
        max_length=3,
        verbose_name="PCIe",
    )

    @classmethod
    def get_category_slug(cls):
        return "cpu"

    @staticmethod
    def get_reverse_url():
        return reverse("product:cpu")

    @staticmethod
    def get_comparison_model():
        return CPUComparison

    def get_full_name(self):
        return f"{self.brand.name} {self.family} {self.model}"

    class Meta:
        ordering = (
            "-year",
            "-segment",
        )


class GPUModel(BaseProductModel):
    family = models.CharField(
        verbose_name="Семейство", max_length=50, help_text="Пример: GeForce RTX"
    )
    model = models.CharField(
        verbose_name="Модель", max_length=50, help_text="Пример: 3080"
    )
    base_clock = models.PositiveIntegerField(
        verbose_name="Базовая тактовая частота",
        help_text="Введите базовую тактовую частоту видеокарты в GHz",
    )
    boost_clock = models.PositiveIntegerField(
        verbose_name="Максимальная тактовая частота",
        help_text="Введите максимальную тактовую частоту видеокарты в GHz",
    )

    @staticmethod
    def get_reverse_url():
        return reverse("product:gpu")

    @staticmethod
    def get_comparison_model():
        return GPUComparison

    def get_full_name(self):
        return f"{self.brand.name} {self.family} {self.model}"

    class Meta:
        ordering = ("family", "model")
