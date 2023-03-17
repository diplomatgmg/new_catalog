import re

from fuzzywuzzy import process
from datetime import datetime


def string_similarity(string_1, string_2):
    """
    Функция для вычисления сходства двух строк.
    """

    # Вычисляем длины строк
    len1 = len(string_1)
    len2 = len(string_2)

    # Находим количество общих символов
    common_chars = set(string_1) & set(string_2)
    common_count = sum(min(string_2.count(char), string_2.count(char)) for char in common_chars)

    # Вычисляем процентное соотношение сходства строк
    similarity = (2.0 * common_count) / (len1 + len2) * 100

    return similarity


def clean_string(string):
    """
    Функция, которая оставляет только буквы и цифры в строке
    """
    s = string.strip().lower()
    return re.sub(r'[^a-z0-9\s]', ' ', s)


def min_length(string):
    return min(len(word) for word in string.split())


def find_match(string_1, string_2):
    """
    Функция для поиска наилучшего совпадения между строками.
    """

    # Удаляем из s1 символы, отличные от букв и цифр и приводим к нижнему регистру
    string_1 = clean_string(string_1)

    # Создаем список возможных вариантов совпадений
    matches = process.extract(string_1, string_2, scorer=string_similarity)

    # Сортируем список возможных вариантов совпадений по убыванию коэффициента схожести
    matches.sort(key=lambda x: x[1], reverse=True)

    # Если список возможных вариантов совпадений не пуст, то выводим первый элемент списка
    if matches:
        return matches[0][0]


s1 = 'ryzen 5500'
s2 = ["amd-ryzen-5-5500", "amd-ryzen-7-5600x", "amd-ryzen-7-5800x", 'nvidia-rtx-2060'] * 10000 + ['nvidia-rtx-5500']

start = datetime.now()

print(find_match(s1, s2))

print(datetime.now() - start)