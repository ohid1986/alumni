from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Person, ExecMember, Membership, Constitution, Event, Gallery, Tag, Children
from .forms import MemberForm, ExeCommMemberForm, ConstitutionForm,ChildrenForm, MembershipForm, TagForm, EventForm, GalleryFormSet, ChildrenFormSet

from user.decorators import require_authenticated_permission
from .utils import (FormsetMixin, PostFormValidMixin,  PageLinksMixin,
    EventContextMixin)




class HomePageView(TemplateView):

    template_name = 'member/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['gallery_list'] = Gallery.objects.order_by('-pub_date')[:4]

        return context

class PersonDetailView(generic.DetailView):
    model = Person
    template_name = 'member/person_detail.html'


class AllMemberListView(generic.ListView):
    model = Person
    paginate_by = 10
    context_object_name = 'persons'

class GeneralMemberView(generic.ListView):
    model = Person
    paginate_by = 10
    context_object_name = 'persons'

    def get_queryset(self):
        queryset = super(GeneralMemberView, self).get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(category__id="1")
        return queryset

    #
class LifeMemberView(generic.ListView):
    model = Person

    paginate_by = 10
    context_object_name = 'persons'

    def get_queryset(self):
        queryset = super(LifeMemberView, self).get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(category__id="3")
        return queryset

@require_authenticated_permission(
'member.add_person')
class PersonCreate(FormsetMixin, CreateView):
    template_name = 'member/person_form.html'
    model = Person
    success_url = '/allmember/'
    form_class = MemberForm
    formset_class = ChildrenFormSet




@require_authenticated_permission(
'member.change_person')
class PersonUpdate(FormsetMixin, UpdateView):
    template_name = 'member/person_form.html'
    is_update_view = True
    model = Person
    form_class = MemberForm
    formset_class = ChildrenFormSet

@require_authenticated_permission(
'member.delete_person')
class PersonDelete(DeleteView):
    model = Person
    success_url = '/allmember/'


# Children

@require_authenticated_permission(
'member.add_children')
class ChildrenCreate(CreateView):
    template_name = 'member/children_form.html'
    model = Children
    form_class = ChildrenForm

    success_url = '/children/'

@require_authenticated_permission(
'member.change_children')
class ChildrenUpdate(UpdateView):
    template_name = 'member/children_form.html'
    model = Children
    form_class = ChildrenForm
    # success_url = '/children/'

    def get_success_url(self):
        return (self.object.person
                .get_absolute_url())


@require_authenticated_permission(
'member.delete_children')
class ChildrenDelete(DeleteView):
    model = Children

    def get_success_url(self):
        return (self.object.person
                .get_absolute_url())

class ChildrenDetailView(generic.DetailView):
    model = Children


class ChildrenListView(generic.ListView):
    model = Children


class ExeCommListView(generic.ListView):
    model = ExecMember
    context_object_name = 'members'

@require_authenticated_permission(
'member.add_exec_member')
class ExeCommMembCreate(CreateView):
    template_name = 'member/execmember_form.html'
    model = ExecMember
    success_url = '/execomember/'
    form_class = ExeCommMemberForm

    def get_form(self):
        kwargs = super(ExeCommMembCreate, self).get_form()
        return kwargs

class ExeCommMembDetailView(generic.DetailView):
    model = ExecMember

@require_authenticated_permission(
'member.change_exec_member')
class ExeCommMembUpdate(UpdateView):
    template_name = 'member/execmember_form.html'
    model = ExecMember
    success_url = '/execomember/'
    form_class = ExeCommMemberForm

@require_authenticated_permission(
'member.delete_exec_member')
class ExeCommMembDelete(DeleteView):
    model = ExecMember
    success_url = '/execomember/'

# Member Category

class MembershipView(generic.ListView):
    model = Membership
    context_object_name = 'entries'

@require_authenticated_permission(
'member.add_membership')
class MemberCatCreate(CreateView):
    template_name = 'member/membership_form.html'
    model = Membership
    success_url = '/membercat/'
    form_class = MembershipForm

#Constitution

class ConstitutionView(generic.ListView):
    model = Constitution
    context_object_name = 'documents'

@require_authenticated_permission(
'member.add_constitution')
class ConstitutionCreate(CreateView):
    template_name = 'member/constitution_form.html'
    model = Constitution
    success_url = '/cons/'
    form_class = ConstitutionForm

@require_authenticated_permission(
'member.delete_constitution')
class ConstitutionDelete(DeleteView):
    model = Constitution
    success_url = '/cons/'

@require_authenticated_permission(
'member.change_constitution')
class ConstitutionUpdate(UpdateView):
    template_name = 'member/constitution_form.html'
    model = Constitution
    success_url = '/cons/'
    form_class = ConstitutionForm


#Event and Gallery
@require_authenticated_permission(
'member.add_event')
class EventCreateView(FormsetMixin, CreateView):
    template_name = 'member/event_and_gallery_form.html'
    model = Event
    form_class = EventForm
    formset_class = GalleryFormSet

@require_authenticated_permission(
'member.change_event')
class EventUpdateView(FormsetMixin, UpdateView):
    template_name = 'member/event_and_gallery_form.html'
    is_update_view = True
    model = Event
    form_class = EventForm
    formset_class = GalleryFormSet


class GalleryList(generic.ListView):

    model = Gallery


class GalleryDetailView(generic.DetailView):

    model = Gallery


class EventList(generic.ListView):

    model = Event
    paginate_by = 5


# class EventDetailView(generic.DetailView):
#     model = Event

class EventDetailView(DetailView):
    queryset = (
        Event.objects.all()
        .prefetch_related('tags')

        # below omitted because of with tag
        # and conditional display based on time
        # .prefetch_related('blog_posts')
    )




class EventGalleryListView(generic.ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'member/event_gallery.html'

@require_authenticated_permission(
'member.delete_event')
class EventDelete(DeleteView):

    model = Event
    success_url = '/event/'



#Contact form

import operator

from django.db.models import Q
from functools import reduce
from itertools import chain
from operator import attrgetter





import operator

from django.db.models import Q


class PersonSearchListView(AllMemberListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(PersonSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(present_position__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(address__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(organization__icontains=q) for q in query_list))

            )

        return result


# Tag


@require_authenticated_permission(
    'member.add_tag')
class TagCreate(CreateView):
    form_class = TagForm
    model = Tag


@require_authenticated_permission(
    'member.delete_tag')
class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy(
        'member:member_tag_list')


class TagDetail(DetailView):
    queryset = (
        Tag.objects
        .prefetch_related('event_set')
    )


class TagList(PageLinksMixin, ListView):
    paginate_by = 5
    model = Tag


@require_authenticated_permission(
    'member.change_tag')
class TagUpdate(UpdateView):
    form_class = TagForm
    model = Tag
    success_url = '/tag/'