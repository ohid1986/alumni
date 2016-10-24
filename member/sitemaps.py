from django.contrib.sitemaps import (
    GenericSitemap, Sitemap)

from .models import Event, Tag

tag_sitemap_dict = {
    'queryset': Tag.objects.all(),
}


TagSitemap = GenericSitemap(tag_sitemap_dict)


class EventSitemap(Sitemap):

    def items(self):
        return Event.objects.all()

    def lastmod(self, event):
        if event.gallery_set.exists():
            return (
                event.gallery_set.latest()
                .pub_date)
        else:
            return event.created