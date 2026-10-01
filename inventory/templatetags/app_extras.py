from django import template

register = template.Library()


@register.simple_tag
def get_verbose_field_name(object, fileld_name):
    return object._meta.get_field(fileld_name).verbose_name
