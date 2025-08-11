from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown_highlight')
def markdown_highlight(text):
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    html = md.convert(text)
    return mark_safe(html)