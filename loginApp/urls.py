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
    path('home/', views.home, name="home"),
    path('profile/', views.profile_view, name='profile'),



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
    path('edit_projects/<int:project_id>/', views.edit_projects, name='edit_projects')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
