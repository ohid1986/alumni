from django import forms
from django.forms import ModelForm,Textarea
from pagedown.widgets import PagedownWidget
from django.forms.models import inlineformset_factory
from crispy_forms.bootstrap import InlineField
from django.forms.widgets import HiddenInput

from crispy_forms.layout import Field, Layout, ButtonHolder, Submit, Div,Fieldset

from crispy_forms.helper import FormHelper

from .models import Person, ExecMember, Membership, Child, Constitution,  Event, Gallery, Tag


from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

from django.utils.translation import ugettext_lazy as _


from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

# for Land phone


from django.contrib.auth import get_user
from datetime import date
from crispy_forms.bootstrap import TabHolder, Tab

from django.template.defaultfilters import slugify
from crispy_forms.bootstrap import TabHolder, Tab,AppendedText, PrependedText, FormActions

from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field



class SlugCleanMixin:
    """Mixin class for slug cleaning method."""

    def clean_slug(self):
        new_slug = (
            self.cleaned_data['slug'].lower())
        if new_slug == 'create':
            raise ValidationError(
                'Slug may not be "create".')
        return new_slug

class MemberForm(ModelForm):
    birth_date = forms.DateField(('%d/%m/%Y',), label='Birth Date', required=True,
                                 widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                     'class': 'input',
                                     'size': '15'})
                                 )
    class Meta:
        model = Person
        exclude =('user',)
        widgets = {
            'tele_land': forms.TextInput(attrs={'placeholder': 'Start with ' + ', e.g., +8802...'}),
            'tele_cell': forms.TextInput(attrs={'placeholder': 'Start with ' + ', e.g., +8802...'}),

        }

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Your full name. 100 characters.'
        self.fields['tele_land'].label = 'Land phone'
        self.fields['tele_cell'].label = 'Cell phone'
        self.fields['passing_year'].label = 'Passing year'
        self.fields['passing_year'].help_text = 'According to your session year'

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # TabHolder(
            #     Tab(
            #         'Basic Information','name','name_in_bangla','nick_name','birth_date','blood_group','photo',
            #         'category', 'is_active',
            #     ),
            #     Tab('Adress',
            #         'present_address',
            #         'permanent_address',
            #         'tele_land','tele_cell',
            #         ),
            #     Tab('Academic Information',
            #         'admission_session',
            #         'degree_obtained',
            #         'passing_year',
            #         ),
            #     Tab('Official Information',
            #         'profession', 'Designation', 'organization', 'official_address', 'office_phone', 'office_mobile',
            #         'office_email', 'office_fax', ' website',),
            #
            #     Tab('Payment Information',
            #
            #         'payment_number', 'bank_name', 'branch_name',
            #         ),
            #     Tab(
            #         'Personal Information',
            #         'father_name','mother_name','is_married','national_id_no','passport_no','spouse_name','spouse_blood_group',
            #     ),
            # ),

            Div(
                Div(HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Basic Information</span>"""),'name', 'name_in_bangla', 'nick_name', 'birth_date','blood_group',HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Adress</span>"""),'present_address','permanent_address','tele_land','tele_cell','photo',HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Academic Information</span>"""),'admission_session','degree_obtained','passing_year', 'category','is_active', HTML("""<label>Membership Registration fee: 1,000/-</label>"""),HTML('<br>Payment should be made by Pay Order/ Cash in favour of ACCE ALUMNI ASSOCIATION.<br>Bank Account: ACCEAA, D.U. NO.0200003149763<br>Agrani Bank, D.U. Branch, Dhaka.'),css_class='col-md-5'),
                Div(css_class='col-xs-2'),
                Div(HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Payment Information</span>"""),'payment_number','bank_name','branch_name',HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Official Information</span>"""),'profession', 'Designation', 'organization', 'official_address','office_phone', 'office_mobile','office_email','office_fax',' website',HTML("""<span style="font-size: 150%; alignment:left; color:#009933;">Personal Information</span>"""),'father_name','mother_name','is_married','national_id_no','passport_no','spouse_name','spouse_blood_group', css_class='col-md-5'), css_class='row-crispy'
            ),
            # Div(
            #     Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            # )
        )


    def clean(self):
        user = get_user(self.request)
        name = self.cleaned_data.get('name')
        birth_date = self.cleaned_data.get('birth_date')
        if self.instance.id:
            if Person.objects.filter(user=user).exclude(id=self.instance.id).exists():
                self.add_error('name', "You already submitted data")
            elif Person.objects.filter(name=name, birth_date=birth_date).exclude(id=self.instance.id).exists():
                self.add_error('name', "Person with this Name and Birth date already exists.")
        else:
            if Person.objects.filter(user=user).exists():
                self.add_error('name', "You already submitted data")
            elif Person.objects.filter(name=name, birth_date=birth_date).exists():
                self.add_error('name', "Person with this Name and Birth date already exists.")
        return self.cleaned_data

    def save(self, commit=True):
        person = super().save(commit=False)
        if not person.pk:
            person.user = get_user(self.request)
        if commit:
            person.save()
            self.save_m2m()
        return person


class ChildForm(SlugCleanMixin, forms.ModelForm):
    child_birth_date = forms.DateField(('%d/%m/%Y',), label='Birth Date', required=True,
                                       widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                           'class': 'input',
                                           'size': '15'
                                       })
                                       )

    class Meta:
        model = Child
        fields = ('person','child_name', 'slug', 'child_birth_date', 'blood_group')
        widgets = {'person': HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'POST'
        self.helper.form_tag = True


        self.helper.layout = Layout(
            'child_name',
            Field('slug', readonly=True),
            'child_birth_date',
            'blood_group',

            Div(
                Div(Submit('save', 'Save'), css_class='col-md-12'), css_class='row'
            ),
        )



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
            'rank': forms.TextInput(attrs={'placeholder': 'Rank order 1.2.3... in Exe. Comm.'}),

        }

    def __init__(self, *args, **kwargs):
        super(ExeCommMemberForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Person.objects.filter(category__id="2")


        self.helper = FormHelper()


        self.helper.form_method = 'POST'
        self.helper.form_tag = True

        self.helper.layout = Layout(


            Div(
                Div('name', 'committee_position', 'committe_period', css_class='col-md-5'),
                Div(css_class='col-md-1'),
                Div('rank','member_start_date', 'member_end_date', 'is_active', css_class='col-md-5'), css_class='row-crispy'
            ),
            Div(
                Div(Submit('save', 'Save'), css_class='col-md-7'), css_class='row'
            )

        )

from crispy_forms.bootstrap import  FormActions


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
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('tags'),
        )
        self.helper.layout.append(Submit('save', 'Save'))

    class Meta:
        model = Event
        fields = ('name','description','tags', )

class GalleryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.form.method = 'post'
        self.helper.form.action = ''
        self.helper.layout = Layout(
            'title',
            Field('slug', readonly=True),
            'image',

        )

    class Meta:
        model= Gallery
        fields = ('title', 'slug', 'event',  'image')

# GalleryFormSet = inlineformset_factory(Event, Gallery, form=GalleryForm, extra=1, widgets={
#             'slug': forms.TextInput(attrs={'readonly': 'readonly'}), })
GalleryFormSet = inlineformset_factory(Event, Gallery, extra=0, min_num=1, fields=('title', 'slug', 'image' ),widgets = {
            'slug': forms.TextInput(attrs={'readonly':'readonly'}), })
formset = GalleryFormSet()


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