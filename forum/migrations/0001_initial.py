# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-13 17:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.Activity')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='Modification Date')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Foruns',
            },
            bases=('courses.activity',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Post message')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='Modification Date')),
                ('post_date', models.DateTimeField(auto_now_add=True, verbose_name='Post Date')),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Forum', verbose_name='Forum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Answer message')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='Modification Date')),
                ('answer_date', models.DateTimeField(auto_now_add=True, verbose_name='Answer Date')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post', verbose_name='Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={
                'verbose_name': 'Post Answer',
                'verbose_name_plural': 'Post Answers',
            },
        ),
    ]
