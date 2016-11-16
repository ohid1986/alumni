from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Person, ExecMember, Membership, Constitution, Event, Gallery, Tag, Child
from .forms import MemberForm, ExeCommMemberForm, ConstitutionForm,ChildForm, MembershipForm, TagForm, EventForm, GalleryFormSet

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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

    queryset = (
        Person.objects.all()
            .prefetch_related('child_set')
        # below omitted because of with tag
        # and conditional display based on time
        # .prefetch_related('blog_posts')
    )


class AllMemberListView(generic.ListView):

    model = Person
    paginate_by = 5
    context_object_name = 'persons'

class GeneralMemberView(generic.ListView):

    model = Person
    paginate_by = 5
    context_object_name = 'persons'

    def get_queryset(self):
        queryset = super(GeneralMemberView, self).get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(category__id="1")
        return queryset

    #
class LifeMemberView(generic.ListView):

    model = Person
    paginate_by = 5
    context_object_name = 'persons'

    def get_queryset(self):
        queryset = super(LifeMemberView, self).get_queryset()
        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(category__id="3")
        return queryset

@require_authenticated_permission(
'member.add_person')
class PersonCreate(SuccessMessageMixin,CreateView):

    model = Person
    form_class = MemberForm
    success_message = "%(name)s was added as %(category)s successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

@require_authenticated_permission(
'member.change_person')
class PersonUpdate(SuccessMessageMixin,UpdateView):

    model = Person
    form_class = MemberForm
    success_message = "%(category)s: %(name)s was updated successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


@require_authenticated_permission(
'member.delete_person')
class PersonDelete(DeleteView):
    model = Person
    success_url = '/allmember/'

    success_message = "%(category)s: %(name)s was deleted successfully."


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PersonDelete, self).delete(request, *args, **kwargs)


from .utils import (ChildrenGetObjectMixin,
    PersonContextMixin)


# Children

@require_authenticated_permission(
'member.add_child')
class ChildCreate( SuccessMessageMixin,ChildrenGetObjectMixin,
    PersonContextMixin, CreateView):
    template_name = 'member/children_form.html'
    model = Child
    form_class = ChildForm
    success_message = "Child %(child_name)s was added successfully"

    def get_initial(self):
        person_slug = self.kwargs.get(
            self.person_slug_url_kwarg)
        self.person = get_object_or_404(
            Person, slug__iexact=person_slug)
        initial = {
            self.person_context_object_name:
                self.person,
        }
        initial.update(self.initial)
        return initial



@require_authenticated_permission(
'member.change_child')
class ChildUpdate(SuccessMessageMixin,ChildrenGetObjectMixin,
    PersonContextMixin,UpdateView):
    template_name = 'member/children_form.html'
    model = Child
    form_class = ChildForm
    slug_url_kwarg = 'children_slug'
    success_message = "Child %(child_name)s was updated successfully"


@require_authenticated_permission(
'member.delete_child')
class ChildDelete(ChildrenGetObjectMixin,
    PersonContextMixin,DeleteView):
    model = Child
    slug_url_kwarg = 'children_slug'
    success_message = "Child was deleted successfully"

    def get_success_url(self):
        return (self.object.person
                .get_absolute_url())

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChildDelete, self).delete(request, *args, **kwargs)

class ChildDetailView(generic.DetailView):
    model = Child


class ChildListView(generic.ListView):
    model = Child


class ExeCommListView(generic.ListView):
    model = ExecMember
    context_object_name = 'members'


@require_authenticated_permission(
'member.add_exec_member')
class ExeCommMembCreate(SuccessMessageMixin,CreateView):
    template_name = 'member/execmember_form.html'
    model = ExecMember
    success_url = '/execomember/'
    form_class = ExeCommMemberForm
    success_message = "%(committe_period)s %(committee_position)s was added successfully"

    def get_form(self):
        kwargs = super(ExeCommMembCreate, self).get_form()
        return kwargs

class ExeCommMembDetailView(generic.DetailView):
    model = ExecMember

@require_authenticated_permission(
'member.change_exec_member')
class ExeCommMembUpdate(SuccessMessageMixin,UpdateView):
    template_name = 'member/execmember_form.html'
    model = ExecMember
    success_url = '/execomember/'
    form_class = ExeCommMemberForm
    success_message = "%(committe_period)s %(committee_position)s was added successfully"


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
class MemberCatCreate(SuccessMessageMixin,CreateView):
    template_name = 'member/membership_form.html'
    model = Membership
    success_url = '/membercat/'
    form_class = MembershipForm
    success_message = "%(category)s was added successfully"

#Constitution

class ConstitutionView(generic.ListView):
    model = Constitution
    context_object_name = 'documents'

@require_authenticated_permission(
'member.add_constitution')
class ConstitutionCreate(SuccessMessageMixin,CreateView):

    model = Constitution
    form_class = ConstitutionForm
    success_url = '/cons/'
    success_message = "%(title)s was added successfully"

@require_authenticated_permission(
'member.delete_constitution')
class ConstitutionDelete(DeleteView):
    model = Constitution
    success_url = '/cons/'

    success_message = "Constitution was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ConstitutionDelete, self).delete(request, *args, **kwargs)


@require_authenticated_permission(
'member.change_constitution')
class ConstitutionUpdate(SuccessMessageMixin,UpdateView):

    model = Constitution
    success_url = '/cons/'
    form_class = ConstitutionForm
    success_message = "%(title)s was updated successfully"


#Event and Gallery
@require_authenticated_permission(
'member.add_event')
class EventCreateView(FormsetMixin, CreateView):
    template_name = 'member/event_and_gallery_form.html'
    model = Event
    form_class = EventForm
    formset_class = GalleryFormSet
    success_message = "%(name)s was added successfully"

@require_authenticated_permission(
'member.change_event')
class EventUpdateView(FormsetMixin, UpdateView):
    template_name = 'member/event_and_gallery_form.html'
    is_update_view = True
    model = Event
    form_class = EventForm
    formset_class = GalleryFormSet
    success_message = "%(name)s was updated successfully"


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
class TagCreate(SuccessMessageMixin,CreateView):
    form_class = TagForm
    model = Tag
    success_message = "%(name)s was added successfully"


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
class TagUpdate(SuccessMessageMixin,UpdateView):
    form_class = TagForm
    model = Tag
    success_url = '/tag/'
    success_message = "%(name)s was updated successfully"