from django.contrib import admin
from loginApp.models.employee.employeeModel import Employee_Model
from loginApp.models.projects.add_projects_model import AddProjects
from loginApp.models.location.locationDetail import LocationDetail

# Register your models here.
admin.site.register(Employee_Model)
admin.site.register(AddProjects) 
admin.site.register(LocationDetail)


