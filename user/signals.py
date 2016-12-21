from django.contrib.auth.signals import (
    user_logged_in, user_logged_out)
from django.contrib.messages import success
from django.dispatch import receiver



@receiver(user_logged_in)
def display_login_message(sender, **kwargs):
    request = kwargs.get('request')
    user = kwargs.get('user')
    success(
        request,
        "Successfully logged in as {}".format(
            user.get_short_name()),
        fail_silently=True)


@receiver(user_logged_out)
def display_logout_message(sender, **kwargs):
    request = kwargs.get('request')
    success(
        request,
        "Successfully logged out",
        fail_silently=True)


from django.contrib.auth.models import Group,Permission

from django.conf import settings

from django.db.models.signals import post_save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_default_group(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:

        group, group_created = Group.objects.get_or_create(name='members')
        user.groups.add(group)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_default_permission(sender, **kwargs):
    members = kwargs["instance"]
    if kwargs["created"]:

        #default permissions for members
        permission1 = Permission.objects.get(name='Can add person')
        permission2 = Permission.objects.get(name='Can change person')
        permission3 = Permission.objects.get(name='Can add child')
        permission4 = Permission.objects.get(name='Can change child')
        permission5 = Permission.objects.get(name='Can delete child')
        members, created = Group.objects.get_or_create(name='members')
        members.permissions.add(permission1,permission2,permission3,permission4,permission5)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def add_to_default_permission(sender, **kwargs):
#     managers = kwargs["instance"]
#     if kwargs["created"]:
#
#         #default permissions for managers
#         permission6 = Permission.objects.get(name='Can add blog post')
#         permission7 = Permission.objects.get(name='Can change blog post')
#         permission8 = Permission.objects.get(name='Can view unpublished Post')
#         permission9 = Permission.objects.get(name='Can add constitution')
#         permission10 = Permission.objects.get(name='Can change constitution')
#         permission11 = Permission.objects.get(name='Can add event')
#         permission12 = Permission.objects.get(name='Can change event')
#         permission13 = Permission.objects.get(name='Can add exec member')
#         permission14 = Permission.objects.get(name='Can change exec member')
#         permission15 = Permission.objects.get(name='Can add tag')
#         permission16 = Permission.objects.get(name='Can change tag')
#         permission17= Permission.objects.get(name='Can add gallery')
#         permission18 = Permission.objects.get(name='Can change gallery')
#         permission19 = Permission.objects.get(name='Can delete gallery')
#         managers, created = Group.objects.get_or_create(name='managers')
#         managers.permissions.add(permission6, permission7, permission8, permission9, permission10,
#                                  permission11, permission12, permission13, permission14, permission15,
#                                  permission16, permission17, permission18, permission19)