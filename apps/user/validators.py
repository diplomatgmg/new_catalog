from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*$'
    message = 'Введите корректное имя пользователя, оно может содержать только латинские буквы,' \
              'цифры, спецсимволы (., _, -)'
