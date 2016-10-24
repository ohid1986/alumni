from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from blog.sitemaps import (
    PostArchiveSitemap, PostSitemap)
from member.sitemaps import (
    EventSitemap, TagSitemap)


class RootSitemap(Sitemap):
    priority = 0.6

    def items(self):
        return [
            'about_site',
            'blog_post_list',
            'contact',
            'dj-auth:login',
            'member:event-list',
            'member:member_tag_list',
        ]

    def location(self, url_name):
        return reverse(url_name)


sitemaps = {
    'post-archives': PostArchiveSitemap,
    'posts': PostSitemap,
    'roots': RootSitemap,
    'events': EventSitemap,
    'tags': TagSitemap,
}


