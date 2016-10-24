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

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def add_to_default_permission(sender, **kwargs):
#     members = kwargs["instance"]
#     if kwargs["created"]:
#         permission1 = Permission.objects.get(name='Can add person')
#         permission2 = Permission.objects.get(name='Can change person')
#         permission3 = Permission.objects.get(name='Can add children')
#         permission4 = Permission.objects.get(name='Can change children')
#         permission5 = Permission.objects.get(name='Can delete children')
#         members.permissions = [permission1, permission2,permission3,permission4,permission5]