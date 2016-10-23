# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 04:32
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import s3direct.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Resource')),
                ('limit_date', models.DateField(verbose_name='Deliver Date')),
                ('all_students', models.BooleanField(default=False, verbose_name='All Students')),
                ('students', models.ManyToManyField(related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='Students')),
            ],
            bases=('core.resource',),
        ),
        migrations.CreateModel(
            name='ActivityFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', s3direct.fields.S3DirectField()),
                ('name', models.CharField(max_length=100)),
                ('diet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='courses.Activity')),
            ],
            options={
                'verbose_name_plural': 'Activitys Files',
                'verbose_name': 'Activity File',
            },
        ),
        migrations.CreateModel(
            name='CategorySubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('objectivies', models.TextField(blank=True, verbose_name='Objectivies')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('max_students', models.PositiveIntegerField(blank=True, verbose_name='Maximum Students')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('init_register_date', models.DateField(verbose_name='Register Date (Begin)')),
                ('end_register_date', models.DateField(verbose_name='Register Date (End)')),
                ('init_date', models.DateField(verbose_name='Begin of Course Date')),
                ('end_date', models.DateField(verbose_name='End of Course Date')),
                ('image', models.ImageField(blank=True, upload_to='courses/', verbose_name='Image')),
                ('public', models.BooleanField(verbose_name='Public')),
            ],
            options={
                'verbose_name_plural': 'Courses',
                'verbose_name': 'Course',
                'ordering': ('create_date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='FileMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LinkMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.URLField(max_length=300, verbose_name='Link')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('resource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Resource')),
                ('all_students', models.BooleanField(default=False, verbose_name='All Students')),
                ('students', models.ManyToManyField(related_name='materials', to=settings.AUTH_USER_MODEL, verbose_name='Students')),
            ],
            bases=('core.resource',),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('init_date', models.DateField(verbose_name='Begin of Subject Date')),
                ('end_date', models.DateField(verbose_name='End of Subject Date')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date of last update')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_category', to='courses.CategorySubject', verbose_name='Category')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='courses.Course', verbose_name='Course')),
                ('professors', models.ManyToManyField(related_name='professors_subjects', to=settings.AUTH_USER_MODEL, verbose_name='Professors')),
                ('students', models.ManyToManyField(blank=True, related_name='subject_student', to=settings.AUTH_USER_MODEL, verbose_name='Students')),
            ],
            options={
                'verbose_name_plural': 'Subjects',
                'verbose_name': 'Subject',
                'ordering': ('create_date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('subjects', models.ManyToManyField(to='courses.Subject')),
            ],
            options={
                'verbose_name_plural': 'subject categories',
                'verbose_name': 'subject category',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date of last update')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name_plural': 'Topics',
                'verbose_name': 'Topic',
                'ordering': ('create_date', 'name'),
            },
        ),
        migrations.AddField(
            model_name='material',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.Topic', verbose_name='Topic'),
        ),
        migrations.AddField(
            model_name='linkmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_link', to='courses.Material', verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='filematerial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_file', to='courses.Material', verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_category', to='courses.CourseCategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='course',
            name='professors',
            field=models.ManyToManyField(related_name='courses_professors', to=settings.AUTH_USER_MODEL, verbose_name='Professors'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses_student', to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='activity',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='courses.Topic', verbose_name='Topic'),
        ),
    ]
