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