from django.db import models
from django.urls import reverse


class BaseComparison(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, verbose_name="Пользователь")

    class Meta:
        abstract = True


class CPUComparison(BaseComparison):
    products = models.ManyToManyField(
        "product.CPUModel",
        verbose_name="Процессоры",
        related_name="compare_cpu",
    )

    def get_absolute_url(self):
        return reverse("comparison:cpu")

    class Meta:
        verbose_name = "сравнение процессоров"
        verbose_name_plural = "сравнение процессоров"


class GPUComparison(BaseComparison):
    products = models.ManyToManyField(
        "product.GPUModel",
        verbose_name="Процессоры",
        related_name="compare_gpu",
    )

    def get_absolute_url(self):
        return reverse("comparison:gpu")

    class Meta:
        verbose_name = "сравнение видеокарт"
        verbose_name_plural = "сравнение видеокарт"
