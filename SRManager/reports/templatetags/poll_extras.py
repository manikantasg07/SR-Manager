from django import template
from datetime import date

register = template.Library()


@register.filter
def is_today(value):
    if isinstance(value, date):
        return value == date.today()
    return False