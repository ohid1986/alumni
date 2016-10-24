# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 07:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_persons', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
