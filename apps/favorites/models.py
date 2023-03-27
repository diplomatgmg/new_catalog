from django.db import models


class Favorites(models.Model):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    temp_user = models.CharField(max_length=255, blank=True, null=True)

    cpu = models.ManyToManyField(
        "product.CPUModel", blank=True, verbose_name="Процессоры"
    )
    gpu = models.ManyToManyField(
        "product.GPUModel", blank=True, verbose_name="Видеокарты"
    )

    def get_favorites(self):
        return (
            *self.cpu.all().select_related("brand", "category"),
            *self.gpu.all().select_related("brand", "category"),
        )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранное"
