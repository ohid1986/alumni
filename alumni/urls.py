"""alumni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from  django.conf.urls.static import static


from django.views.generic import (
    RedirectView, TemplateView)

from member import urls as member_urls
from contact import urls as contact_urls
from user import urls as user_urls
from blog import urls as blog_urls


from blog.feeds import AtomPostFeed, Rss2PostFeed

from django.contrib.sitemaps import views

from django.contrib.sitemaps.views import sitemap

from django.contrib.sitemaps.views import (
    index as site_index_view,
    sitemap as sitemap_view)

from .sitemaps import sitemaps



sitenews = [
    url(r'^atom/$',
        AtomPostFeed(),
        name='blog_atom_feed'),
    url(r'^rss/$',
        Rss2PostFeed(),
        name='blog_rss_feed'),
]

urlpatterns = [


    url(r'^about/$',
        TemplateView.as_view(
            template_name='site/about.html'),
        name='about_site'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include(blog_urls)),
    url(r'^contact/', include(contact_urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        sitemap_view,
        {'sitemaps': sitemaps},
        name='sitemap-sections'),

    url(r'^sitenews/', include(sitenews)),
    url(r'^', include(member_urls)),


    url(r'^user/',
        include(
            user_urls,
            app_name='user',
            namespace='dj-auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







