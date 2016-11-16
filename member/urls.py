from django.conf.urls import url
from . import views

from .feeds import AtomEventFeed, Rss2EventFeed

app_name = 'member'
urlpatterns = [

    url(r'^$', views.HomePageView.as_view(), name='home'),

    # Event and Gallery
    url(r'^gallery/$', views.GalleryList.as_view(), name='gallery-list'),
    url(r'^gallery/(?P<slug>[\w\-]+)/$', views.GalleryDetailView.as_view(), name='gallery-detail'),
    url(r'^event/$', views.EventList.as_view(), name='event-list'),
    url(r'^event/gallery/$', views.EventGalleryListView.as_view(), name='event-gallery'),
    url(r'^event/create/$', views.EventCreateView.as_view(), name='member_event_create'),
    url(r'^event/(?P<slug>[\w\-]+)/$', views.EventDetailView.as_view(), name='event-detail'),
    url(r'^event/(?P<slug>[\w\-]+)/update/$', views.EventUpdateView.as_view(), name='update_event_and_gallery'),
    url(r'^event/(?P<slug>[\w\-]+)/delete/$', views.EventDelete.as_view(), name='event-delete'),

       # Executive Member
    url(r'^execomember/$', views.ExeCommListView.as_view(), name='execomember-list'),
    url(r'^execomember/create/$', views.ExeCommMembCreate.as_view(), name='execomember-create'),
    url(r'^execomember/(?P<slug>[\w\-]+)/$', views.ExeCommMembDetailView.as_view(), name='execomember-detail'),
    url(r'^execomember/(?P<slug>[\w\-]+)/update/$', views.ExeCommMembUpdate.as_view(), name='execomember-update'),
    url(r'^execomember/(?P<slug>[\w\-]+)/delete/$', views.ExeCommMembDelete.as_view(), name='execomember-delete'),

    # Member Category
    url(r'^membercat/$', views.MembershipView.as_view(), name='member-cat'),
    url(r'^membercat/create/$', views.MemberCatCreate.as_view(), name='membercat-create'),

    # Constitution
    url(r'^cons/$', views.ConstitutionView.as_view(), name='cons-list'),
    url(r'^cons/create/$', views.ConstitutionCreate.as_view(), name='cons-create'),
    url(r'^cons/(?P<slug>[\w\-]+)/update/$', views.ConstitutionUpdate.as_view(), name='cons-update'),
    url(r'^cons/(?P<slug>[\w\-]+)/delete/$', views.ConstitutionDelete.as_view(), name='cons-delete'),




    # Search

    url(r'^search/$', views.PersonSearchListView.as_view(), name='search'),

    # Tag
    url(r'^tag/$',
            views.TagList.as_view(),
        name='member_tag_list'),
    url(r'^tag/create/$',
        views.TagCreate.as_view(),
        name='member_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',
        views.TagDetail.as_view(),
        name='member_tag_detail'),
    url(r'^tag/(?P<slug>[\w-]+)/delete/$',
        views.TagDelete.as_view(),
        name='member_tag_delete'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$',
        views.TagUpdate.as_view(),
        name='member_tag_update'),

    # Member
    url(r'^person/$', views.GeneralMemberView.as_view(), name='person-list'),
    url(r'^lifemember/$', views.LifeMemberView.as_view(), name='lifemember-list'),
    url(r'^allmember/$', views.AllMemberListView.as_view(), name='all-member'),
    url(r'^person/create/$', views.PersonCreate.as_view(), name='person-create'),
    url(r'^person/(?P<slug>[\w\-]+)/$', views.PersonDetailView.as_view(), name='person-detail'),
    url(r'^(?P<person_slug>[\w\-]+)/'
        r'add_children_link/$',
        views.ChildCreate.as_view(),
        name='children-create'),
    url(r'^person/(?P<slug>[\w\-]+)/update/$', views.PersonUpdate.as_view(), name='person-update'),
    url(r'^person/(?P<slug>[\w\-]+)/delete/$', views.PersonDelete.as_view(), name='person-delete'),
    url(r'^(?P<person_slug>[\w\-]+)/'
        r'(?P<children_slug>[\w\-]+)/'
        r'delete/$',
        views.ChildDelete.as_view(),
        name='children-delete'),
    url(r'^(?P<person_slug>[\w\-]+)/'
        r'(?P<children_slug>[\w\-]+)/'
        r'update/$',
        views.ChildUpdate.as_view(),
        name='children-update'),

    # Children
    url(r'^child/$', views.ChildListView.as_view(), name='children-list'),
    url(r'^child/(?P<slug>[\w\-]+)/$', views.ChildDetailView.as_view(), name='children-detail'),

    # Event


    url(r'^(?P<event_slug>[\w-]+)/atom/$',
        AtomEventFeed(),
        name='member_event_atom_feed'),

    url(r'^(?P<event_slug>[\w-]+)/rss/$',
        Rss2EventFeed(),
        name='member_event_rss_feed'),

]

