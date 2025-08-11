import re
from django import template

register = template.Library()

@register.filter
def slugify(value):
    value = value.lower()
    value = re.sub(r'[^\w]+', '-', value)
    return value.strip('-')
