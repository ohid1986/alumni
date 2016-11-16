from django.shortcuts import get_object_or_404,render
from django.db import IntegrityError

from django.shortcuts import redirect
from django.http import (
    Http404, HttpResponseRedirect)

from django.http import HttpResponse

from .models import Event, Person, Child

class ChildrenFormMixin():

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            self.person = get_object_or_404(
                Person,
                slug__iexact=self.kwargs.get(
                    self.person_slug_url_kwarg))
            data = kwargs['data'].copy()
            data.update({'person': self.person})
            kwargs['data'] = data
        return kwargs

class ChildrenGetObjectMixin():

    def get_object(self, queryset=None):
        person_slug = self.kwargs.get(
            self.person_slug_url_kwarg)
        child_slug = self.kwargs.get(
            self.slug_url_kwarg)
        return get_object_or_404(
            Child,
            slug__iexact=child_slug,
            person__slug__iexact=person_slug)

class PersonContextMixin():
    person_slug_url_kwarg = 'person_slug'
    person_context_object_name = 'person'

    def get_context_data(self, **kwargs):

        person_slug = self.kwargs.get(
            self.person_slug_url_kwarg)
        person = get_object_or_404(
            Person, slug__iexact=person_slug)
        context = {
            self.person_context_object_name:
                person,
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save(self.request)
        formset.instance = self.object
        formset.save()
        try:
            return redirect(self.object.get_absolute_url())
        except IntegrityError:
            return HttpResponse("ERROR: Your data already exists!")


    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))




class PostFormValidMixin:

    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(
            self.get_success_url())

class PageLinksMixin:
    page_kwarg = 'page'

    def _page_urls(self, page_number):
        return "?{pkw}={n}".format(
            pkw=self.page_kwarg,
            n=page_number)

    def first_page(self, page):
        # don't show on first page
        if page.number > 1:
            return self._page_urls(1)
        return None

    def previous_page(self, page):
        if (page.has_previous()
                and page.number > 2):
            return self._page_urls(
                page.previous_page_number())
        return None

    def next_page(self, page):
        last_page = page.paginator.num_pages
        if (page.has_next()
                and page.number < last_page - 1):
            return self._page_urls(
                page.next_page_number())
        return None

    def last_page(self, page):
        last_page = page.paginator.num_pages
        if page.number < last_page:
            return self._page_urls(last_page)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs)
        page = context.get('page_obj')
        if page is not None:
            context.update({
                'first_page_url':
                    self.first_page(page),
                'previous_page_url':
                    self.previous_page(page),
                'next_page_url':
                    self.next_page(page),
                'last_page_url':
                    self.last_page(page),
            })
        return context


class EventContextMixin():
    event_slug_url_kwarg = 'event_slug'
    event_context_object_name = 'event'

    def get_context_data(self, **kwargs):
        if hasattr(self, 'event'):
            context = {
                self.event_context_object_name:
                    self.event,
            }
        else:
            event_slug = self.kwargs.get(
                self.event_slug_url_kwarg)
            event = get_object_or_404(
                Event,
                slug__iexact=event_slug)
            context = {
                self.event_context_object_name:
                    event,
            }
        context.update(kwargs)
        return super().get_context_data(**context)


