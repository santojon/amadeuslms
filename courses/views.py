from django.shortcuts import render
from django.views.generic import ListView
from .models import Category
from django.core.urlresolvers import reverse_lazy
from rolepermissions.verifications import has_role

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, ListView):

    login_url = reverse_lazy("users:login")
    redirect_field_name = 'next'
    queryset = Category.objects.all()
    template_name = 'courses/home.html'
    context_object_name = 'categories'


    def get_queryset(self):
        result = super(IndexView, self).get_queryset()

       	
        return result

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_staff:
            context['page_template'] = "courses/home_admin_content.html"
        else:
            context['page_template'] = "courses/home_teacher_student_content.html"

        context['title'] = _('Home')

        if self.request.is_ajax():
            if self.request.user.is_staff:
                self.template_name = "home_admin_content.html"
            else:
                self.template_name = "home_teacher_student_content.html"

        return self.response_class(request = self.request, template = self.template_name, context = context, using = self.template_engine, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        list_courses = None
        if has_role(self.request.user,'system_admin'):
            list_courses = self.get_queryset().order_by('name')
            # categorys_courses = CourseCategory.objects.all()
        elif has_role(self.request.user,'professor'):
        	pass
            #list_courses = self.get_queryset().filter(professors__in = [self.request.user]).order_by('name')
            # categorys_courses = CourseCategory.objects.filter(course_category__professors__name = self.request.user.name).distinct()
        elif has_role(self.request.user, 'student'):
        	pass
            #list_courses = self.get_queryset().filter(students__in = [self.request.user]).order_by('name')

        
        context['title'] = _('Categories')
       
        return context

