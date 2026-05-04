from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """ takes two input values and returns the product """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
