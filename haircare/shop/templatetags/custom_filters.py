from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(int(key))

@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide value by arg"""
    try:
        return int(value) / int(arg) if int(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0