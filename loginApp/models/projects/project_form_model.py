from django import forms
from .add_projects_model import AddProjects

class ProjectForm(forms.ModelForm):
    class Meta:
        model = AddProjects
        fields = ['name', 'status', 'start_date','end_date','document']

        