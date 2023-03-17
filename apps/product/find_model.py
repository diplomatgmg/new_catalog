from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from apps.product.models import CPUModel

PRODUCT_MODELS = (
    CPUModel,
)

def find_model(request):
    query = request.GET.get('q')
    result = string_similarity(query)
    query_params = '?' + request.META['QUERY_STRING']

    if result:
        slug = result.category.slug
        url = reverse(f'product:{slug}')
        request.session['query'] = query
        response = redirect(url + query_params, query)
        return response
    else:
        messages.warning(request, 'Похоже, поиск сломался. '
                                  'Пожалуйста, уточните категорию вручную.')
        return redirect(reverse('index:index') + query_params)





def string_similarity(query):
    """
    Функция для вычисления сходства двух строк.
    """
    # Приводим строки к нижнему регистру
    query = ' '.join(word for word in query.strip().lower().split() if len(word) >= 3)

    for model in PRODUCT_MODELS:
        models = model.objects.all()
        for product in models:

            word = ' '.join(word for word in product.slug.split('-') if len(word) >= 3)

            # Вычисляем длины строк
            len1 = len(query)
            len2 = len(word)

            # Находим количество общих символов
            common_chars = set(query) & set(word)
            common_count = sum(min(query.count(char), word.count(char)) for char in common_chars)

            # Вычисляем процентное соотношение сходства строк
            similarity = (2.0 * common_count) / (len1 + len2) * 100

            if int(similarity) in range(75, 101):
                return product
            else:
                print(product.slug, similarity)
