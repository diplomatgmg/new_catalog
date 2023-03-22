from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from .validators import UsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "имя пользователя",
        max_length=32,
        unique=True,
        validators=(UsernameValidator(),),
        error_messages={
            "unique": "Пользователь с таким именем уже существует.",
        },
    )

    first_name = models.CharField("Имя", max_length=16, blank=True)
    last_name = models.CharField("Фамилия", max_length=16, blank=True)
    email = models.EmailField(
        "Почта",
        blank=False,
        unique=True,
        error_messages={
            "unique": "Пользователь с такой почтой уже существует.",
        },
    )

    date_joined = models.DateTimeField("Дата создания", default=timezone.now)

    is_staff = models.BooleanField(
        "Персонал",
        default=False,
        help_text="Пользователь часть персонала",
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @staticmethod
    def find_user(username_or_email, password):
        user = (
            User.objects.filter(username=username_or_email).last()
            or User.objects.filter(email=username_or_email).last()
        )
        return user if user and check_password(password, user.password) else False

    def __str__(self):
        return self.get_username()

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
