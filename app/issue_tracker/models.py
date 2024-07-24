from django.db import models

from issue_tracker.validators import summary_validator, description_validator, project_title_validator, \
    project_description_validator


class Status(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name='Title',
                             validators=(project_title_validator, ))
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Description',
                                   validators=(project_description_validator,))

    start_date = models.DateField(null=False, blank=False, verbose_name='Start Date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End Date')

class Task(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name="Summary",
                               validators=(summary_validator,))
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Description",
                                   validators=(description_validator,))
    status = models.ForeignKey('Status', related_name='tasks', on_delete=models.RESTRICT, verbose_name='Status')
    types = models.ManyToManyField('Type', related_name='tasks', blank=True, verbose_name='Type')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Update Time")

    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.PROTECT, null=True, verbose_name='Project')

    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")