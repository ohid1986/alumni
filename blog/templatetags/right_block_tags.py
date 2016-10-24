from django import template

from ..models import Post

register = template.Library()



@register.inclusion_tag('blog/latest_news.html')
def get_latest_post():
    post_list = Post.objects.order_by('-pub_date')[:1]
    return {'post_list': post_list}