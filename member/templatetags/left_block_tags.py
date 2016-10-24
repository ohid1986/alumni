from django import template

from ..models import Gallery

register = template.Library()

@register.inclusion_tag('member/latest_event.html')
def get_latest_event():
    gallery_list = Gallery.objects.order_by('-pub_date')[:1]
    return {'gallery_list': gallery_list}