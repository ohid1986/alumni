from django import template

from ..models import Post

register = template.Library()



@register.inclusion_tag('blog/archieve_sidebar.html')
def get_archieve_post():
    post_list = Post.objects.order_by('-pub_date')
    return {'post_list': post_list}