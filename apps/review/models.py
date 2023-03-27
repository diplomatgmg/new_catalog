from django.db import models


class BaseReview(models.Model):
    RATING_CHOICES = [(rating, str(rating)) for rating in range(1, 6)]

    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CPUReview(BaseReview):
    product = models.ForeignKey("product.CPUModel", on_delete=models.CASCADE)


class GPUReview(BaseReview):
    product = models.ForeignKey("product.GPUModel", on_delete=models.CASCADE)
