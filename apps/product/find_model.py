import re

import numpy as np
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from fuzzywuzzy import process

PRODUCT_MODELS = settings.PRODUCT_MODELS

product_models = [apps.get_model(model_name) for model_name in PRODUCT_MODELS]


def find_model(request):
    query = request.GET.get("q")
    query = clean_string(query)

    if not query:
        messages.warning(request, "Похоже, вы ввели пустой запрос.")
        return redirect(reverse("index:index"))

    query_params = "?" + request.META["QUERY_STRING"]

    slugs = get_slugs()

    matches = [[model, find_match(query, slug)] for model, slug in slugs.items()]

    try:
        matches.sort(key=lambda x: x[1][1] if x[1] else [], reverse=True)
        model = matches[0][0]
        category_slug = model.objects.first().category.slug
        url = reverse(f"product:{category_slug}")
        response = redirect(url + query_params, query)
        return response

    except IndexError:
        messages.warning(
            request,
            "Похоже, вы ввели только бренд. " "Пожалуйста, уточните категорию вручную.",
        )
    except TypeError:
        messages.warning(
            request, "Скорее всего, такого товара не существует в нашей базе."
        )

        return redirect(reverse("index:index"))


def get_slugs():
    return {
        model: list(model.objects.values_list("slug", flat=True))
        for model in product_models
    }


def string_similarity(string_1, string_2):
    """
    Функция для вычисления сходства двух строк.
    """
    len1 = len(string_1)
    len2 = len(string_2)

    # Вычисляем расстояние Левенштейна
    dist = np.zeros((len1 + 1, len2 + 1), dtype=int)

    for i in range(len1 + 1):
        dist[i][0] = i

    for j in range(len2 + 1):
        dist[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if string_1[i - 1] == string_2[j - 1]:
                cost = 0
            else:
                cost = 1

            dist[i][j] = min(
                dist[i - 1][j] + 1, dist[i][j - 1] + 1, dist[i - 1][j - 1] + cost
            )

    # Вычисляем процентное соотношение сходства строк
    return ((len1 + len2) - dist[len1][len2]) / (len1 + len2) * 100


def clean_string(string):
    """
    Функция, которая оставляет только буквы и цифры в строке
    """
    s = string.strip().lower()
    return re.sub(r"[^a-z0-9\s]", " ", s)


def find_match(string_1, seq):
    """
    Функция для поиска наилучшего совпадения между строками.
    """

    # Удаляем из string_1 символы, отличные от букв и цифр и приводим к нижнему регистру
    string_1 = clean_string(string_1)

    # Удаляем из seq все элементы, где длина слова меньше длины самого короткого слова в string_1
    min_len = len(min(string_1.split(), key=len))
    new_seq = [
        " ".join(word for word in s.split("-") if len(word) >= min_len) for s in seq
    ]

    filtered_seq = []
    for index, slug in enumerate(new_seq):
        brand = seq[index].split("-", maxsplit=1)[0].lower()

        # Удаляем бренд из slug если пользователь его не вводит
        if brand not in string_1:
            slug = slug.replace(brand, "").strip()

        # Если пользователь ввел только бренд
        if string_1 == brand:
            return []

        filtered_seq.append(slug.strip("-"))

    # Создаем список возможных вариантов совпадений
    matches = process.extract(string_1, filtered_seq, scorer=string_similarity)

    # Сортируем список возможных вариантов совпадений по убыванию коэффициента схожести
    matches.sort(key=lambda x: x[1], reverse=True)

    # Если список возможных вариантов совпадений не пуст, то выводим первый элемент списка
    if matches:
        return matches[0]
