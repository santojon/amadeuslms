# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-22 20:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='title',
        ),
    ]
