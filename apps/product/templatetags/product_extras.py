from django import template

register = template.Library()


@register.filter
def get_list(request_get, key):
    """
    Возвращает список полученного из request_get по ключу key
    """
    return request_get.getlist(key)


@register.simple_tag
def get_comparison_url(request, product):
    url = product.get_comparison_url()
    pass


@register.filter(name='min')
def get_min(seq: list[int]) -> int:
    return min(seq)


@register.filter(name='max')
def get_max(seq: list[int]) -> int:
    return max(seq)
