"""ext tags."""
from django import template

register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag('layout/left-menu.html', takes_context=True)
def render_xcrm_menu(context):
    request = context['request']

    context['menu_list'] = []

    return context
