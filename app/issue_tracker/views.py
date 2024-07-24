from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from issue_tracker.forms import TaskForm, SearchForm, ProjectForm
from issue_tracker.models import Task, Project


class TasksView(LoginRequiredMixin, ListView):
    template_name = 'tasks.html'
    model = Task

    context_object_name = 'tasks'
    paginate_by = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_value = None
        self.form = None

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        hide_deleted = ~Q(is_deleted=True)

        if self.search_value:
            query = ((Q(summary__icontains=self.search_value) |
                     Q(description__icontains=self.search_value)) &
                     hide_deleted
                     )
            queryset = queryset.filter(query)
        else:
            queryset = queryset.filter(hide_deleted).order_by('id')

        return queryset

    def get_search_form(self):
        return SearchForm(self.request.POST)

    def get_search_value(self):
        if self.form.is_valid():
            print(self.form)
            return self.form.cleaned_data['search']
        return None


class TaskView(LoginRequiredMixin, TemplateView):
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if not task.is_deleted:
            context['task'] = task
        else:
            context['error'] = "Not Found"

        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_task.html'
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse('task', kwargs={'pk': self.kwargs['pk']})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = 'tasks'
    template_name = 'task_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        print(123181312182312)
        self.success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.success_url)


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'projects_list.html'
    model = Project

    context_object_name = 'projects'
    paginate_by = 5

class ProjectDetailView(LoginRequiredMixin, ListView):
    template_name = 'project_detail.html'
    model = Project

    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        fake_delete = Q(project_id=self.kwargs['pk']) & Q(is_deleted__icontains=False)
        context['tasks'] = Task.objects.filter(fake_delete)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project_create.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class CreateProjectTaskView(LoginRequiredMixin, CreateView):
    template_name = 'project_task_create.html'
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        task = form.save()
        task.project = project
        task.save()
        return super().form_valid(form)
