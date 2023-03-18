from django.shortcuts import redirect
from django.urls import reverse
from apps.product.models import CPUModel, GPUModel
import re

from fuzzywuzzy import process

PRODUCT_MODELS = (
    CPUModel,
    GPUModel,
)


def find_model(request):
    query = request.GET.get('q')
    query_params = '?' + request.META['QUERY_STRING']
    slugs = get_slugs()

    best_match = [(model, find_match(query, slug)) for model, slug in slugs.items()]

    model = best_match[0][0].objects.filter(slug=best_match[0][1]).last()
    slug = model.category.slug
    url = reverse(f'product:{slug}')
    request.session['query'] = query
    response = redirect(url + query_params, query)
    return response


def get_slugs():
    return {model: list(model.objects.values_list('slug', flat=True)) for model in PRODUCT_MODELS}


def find_match(string_1, seq):
    """
    Функция для поиска наилучшего совпадения между строками.
    """
    string_1 = clean_string(string_1)
    matches = process.extract(string_1, seq, scorer=string_similarity)
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[0][0] if matches else None


def string_similarity(string_1, string_2):
    """
    Функция для вычисления сходства двух строк.
    """
    len1, len2 = len(string_1), len(string_2)
    common_chars = set(string_1) & set(string_2)
    common_count = sum(min(string_2.count(char), string_1.count(char)) for char in common_chars)
    return (2.0 * common_count) / (len1 + len2) * 100


def clean_string(string):
    """
    Функция, которая оставляет только буквы и цифры в строке
    """
    return re.sub(r'[^a-z0-9\s]', ' ', string.strip().lower())


def min_length(string):
    return min(len(word) for word in string.split())
