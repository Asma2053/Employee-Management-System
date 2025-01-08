from django.contrib import admin
from loginApp.models.employee.employeeModel import Employee_Model
from loginApp.models.projects.add_projects_model import AddProjects


# Register your models here.
admin.site.register(Employee_Model)
admin.site.register(AddProjects) 


