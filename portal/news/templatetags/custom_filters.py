from django import template

register = template.Library()


@register.filter()
def currency(value):
    """
    value: значение, к которому нужно применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value}'[:-7]


@register.filter()
def censor(value):
    string = f'{value}'
    str = string.replace('строка', '******')
    return str
