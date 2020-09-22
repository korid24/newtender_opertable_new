from django import template

register = template.Library()


@register.filter(name='absolute')
def absolute(value):
    return abs(int(value*100) / 100)
