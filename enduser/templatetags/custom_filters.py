from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def timesince_biggest(value, arg=None):
    """
    Returns the biggest time unit only (e.g., "2 hours" instead of "2 hours, 3 minutes").
    """
    time_difference = timesince(value, arg)
    biggest_unit = time_difference.split(',')[0]
    return biggest_unit