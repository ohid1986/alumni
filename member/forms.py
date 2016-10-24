from django import forms
from django.forms import ModelForm,Textarea
from pagedown.widgets import PagedownWidget
from django.forms.models import inlineformset_factory
from crispy_forms.bootstrap import InlineField

from crispy_forms.layout import Field, Layout, ButtonHolder, Submit, Div

from crispy_forms.helper import FormHelper

from .models import Person, ExecMember, Membership, Children, Constitution,  Event, Gallery, Tag
from django.conf import settings

from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

from django.utils.translation import ugettext_lazy as _


from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

# for Land phone


from django.contrib.auth import get_user
from datetime import date
from crispy_forms.bootstrap import TabHolder, Tab

DUPLICATE_ITEM_ERROR = "You've already submitted your data."

class MemberForm(ModelForm):

    birth_date = forms.DateField(('%d/%m/%Y',), label='Birth Date', required=False,
                                 widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                     'class': 'input',
                                     'size': '15'                                 })
                                 )


    class Meta:
        model = Person
        exclude = ('user',)
        widgets = {
            'tele_land': forms.TextInput(attrs={'placeholder': 'Start with '+', e.g., +8802...'}),
            'tele_cell': forms.TextInput(attrs={'placeholder': 'Start with ' + ', e.g., +8802...'}),

        }



    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Your full name'
        self.fields['tele_land'].label = 'Land phone'
        self.fields['tele_cell'].label = 'Cell phone'
        self.fields['passing_year'].label = 'Passing year'
        self.fields['passing_year'].help_text = 'According to your session year'


    # def validate_unique(self, *args, **kwargs):
    #     try:
    #         self.instance.validate_unique()
    #     except ValidationError:
    #         the_url = Person.objects.get(user=self.instance.user).get_absolute_url()
    #         msg = '<a href="{0}">An instance already exists.</a>'.format(the_url)
    #         self.add_error(None, mark_safe(msg))


    def save(self, request, commit=True):
        person = super().save(commit=False)
        if not person.pk:
            person.user = get_user(request)
        if commit:
            person.save()
            self.save_m2m()
        return person

class ChildrenForm(ModelForm):
    child_birth_date = forms.DateField(('%d/%m/%Y',), label='Birth Date', required=True,
                                   widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                       'class': 'input',
                                       'size': '15'
                                   })
                                   )
    class Meta:
        model = Children
        # exclude = ('person',)
        fields = ('person','child_name', 'child_birth_date','blood_group')
        widgets = {
            'person': forms.TextInput(attrs={'placeholder': 'Select Parent Name'}),

        }



ChildrenFormSet = inlineformset_factory(Person, Children, extra=0, min_num=1, fields=('child_name', 'child_birth_date','blood_group' ))
# Tag

class ExeCommMemberForm(ModelForm):
    member_start_date = forms.DateField(('%d/%m/%Y',), label='Start Date of Membership', required=True,
                                 widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                     'class': 'input',
                                     'size': '15'
                                 })
                                 )
    member_end_date = forms.DateField(('%d/%m/%Y',), label='End Date of Membership', required=False,
                                        widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                            'class': 'input',
                                            'size': '15'
                                        })
                                        )


    class Meta:
        model = ExecMember
        fields = '__all__'
        widgets = {
            'committee_position': forms.TextInput(attrs={'placeholder': 'Designation in Exe. Comm.'}),
            'rank': forms.TextInput(attrs={'placeholder': 'Rank order in Exe. Comm.'}),

        }

    def __init__(self, *args, **kwargs):
        super(ExeCommMemberForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Person.objects.filter(category__id="2")


class MembershipForm(ModelForm):

    class Meta:
        model = Membership
        fields = '__all__'

class ConstitutionForm(ModelForm):

    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Constitution
        fields = [
            'title',
            'content',
            'docfile',

        ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','description','tags', )

class GalleryForm(ModelForm):
    class Meta:
        model= Gallery
        fields = ('title', 'event',  'image')




GalleryFormSet = inlineformset_factory(Event, Gallery, extra=0, min_num=1, fields=('title', 'image' ))





# Tag

class SlugCleanMixin:
    """Mixin class for slug cleaning method."""

    def clean_slug(self):
        new_slug = (
            self.cleaned_data['slug'].lower())
        if new_slug == 'create':
            raise ValidationError(
                'Slug may not be "create".')
        return new_slug

class TagForm(
        SlugCleanMixin, forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()