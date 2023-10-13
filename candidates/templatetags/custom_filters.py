# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_first_name(value):
    return value.split(' ')[0]
