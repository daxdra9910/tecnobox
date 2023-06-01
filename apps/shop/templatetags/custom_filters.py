from django import template

register = template.Library()

@register.filter
def sus(value, arg):
    return value - arg