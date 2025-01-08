from .employeeModel import Employee_Model
from django import forms

class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee_Model
        fields = ('name','salary','position','department','contact_number','hiring_date')