from django import template

register = template.Library()


@register.simple_tag()
def define(value):
    return value

@register.simple_tag()
def assign(**kwargs):
    return kwargs['var']