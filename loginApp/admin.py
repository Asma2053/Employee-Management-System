from django.contrib import admin
from loginApp.models.employee.employeeModel import Employee_Model
from loginApp.models.projects.add_projects_model import AddProjects
from loginApp.models.location.locationDetail import LocationDetail
from loginApp.models.projects.LeaveRequest import LeaveRequest
from loginApp.models.projects.LeaveRequestForm import LeaveRequestForm

# Register your models here.
admin.site.register(Employee_Model)
admin.site.register(AddProjects) 
admin.site.register(LocationDetail)
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'leave_type']
    search_fields = ['employee__username', 'reason']


