from django.db import models


class BaseReview(models.Model):
    RATING_CHOICES = [(rating, str(rating)) for rating in range(1, 6)]

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CPUReview(BaseReview):
    product = models.ForeignKey("product.CPUModel", on_delete=models.CASCADE)

    @classmethod
    def get_category_slug(cls):
        return "cpu"


class GPUReview(BaseReview):
    product = models.ForeignKey("product.GPUModel", on_delete=models.CASCADE)

    @classmethod
    def get_category_slug(cls):
        return "gpu"
