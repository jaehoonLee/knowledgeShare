from django import template

register = template.Library()

@register.filter
def lookupfor(d, key):
    return d[key-1]

@register.filter
def get_at_index(list, index):
    return list[index]
