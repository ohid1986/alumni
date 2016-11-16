from django.db import models
from django.core.urlresolvers import reverse
from .file_validators import file_size, validate_file_extension
from django.conf import settings

from django.core.validators import RegexValidator

from django.utils.functional import cached_property

from django_resized import ResizedImageField
from autoslug import AutoSlugField

import datetime
from datetime import date
# Create your models here.
phone_regex = RegexValidator(regex=r'^\+(?:[0-9]●?){6,14}[0-9]$',
                                 message="Phone number format: '+999999999'. Up to 15 digits allowed.")

# r'^\+?1?\d{9,15}$'
class PersonManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

DEGREE_CHOICES = (
    ("B.Sc(Hons)", "B.Sc(Hons)"),
    ("M.Sc", "M.Sc"),
    ("M.S", "M.S"),
    ("M.Phil", "M.Phil"),
    ("PhD", "PhD"),
        )
class Person(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(1970, datetime.date.today().year + 1)]
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    name_in_bangla = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=3,validators=[RegexValidator(
                regex='^(A|B|AB|O)[+-]$',message='Blood group must be A|B|AB|O[+/-] format',),],)
    present_address = models.CharField(max_length=250, blank=True)
    permanent_address = models.CharField(max_length=250, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='member_persons')
    tele_land = models.CharField(max_length=15, validators=[phone_regex],blank=True)
    tele_cell = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    photo = ResizedImageField(size=[70, 70],crop=['middle', 'center'],upload_to='persons/%Y/%m/%d/',null=True,
        blank=True,
        editable=True,
        help_text="Person Picture", validators=[file_size])

    admission_session = models.CharField(max_length=9, validators=[RegexValidator(
                regex='^(\d{4}-(\d{2}|\d{4}))$',message='Session format yyyy-yyyy not comply.',),],)
    degree_obtained = models.CharField(max_length=9,
                  choices=DEGREE_CHOICES,default="M.Sc")
    passing_year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    # Official Informantion
    profession = models.CharField(max_length=25)
    Designation = models.CharField(max_length=40, null=True, blank=True)
    organization = models.CharField(max_length=75, blank=True)
    official_address = models.CharField(max_length=250, blank=True)
    office_phone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    office_mobile = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    office_email = models.EmailField(max_length=70, null=True, blank=True)
    office_fax = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    website = models.URLField(max_length=250,blank=True)

    #Bank detail

    payment_number = models.CharField(max_length=60, null=True, blank=True,)
    bank_name = models.CharField(max_length=30, null=True, blank=True,)
    branch_name = models.CharField(max_length=50, null=True, blank=True,)

    # Personal Information
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    is_married = models.BooleanField(default=True)
    national_id_no = models.IntegerField(unique=True)
    passport_no = models.CharField(max_length=15, null=True, blank=True)
    spouse_name = models.CharField(max_length=200, null=True, blank=True)
    spouse_blood_group = models.CharField(max_length=3,validators=[RegexValidator(
                regex='^(A|B|AB|O)[+-]$',message='Blood group must be A|B|AB|O[+/-] format',),],null=True, blank=True)
    category = models.ForeignKey('Membership', on_delete=models.CASCADE)

    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    is_active = models.BooleanField(default=True)

    objects = PersonManager()

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'birth_date']

    def get_absolute_url(self):
        return reverse('member:person-detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('member:person-delete',
                       kwargs={'slug': self.slug})

    def get_child_create_url(self):
        return reverse(
            'member:children-create',
            kwargs={'person_slug': self.slug})

    def get_update_url(self):
        return reverse('member:person-update',
                       kwargs={'slug': self.slug})

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def natural_key(self):
        return (self.slug,)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url


class ChildManager(models.Manager):

    def get_by_natural_key(
            self, person_slug, slug):
        return self.get(
            person__slug=person_slug,
            slug=slug)

class Child(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, help_text='Slug will automaticall created from Child Name. No need to type here.')
    child_birth_date = models.DateField()
    blood_group = models.CharField(max_length=3,validators=[RegexValidator(regex='^(A|B|AB|O)[+-]$',message='Blood group must be A|B|AB|O[+/-] format',),], blank=True)

    objects = ChildManager()

    class Meta:
        verbose_name_plural = 'children'
        ordering = ['-child_birth_date']
        unique_together = ['slug', 'person']



    def __str__(self):
        return "{}: {}".format(
            self.person, self.child_name)

    def get_absolute_url(self):
        return self.person.get_absolute_url()

    def get_delete_url(self):
        return reverse(
            'member:children-delete',
            kwargs={
                'person_slug': self.person.slug,
                'children_slug': self.slug})

    def get_update_url(self):
        return reverse(
            'member:children-update',
            kwargs={
                'person_slug': self.person.slug,
                'children_slug': self.slug})


    def natural_key(self):
        return (
            self.person.natural_key(),
            self.slug)

    natural_key.dependencies = [
        'member.person']

class Membership(models.Model):
    category = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.category


class ExecMember(models.Model):
    name = models.ForeignKey(Person, on_delete=models.CASCADE ,help_text='Select Member Name')
    committee_position = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='committee_position')
    committe_period = models.CharField(max_length=9, validators=[RegexValidator(
        regex='^(\d{4}-(\d{2}|\d{4}))$', message='Period format yyyy-yyyy not comply.', ), ], )
    rank = models.IntegerField()
    member_start_date = models.DateField(blank=True)
    member_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering =['-committe_period','-rank']
        unique_together = ['committe_period', 'rank']

    def get_absolute_url(self):
        return reverse('member:execomember-detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('member:execomember-delete',
                       kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('member:execomember-update',
                       kwargs={'slug': self.slug})

    def __str__(self):  # __unicode__ on Python 2
        return self.committee_position


class Constitution(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title')
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/',null=True,
        blank=True,
        editable=True,
        help_text="Document File", validators=[file_size])


    def get_delete_url(self):
        return reverse('member:cons-delete',
                       kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('member:cons-update',
                       kwargs={'slug': self.slug})

    def __str__(self):  # __unicode__ on Python 2
        return self.title





# Tags
class TagManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Tag(models.Model):
    name = models.CharField(
        max_length=31, unique=True)
    slug = AutoSlugField(populate_from='name')

    objects = TagManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse('member:member_tag_detail',
                       kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('member:member_tag_delete',
                       kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('member:member_tag_update',
                       kwargs={'slug': self.slug})

    @cached_property
    def published_posts(self):
        return tuple(self.blog_posts.filter(
            pub_date__lt=date.today()))

    def natural_key(self):
        return (self.slug,)
# Event

class EventManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Event(models.Model):
    name = models.CharField(
        max_length=65,unique=True, db_index=True)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()
    created = models.DateField('date created', auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = EventManager()

    class Meta:
        ordering = ['name']
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('member:event-detail',
                       kwargs={'slug': self.slug})


    def get_delete_url(self):
        return reverse('member:event-delete',
                       kwargs={'slug': self.slug})

    def get_feed_atom_url(self):
        return reverse(
            'member:member_event_atom_feed',
            kwargs={'event_slug': self.slug})

    def get_feed_rss_url(self):
        return reverse(
            'member:member_event_rss_feed',
            kwargs={'event_slug': self.slug})



    def get_update_url(self):
        return reverse('member:update_event_and_gallery',
                       kwargs={'slug': self.slug})

    @cached_property
    def published_posts(self):
        return tuple(self.blog_posts.filter(
            pub_date__lt=date.today()))

    def natural_key(self):
        return (self.slug,)


class GalleryManager(models.Manager):

    def get_by_natural_key(
            self, event_slug, slug):
        return self.get(
            event__slug=event_slug,
            slug=slug)

class Gallery(models.Model):
    title = models.CharField(max_length=35)
    slug = models.SlugField(max_length=35)
    event = models.ForeignKey(Event, on_delete=models.CASCADE )
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    image = models.ImageField(upload_to='events/%Y/%m/%d/', null=True,
                              blank=True,
                              editable=True,
                              help_text="Event Picture", validators=[file_size], width_field="width", height_field="height")
    pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = GalleryManager()

    class Meta:
        verbose_name = 'gallery event'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'event')

    def __str__(self):
        return "{}: {}".format(
            self.event, self.title)

    def get_absolute_url(self):
        return reverse('member:gallery-detail', kwargs={'slug': self.slug})



