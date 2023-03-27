from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse


class BaseComparison(models.Model):
    user = models.ForeignKey(
        "user.User",
        models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    temp_user = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.username
        return self.temp_user

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

    @staticmethod
    @receiver(pre_delete, sender=Session)
    def delete_comparison_for_session(sender, instance, **kwargs):
        to_delete = CPUComparison.objects.filter(temp_user=instance.session_key)
        if to_delete.exists():
            to_delete.delete()


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

    @staticmethod
    @receiver(pre_delete, sender=Session)
    def delete_comparison_for_session(sender, instance, **kwargs):
        to_delete = GPUComparison.objects.filter(temp_user=instance.session_key)
        if to_delete.exists():
            to_delete.delete()
