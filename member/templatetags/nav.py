from django.core.urlresolvers import resolve, Resolver404
from django.template import Library

register = Library()

@register.simple_tag
def active_page(request, view_name):
    path = resolve(request.path_info)
    if not request:
        return ""
    try:
        return "active" if path.url_name == view_name else ""
    except Resolver404:
        return ""


