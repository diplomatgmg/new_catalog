from django import forms

from apps.review.models import BaseReview


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        label="Рейтинг",
        choices=BaseReview.RATING_CHOICES,
        widget=forms.Select(),
    )
    content = forms.CharField(label="Отзыв", widget=forms.Textarea())
