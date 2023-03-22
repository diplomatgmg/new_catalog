from django import template

register = template.Library()


@register.filter
def get_list(request, key):
    """
    Возвращает список полученного из request_get по ключу key
    """
    return request.GET.getlist(key)


@register.filter(name='min')
def get_min(seq: list[int]) -> int:
    return min(seq) if seq else None


@register.filter(name='max')
def get_max(seq: list[int]) -> int:
    return max(seq) if seq else None


@register.filter
def get(dictionary: dict, key: str) -> str:
    return dictionary.get(key)


@register.filter
def add_min_max(field_key, min_max):
    if 'min' == min_max:
        return f'{field_key}_min'
    elif 'max' == min_max:
        return f'{field_key}_max'
