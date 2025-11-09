from django import template
register = template.Library()

@register.filter
def get_range(value, max_value):
    if not max_value:
        return range(1)
    return range(1, max_value + 1)

@register.filter
def star_type(rating, index):
    try:
        r = float(rating)
        i = int(index)
    except Exception:
        return "empty"
    if r >= i:
        return "full"
    if r >= i - 0.5:
        return "half"
    return "empty"