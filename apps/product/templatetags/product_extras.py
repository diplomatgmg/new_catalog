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
