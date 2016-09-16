from django.utils.translation import ugettext_lazy as _
from django.db import models
from autoslug.fields import AutoSlugField
from users.models import User
from core.models import Resource

class Category(models.Model):

	name = models.CharField(_('Name'), max_length = 100, unique = True)
	slug = AutoSlugField(_("Slug"),populate_from='name',unique=True)
	create_date = models.DateField(_('Creation Date'), auto_now_add = True)

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.name

class Course(models.Model):

	name = models.CharField(_('Name'), max_length = 100)
	slug = AutoSlugField(_("Slug"),populate_from='name',unique=True)
	objectivies = models.TextField(_('Objectivies'), blank = True)
	content = models.TextField(_('Content'), blank = True)
	max_students = models.PositiveIntegerField(_('Maximum Students'), blank = True)
	create_date = models.DateField(_('Creation Date'), auto_now_add = True)
	init_register_date = models.DateField(_('Register Date (Begin)'))
	end_register_date = models.DateField(_('Register Date (End)'))
	init_date = models.DateField(_('Begin of Course Date'))
	end_date = models.DateField(_('End of Course Date'))
	image = models.ImageField(verbose_name = _('Image'), blank = True, upload_to = 'courses/')
	category = models.ForeignKey(Category, verbose_name = _('Category'))
	professors = models.ManyToManyField(User,verbose_name=_('Professors'), related_name='courses')
	students = models.ManyToManyField(User,verbose_name=_('Students'), related_name='courses_student')

	class Meta:
		ordering = ('create_date','name')
		verbose_name = _('Course')
		verbose_name_plural = _('Courses')

	def __str__(self):
		return self.name

class Subject(models.Model):

	name = models.CharField(_('Name'), max_length = 100)
	slug = AutoSlugField(_("Slug"),populate_from='name',unique=True)
	description = models.TextField(_('Description'), blank = True)
	visible = models.BooleanField(_('Visible'), default = False)
	init_date = models.DateField(_('Begin of Subject Date'))
	end_date = models.DateField(_('End of Subject Date'))
	create_date = models.DateTimeField(_('Creation Date'), auto_now_add = True)
	update_date = models.DateTimeField(_('Date of last update'), auto_now=True)
	course = models.ForeignKey(Course, verbose_name = _('Course'), related_name="subjects")
	professors = models.ManyToManyField(User,verbose_name=_('Professors'), related_name='subjects')


	class Meta:
		ordering = ('create_date','name')
		verbose_name = _('Subject')
		verbose_name_plural = _('Subjects')

	def __str__(self):
		return self.name

class Topic(models.Model):

	name = models.CharField(_('Name'), max_length = 100)
	slug = AutoSlugField(_("Slug"),populate_from='name',unique=True)
	description = models.TextField(_('Description'), blank = True)
	create_date = models.DateTimeField(_('Creation Date'), auto_now_add = True)
	update_date = models.DateTimeField(_('Date of last update'), auto_now=True)
	subject = models.ForeignKey(Subject, verbose_name = _('Subject'), related_name="topics")
	owner = models.ForeignKey(User, verbose_name = _('Owner'), related_name="topics")
	visible = models.BooleanField(_('Visible'), default=False)

	class Meta:
		ordering = ('create_date','name')
		verbose_name = _('Topic')
		verbose_name_plural = _('Topics')

	def __str__(self):
		return self.name

"""
It is one kind of possible resources available inside a Topic.
Activity is something that has a deadline and has to be delivered by the student
"""
class Activity(Resource):
	create_date = models.DateTimeField(_('Creation Date'), auto_now_add = True)
	topic = models.ForeignKey(Topic, verbose_name = _('Topic'), related_name="topic")
	create_date = models.DateTimeField(_('Creation Date'), auto_now_add = True)
	limit_date = models.DateTimeField(_('Deliver Date'))
	student = models.ForeignKey(User, verbose_name = _('student'), related_name="student")
	grade = models.IntegerField(_('grade'))

"""
It is one kind of possible resources available inside a Topic.
"""
class Link(Resource):
	url_field = models.CharField(_('url'), max_length= 300)