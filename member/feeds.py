from datetime import datetime

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import (
    Atom1Feed, Rss201rev2Feed)

from .models import Event


class BaseEventFeedMixin():

    def description(self, event):
        return "Gallery related to {}".format(
            event.name)

    def get_object(self, request, event_slug):
        # equivalent to GCBV get() method
        return get_object_or_404(
            Event,
            slug__iexact=event_slug)

    def items(self, event):
        return event.gallery_set.all()[:10]

    def item_image(self, gallery):
        return gallery.image

    def item_title(self, gallery):
        return gallery.title

    def link(self, event):
        return event.get_absolute_url()

    def subtitle(self, event):
        return self.description(event)

    def title(self, event):
        return event.name


class AtomEventFeed(BaseEventFeedMixin, Feed):
    feed_type = Atom1Feed


class Rss2EventFeed(BaseEventFeedMixin, Feed):
    feed_type = Rss201rev2Feed