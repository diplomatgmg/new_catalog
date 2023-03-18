import re
from fuzzywuzzy import process
import numpy as np


def string_similarity(string_1, string_2):
    """
    Функция для вычисления сходства двух строк.
    """
    len1 = len(string_1)
    len2 = len(string_2)

    # Вычисляем расстояние Левенштейна
    dist = np.zeros((len1+1, len2+1), dtype=int)

    for i in range(len1+1):
        dist[i][0] = i

    for j in range(len2+1):
        dist[0][j] = j

    for i in range(1, len1+1):
        for j in range(1, len2+1):
            if string_1[i-1] == string_2[j-1]:
                cost = 0
            else:
                cost = 1

            dist[i][j] = min(dist[i-1][j] + 1,
                             dist[i][j-1] + 1,
                             dist[i-1][j-1] + cost)

    # Вычисляем процентное соотношение сходства строк
    return ((len1 + len2) - dist[len1][len2]) / (len1 + len2) * 100


def clean_string(string):
    """
    Функция, которая оставляет только буквы и цифры в строке
    """
    s = string.strip().lower()
    return re.sub(r'[^a-z0-9\s]', ' ', s)


def find_match(string_1, seq):
    """
    Функция для поиска наилучшего совпадения между строками.
    """

    # Удаляем из s1 символы, отличные от букв и цифр и приводим к нижнему регистру
    string_1 = clean_string(string_1)

    # Получаем минимальную длину слова в строке string_1
    min_len = len(min(string_1.split(), key=len))

    # Создаем словарь, в котором каждому слову из строки string_1 присваивается вес
    weights = {}
    for i, word in enumerate(string_1.split()):
        weights[word] = 1.0 / (i + 1)

    # Фильтруем slug, оставляя только те, которые начинаются с бренда из запроса
    filtered_seq = []
    for s in seq:
        # Разбиваем строку на слова и отбираем только те, длина которых не меньше min_len
        words = s.split('-')
        words = [word for word in words if len(word) >= min_len]

        # Удаляем бренд из slug если пользователь его не вводит
        brand = words[0]
        if brand not in string_1:
            words = words[1:]

        # Получаем slug
        slug = ' '.join(words)

        # Если slug начинается с бренда, то оставляем только часть slug после бренда
        if slug.startswith(brand):
            slug = slug[len(brand):].strip()
            # Добавляем отфильтрованный slug в список
            filtered_seq.append(slug)

    # Создаем список возможных вариантов совпадений
    matches = process.extract(string_1, filtered_seq, scorer=string_similarity)

    # Сортируем список возможных вариантов совпадений по убыванию коэффициента схожести
    matches.sort(key=lambda x: x[1], reverse=True)

    # Если список возможных вариантов совпадений не пуст, то выводим первый элемент списка
    if matches:
        return matches[0]





s1 = 'rtx'
seq = ['amd-ryzen-5600x', 'nvidia-geforce-rtx-2060']

print(find_match(s1, seq))