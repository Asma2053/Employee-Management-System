from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


urlpatterns = [
    path('', views.home, name="home"),
    # path('signup/', views.signUp, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('employee_list/', views.home, name="employee_list"),
    # path('profile/', views.profile_view, name='profile'),

    #get particular user
    path('user/', views.user_view, name = "user"),

    #for employees 
    path('create/', views.create_employeeData, name="create_employeeData"),
    path('delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),

    #for employee detail page
    path('employeedetail/<int:employee_id>/', views.employee_detail, name='employee_detail'),

    #suggestion for employee
    path('get_user_suggestions/', views.get_user_suggestions, name='get_user_suggestions'),


    # for projects
    path('projectsdetails/', views.projectsDetails, name="project_details"),
    path('delete_projects/<int:project_id>/', views.delete_project, name='delete_project'),
    path('create_projects/', views.createProjects, name="create_projects"),
    path('edit_projects/<int:project_id>/', views.edit_projects, name='edit_projects'),


    # #for attendance
    path('attendancedetails/', views.attendanceDetails, name="attendance_details"),
    #for attendance clockout
    path('attendancedetailsclockout/', views.attendanceDetailsClockout, name="attendance_details_clock_out"),
    #to fetch attendance data
    path('api/attendance/', views.get_attendance_data, name='get_attendance_data'),

    # user detail page
    path('profile/', views.user_profile, name='user_profile'),

    path('export/excel/', views.export_attendance_excel, name='export_attendance_excel'),

    #leave
    path('request-leave/', views.request_leave, name='request_leave'),
    path('leave-history/', views.employee_leave_history, name='employee_leave_history'),

    # Admin URLs
    path('leave-requests/', views.admin_leave_requests, name='admin_leave_requests'),
    path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    #required homepage company directory and policies
    path('company-policies/', views.company_policies, name='company_policies'),
    path('org-chart/', views.org_chart, name='org_chart'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
