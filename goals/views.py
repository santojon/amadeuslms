from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory

from amadeus.permissions import has_subject_permissions, has_resource_permissions

from topics.models import Topic

from .forms import GoalsForm, MyGoalsForm, InlinePendenciesFormset, InlineGoalItemFormset
from .models import Goals, MyGoals

class NewWindowView(LoginRequiredMixin, generic.DetailView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'goals/window_view.html'
	model = Goals
	context_object_name = 'goals'

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		if not has_resource_permissions(request.user, goals):
			return redirect(reverse_lazy('subjects:home'))

		return super(NewWindowView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(NewWindowView, self).get_context_data(**kwargs)
		
		context['title'] = (self.object.name)

		return context

class InsideView(LoginRequiredMixin, generic.ListView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'goals/view.html'
	model = Goals
	context_object_name = 'itens'	

	def get_queryset(self):
		slug = self.kwargs.get('slug', '')
		goal = get_object_or_404(Goals, slug = slug)

		goals = MyGoals.objects.filter(user = self.request.user)

		return goals

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		if not has_resource_permissions(request.user, goals):
			return redirect(reverse_lazy('subjects:home'))

		return super(InsideView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(InsideView, self).get_context_data(**kwargs)

		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		context['title'] = _("My Goals")
		
		context['goal'] = goals
		context['topic'] = goals.topic
		context['subject'] = goals.topic.subject

		return context

class SubmitView(LoginRequiredMixin, generic.edit.CreateView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'goals/submit.html'
	form_class = MyGoalsForm

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		if not has_resource_permissions(request.user, goals):
			return redirect(reverse_lazy('subjects:home'))

		return super(SubmitView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = None
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		MyGoalsFormset = formset_factory(MyGoalsForm, extra = 0)
		my_goals_formset = MyGoalsFormset(initial = [{'item': x.id, 'value': x.ref_value} for x in goals.item_goal.all()])
		
		return self.render_to_response(self.get_context_data(my_goals_formset = my_goals_formset))

	def post(self, request, *args, **kwargs):
		self.object = None
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		MyGoalsFormset = formset_factory(MyGoalsForm, extra = 0)
		my_goals_formset = MyGoalsFormset(self.request.POST, initial = [{'item': x.id, 'value': x.ref_value} for x in goals.item_goal.all()])
		
		if (my_goals_formset.is_valid()):
			return self.form_valid(my_goals_formset)
		else:
			return self.form_invalid(my_goals_formset)

	def form_invalid(self, my_goals_formset):
		return self.render_to_response(self.get_context_data(my_goals_formset = my_goals_formset))

	def form_valid(self, my_goals_formset):
		for forms in my_goals_formset.forms:
			form = forms.save(commit = False)
			form.user = self.request.user

			form.save()

		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(SubmitView, self).get_context_data(**kwargs)

		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		context['title'] = goals.name
		
		context['goals'] = goals
		context['topic'] = goals.topic
		context['subject'] = goals.topic.subject

		return context

	def get_success_url(self):
		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		messages.success(self.request, _('Your goals for %s was save successfully!')%(goals.topic.name))

		success_url = reverse_lazy('goals:view', kwargs = {'slug': slug})

		return success_url

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'goals/create.html'
	form_class = GoalsForm

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		if not has_subject_permissions(request.user, topic.subject):
			return redirect(reverse_lazy('subjects:home'))

		return super(CreateView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = None
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pendencies_form = InlinePendenciesFormset(initial = [{'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]}])
		goalitems_form = InlineGoalItemFormset()

		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form, goalitems_form = goalitems_form))

	def post(self, request, *args, **kwargs):
		self.object = None
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pendencies_form = InlinePendenciesFormset(self.request.POST, initial = [{'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]}])
		goalitems_form = InlineGoalItemFormset(self.request.POST)

		if (form.is_valid() and pendencies_form.is_valid() and goalitems_form.is_valid()):
			return self.form_valid(form, pendencies_form, goalitems_form)
		else:
			return self.form_invalid(form, pendencies_form, goalitems_form)

	def get_initial(self):
		initial = super(CreateView, self).get_initial()

		slug = self.kwargs.get('slug', '')

		topic = get_object_or_404(Topic, slug = slug)
		initial['subject'] = topic.subject
		initial['topic'] = topic
		
		return initial

	def form_invalid(self, form, pendencies_form, goalitems_form):
		for p_form in pendencies_form.forms:
			p_form.fields['action'].choices = [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]

		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form, goalitems_form = goalitems_form))

	def form_valid(self, form, pendencies_form, goalitems_form):
		self.object = form.save(commit = False)

		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		self.object.topic = topic
		self.object.order = topic.resource_topic.count() + 1

		self.object.all_students = True

		if not self.object.topic.visible and not self.object.topic.repository:
			self.object.visible = False

		self.object.save()

		pendencies_form.instance = self.object
		pendencies_form.save(commit = False)
		
		for pform in pendencies_form.forms:
			pend_form = pform.save(commit = False)

			if not pend_form.action == "":
				pend_form.save()

		goalitems_form.instance = self.object
		goalitems_form.save(commit = False)

		g_order = 1

		for gform in goalitems_form.forms:
			goal_form = gform.save(commit = False)

			if not goal_form.description == "":
				goal_form.order = g_order
				goal_form.save()

				g_order += 1
		
		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)

		context['title'] = _('Create Topic Goals')

		slug = self.kwargs.get('slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		context['topic'] = topic
		context['subject'] = topic.subject

		return context

	def get_success_url(self):
		messages.success(self.request, _('The Goals specification for the topic %s was realized successfully!')%(self.object.topic.name))

		success_url = reverse_lazy('goals:submit', kwargs = {'slug': self.object.slug})

		if self.object.show_window:
			self.request.session['resources'] = {}
			self.request.session['resources']['new_page'] = True
			self.request.session['resources']['new_page_url'] = reverse('goals:window_view', kwargs = {'slug': self.object.slug})

			success_url = reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})

		return success_url

class UpdateView(LoginRequiredMixin, generic.UpdateView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'goals/update.html'
	model = Goals
	form_class = GoalsForm
	context_object_name = 'goal'

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		if not has_subject_permissions(request.user, topic.subject):
			return redirect(reverse_lazy('subjects:home'))

		return super(UpdateView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pendencies_form = InlinePendenciesFormset(instance = self.object, initial = [{'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]}])
		goalitems_form = InlineGoalItemFormset(instance = self.object)

		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form, goalitems_form = goalitems_form))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		
		form_class = self.get_form_class()
		form = self.get_form(form_class)

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		pendencies_form = InlinePendenciesFormset(self.request.POST, instance = self.object, initial = [{'subject': topic.subject.id, 'actions': [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]}])
		goalitems_form = InlineGoalItemFormset(self.request.POST, instance = self.object)

		if (form.is_valid() and pendencies_form.is_valid() and goalitems_form.is_valid()):
			return self.form_valid(form, pendencies_form, goalitems_form)
		else:
			return self.form_invalid(form, pendencies_form, goalitems_form)
	
	def form_invalid(self, form, pendencies_form, goalitems_form):
		for p_form in pendencies_form.forms:
			p_form.fields['action'].choices = [("", "-------"),("view", _("Visualize")), ("submit", _("Submit"))]

		return self.render_to_response(self.get_context_data(form = form, pendencies_form = pendencies_form, goalitems_form = goalitems_form))

	def form_valid(self, form, pendencies_form, goalitems_form):
		self.object = form.save(commit = False)

		if not self.object.topic.visible and not self.object.topic.repository:
			self.object.visible = False
		
		self.object.save()

		pendencies_form.instance = self.object
		pendencies_form.save(commit = False)

		for form in pendencies_form.forms:
			pend_form = form.save(commit = False)

			if not pend_form.action == "":
				pend_form.save()

		goalitems_form.instance = self.object
		goalitems_form.save(commit = False)

		g_order = 1

		for gform in goalitems_form.forms:
			goal_form = gform.save(commit = False)

			if not goal_form.description == "":
				goal_form.order = g_order
				goal_form.save()

				g_order += 1
		
		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)

		context['title'] = _('Update Topic Goals')

		slug = self.kwargs.get('topic_slug', '')
		topic = get_object_or_404(Topic, slug = slug)

		context['topic'] = topic
		context['subject'] = topic.subject

		return context

	def get_success_url(self):
		messages.success(self.request, _('The Goals specification for the topic %s was updated successfully!')%(self.object.topic.name))

		success_url = reverse_lazy('goals:submit', kwargs = {'slug': self.object.slug})

		if self.object.show_window:
			self.request.session['resources'] = {}
			self.request.session['resources']['new_page'] = True
			self.request.session['resources']['new_page_url'] = reverse('goals:window_view', kwargs = {'slug': self.object.slug})

			success_url = reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})

		return success_url

class DeleteView(LoginRequiredMixin, generic.DeleteView):
	login_url = reverse_lazy("users:login")
	redirect_field_name = 'next'

	template_name = 'resources/delete.html'
	model = Goals
	context_object_name = 'resource'

	def dispatch(self, request, *args, **kwargs):
		slug = self.kwargs.get('slug', '')
		goals = get_object_or_404(Goals, slug = slug)

		if not has_subject_permissions(request.user, goals.topic.subject):
			return redirect(reverse_lazy('subjects:home'))

		return super(DeleteView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		messages.success(self.request, _('The Goals specification of the thopic %s was removed successfully!')%(self.object.topic.name))
		
		return reverse_lazy('subjects:view', kwargs = {'slug': self.object.topic.subject.slug})