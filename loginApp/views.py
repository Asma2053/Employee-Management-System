import json
import logging
import os
from venv import logger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from loginApp.models.employee.employee_form import EmployeeForm
from loginApp.models.employee.employeeModel import Employee_Model
from rest_framework import status
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from loginApp.models.projects.project_form_model import ProjectForm
from loginApp.models.projects.add_projects_model import AddProjects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.middleware.csrf import get_token






logger = logging.getLogger(__name__)

def superuser_check(user):
    return user.is_superuser

@login_required
def home(request):
    employees = Employee_Model.objects.all()
    return render(request, 'loginApp/home.html', {'employees': employees})

@csrf_exempt
# def signUp(request):
    # if request.method == 'POST':
    #     logging.debug(f"Request content type: {request.content_type}")
    #     logging.debug(f"Request body: {request.body}")

    #     try:
    #         # Parse input data
    #         if request.content_type == 'application/json':
    #             data = json.loads(request.body)
    #         else:
    #             data = request.POST

    #         logging.debug(f"Received data: {data}")

    #         username = data.get('username')
    #         email = data.get('email')
    #         password1 = data.get('password')
    #         password2 = data.get('password2')

    #         # Check if username is empty
    #         if not username:
    #             return HttpResponse("Username cannot be empty", status=400)

    #         # Check if passwords match
    #         if password1 != password2:
    #             return HttpResponse("Passwords do not match", status=400)

    #         # Validate email format (basic check)
    #         if '@' not in email:
    #             return HttpResponse("Invalid email format", status=400)

    #         # Attempt to create a new user
    #         try:
    #             user = User.objects.create_user(username, email, password1)
    #             user.save()
    #             logging.debug(f"User created with ID: {user.id}")

    #             return redirect('login')
    #         except IntegrityError:
    #             logging.error("Username already exists.")
    #             return HttpResponse("Username already exists. Please choose a different username", status=400)
    #         except Exception as e:
    #             logging.error(f"Error creating user: {e}")
    #             return HttpResponse(f"An error occurred: {e}", status=500)
        
    #     except json.JSONDecodeError as e:
    #         logging.error(f"Invalid JSON received: {e}")
    #         return HttpResponse("Invalid JSON", status=400)
    #     except Exception as e:
    #         logging.error(f"Unexpected error: {e}")
    #         return HttpResponse(f"An unexpected error occurred: {e}", status=500)

    # return render(request, 'loginApp/signup.html')



# def login_view(request):
#     if request.method == 'POST':
#          username = request.POST.get('username')
#          password = request.POST.get('password')

#          user_status = authenticate(request, username = username, password = password)

#          if user_status is not None:
#             login(request, user_status)
#             return redirect('home')
#          else:
#             return HttpResponse ("Credentials are not valid. Please enter valid credentials")
         
#     # handling wrong request
#     return render(request,'loginApp/login.html')


def login_view(request):
    if request.method == 'POST':
        # Check for JSON Content-Type
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                print(JsonResponse({"error": "Invalid JSON"}, status=400)) 
        else:  # Fallback to form-urlencoded
            username = request.POST.get('username')
            password = request.POST.get('password')

        # Authenticate the user
        user_status = authenticate(request, username=username, password=password)

        if user_status is not None:
            login(request, user_status)
            return redirect('home')
            print(JsonResponse({"message": "Login successful"}, status=200))
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    # Handle other methods
    return render(request, 'loginApp/login.html')



@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST': 
        auth_logout(request)  
        return redirect ('login')
    
    return JsonResponse({"error": "Invalid request method"}, status=400)





def get_user_suggestions(request):
    if request.method == "GET":
        query = request.GET.get("q", "")  # Get the 'q' parameter from the request
        
        if query:
            # Search for usernames starting with the query
            users = User.objects.filter(username__startswith=query).values_list("username", flat=True)
            
            return JsonResponse({"suggestions": list(users)}, safe=False)
        else:
            print("No query provided.")  # Log if no query was sent
            return JsonResponse({"suggestions": []}, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)




def create_employeeData(request):
    if request.method == 'POST':
        logger.debug(f"Request content type: {request.content_type}")
        logger.debug(f"Request body: {request.body}")

        try:
            if request.content_type == 'application/json':
                logger.debug("Processing as JSON")
                data = json.loads(request.body)
            else:
                logger.debug("Processing as form data")
                data = request.POST

            logger.debug(f"Received data: {data}")

            form = EmployeeForm(data) 
            if form.is_valid():
                item = form.save()
                return redirect('home')
            else:
                logger.error(f"Form errors: {form.errors}")
                return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {e}")
            return HttpResponse("Invalid JSON", status=400)

    else:
        # Fetch employee names to pass to the form
        employee_names = list(Employee_Model.objects.values_list('name', flat=True))
        form = EmployeeForm()  # Empty form for GET request
        return render(request, 'loginApp/create_employee.html', {'form': form, 'employee_names': employee_names})


@user_passes_test(superuser_check)
def delete_employee(request, employee_id):
    # Get the employee item by ID or return a 404 error if not found
    employee = get_object_or_404(Employee_Model, id=employee_id)
    
    # Only allow deletion if it's a POST request
    if request.method == 'POST':
        employee.delete()
        return redirect('home')  # Redirect to a page after deletion
    
    # If not POST, render a confirmation page or return a forbidden response
    return render(request, 'loginApp/confirm_delete.html', {'employee': employee})



@user_passes_test(superuser_check)
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee_Model, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or employee list after saving
    else:
        form = EmployeeForm(instance = employee)
    
    return render(request, 'loginApp/edit_employees.html', {'form': form})


# def projectsDetails(request):
#     if request.method == 'GET':
#         projects = AddProjects.objects.all().values()  
#         return render(request, 'loginApp/projectsdetail.html', {'projects': projects})

def projectsDetails(request):
    projects = AddProjects.objects.all().values()
    if request.method == 'GET':
        if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
            return JsonResponse(list(projects), safe=False)
        else:
            return render(request, 'loginApp/projectsdetail.html', {'projects': projects})

def createProjects(request):
    if request.method == 'POST':
        # Handle file uploads with request.FILES
        form = ProjectForm(request.POST, request.FILES)
        # file = request.FILES
        if form.is_valid():
            project_id  = form.save()
            print(f"New project ID: {project_id.id}")


            return redirect('project_details')
        else:
            logger.error(f"Form errors: {form.errors}")
            render(request, 'loginApp/create_projects.html', {'form': form})
    else:
        form = ProjectForm()  # Provide an empty form for GET requests
    
    return render(request, 'loginApp/create_projects.html', {'form': form})


def delete_project(request, project_id):
    # Get the employee item by ID or return a 404 error if not found
    project = get_object_or_404(AddProjects, id=project_id)
    print(f"New project has been deleted: {project_id}")

    # Only allow deletion if     it's a POST request
    if request.method == 'POST':
        project.delete()
        print(f"New project {project_id} has been deleted")
        return redirect('project_details') 
    # If not POST, render a confirmation page or return a forbidden response
    return render(request, 'loginApp/confirm_delete_project.html', {'project': project})


def edit_projects(request, project_id):
    project = get_object_or_404(AddProjects, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_details')  # Redirect to the home page or employee list after saving
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'loginApp/edit_project.html', {'form': form})


def profile_view(request):
    return render(request, 'loginApp/profile.html')

def employee_detail(request, employee_detail):
    return render(request, 'loginApp/employeedetailpage.html')
