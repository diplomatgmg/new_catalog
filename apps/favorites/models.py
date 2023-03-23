from django.db import models


class FavoriteProducts(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    cpu = models.ManyToManyField(
        "product.CPUModel", blank=True, verbose_name="Процессоры"
    )
    gpu = models.ManyToManyField(
        "product.GPUModel", blank=True, verbose_name="Видеокарты"
    )

    def get_favorites(self):
        return *self.cpu.all(), *self.gpu.all()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "избранное"
        verbose_name_plural = "избранное"
