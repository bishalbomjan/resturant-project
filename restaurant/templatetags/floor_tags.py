from django import template
import math

register = template.Library()

@register.filter(name='floor')
def floor(value):
    val=value%1
    if val<= 0.5:
        return math.floor(value)
    else:
        return math.ceil(value)

