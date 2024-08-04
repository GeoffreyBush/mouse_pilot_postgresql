from django import template

register = template.Library()

@register.inclusion_tag('filter_form.html')
def render_filter_form(filter_form):
    return {'filter_form': filter_form}