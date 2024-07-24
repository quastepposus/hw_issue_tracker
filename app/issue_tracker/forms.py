from django import forms

from issue_tracker.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'types']

        widgets = {
            'types': forms.CheckboxSelectMultiple(attrs={'type': 'form-control'})
        }

class SearchForm(forms.Form):
    search = forms.CharField(min_length=3, max_length=50, label='', required=False)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }
