def translate_russian_to_english(text):
    # Создаем словарь русских и английских букв
    russian_to_english = {
        'ф': 'a',
        'и': 'b',
        'с': 'c',
        'в': 'd',
        'у': 'e',
        'ё': 'e',
        'а': 'f',
        'п': 'g',
        'р': 'h',
        'ш': 'i',
        'о': 'j',
        'л': 'k',
        'д': 'l',
        'ь': 'm',
        'т': 'n',
        'щ': 'o',
        'з': 'p',
        'й': 'q',
        'к': 'r',
        'ы': 's',
        'е': 't',
        'г': 'u',
        'м': 'v',
        'ц': 'w',
        'ч': 'x',
        'н': 'y',
        'я': 'z'
    }

    # Пройдемся по каждому символу в строке и заменим его на соответствующую ему букву из словаря
    translated_text = ''
    for char in text.lower():
        if char in russian_to_english:
            translated_text += russian_to_english[char]
        else:
            translated_text += char

    return translated_text



print(translate_russian_to_english('княут'))