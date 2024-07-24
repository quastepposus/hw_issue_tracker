from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from issue_tracker.views import TasksView, TaskView, TaskUpdateView, TaskDeleteView, \
    ProjectListView, ProjectDetailView, ProjectCreateView, CreateProjectTaskView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TasksView.as_view(), name='index'),
    path('tasks/', TasksView.as_view(), name='tasks'),

    path('tasks/<int:pk>/', TaskView.as_view(), name='task'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),

    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/create', CreateProjectTaskView.as_view(), name='create_project_task'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
