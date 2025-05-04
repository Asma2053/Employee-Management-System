import datetime
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
from datetime import date, datetime
from datetime import datetime, timezone
from loginApp.models.location.locationDetail import LocationDetail
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from openpyxl import Workbook
from django.http import HttpResponse
from loginApp.models.projects.LeaveRequest import LeaveRequest
from loginApp.models.projects.LeaveRequestForm import LeaveRequestForm





logger = logging.getLogger(__name__)

def superuser_check(user):
    return user.is_superuser

@login_required
def home(request):
    employees = Employee_Model.objects.all()
    return render(request, 'loginApp/employeedetailpage.html', {'employees': employees})

@csrf_exempt
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
            return redirect('user')
            print(JsonResponse({"message": "Login successful"}, status=200))
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    # Handle other methods
    return render(request, 'loginApp/login.html')



@api_view(['GET', 'POST'])
def logout_view(request):
    if request.method in ['GET', 'POST']:
        auth_logout(request)  
        return redirect ('login')
    
    return JsonResponse({"error": "Invalid request method"}, status=400)





def get_user_suggestions(request):
    if request.method == "GET":
        query = request.GET.get("q", "").strip()  # Get the 'q' parameter from the request
        
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
                data = json.loads(request.body)
            else:
                data = request.POST
                selected_name = data.get('name', '').strip()

            form = EmployeeForm(data) 
            if form.is_valid():
                form.instance.name = selected_name
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


def projectsDetails(request):
    projects = AddProjects.objects.all()
    print("Projects Retrieved:", projects)  # Debugging line
    if request.method == 'GET':
        if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
            return JsonResponse(list(projects), safe=False)
        else:
            return render(request, 'loginApp/projectsdetail.html', {'projects': projects})

@user_passes_test(superuser_check)
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

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee_Model, id= employee_id)
    return render(request, 'loginApp/employeedetailpage.html', {'employee': employee})


# @csrf_exempt
# def attendanceDetails(request):
#     if request.method == 'GET':
#         return render(request, 'loginApp/attendance.html')

#     elif request.method == "POST":
#         if not request.body:
#             return JsonResponse({"error": "Empty request body"}, status=400)

#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             print("Received Data:", data)

#             # Extract values safely
#             timestamp_str = data.get('time')

#             if not timestamp_str:
#                 return JsonResponse({"error": "Clock-in timestamp is missing"}, status=400)

#             # Convert timestamps
#             timestamp_dt = datetime.strptime(timestamp_str.rstrip("Z"), "%Y-%m-%dT%H:%M:%S.%f")

#             # Extract latitude and longitude safely
#             latitude = float(data.get('latitude', 0))
#             longitude = float(data.get('longitude', 0))

#             # Save to database
#             record = LocationDetail.objects.create(
#                 user=request.user,
#                 latitude=latitude,
#                 longitude=longitude
#                 # timestamp=timestamp_dt
#             )

#             print("Data saved successfully!")
#             return JsonResponse({'message': 'Data saved successfully', 'record_id': record.id})

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#         except Exception as e:
#             print("Error:", str(e))
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def attendanceDetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            timestamp_str = data.get('time')
            if not timestamp_str:
                return JsonResponse({"error": "Clock-in timestamp is missing"}, status=400)

            timestamp_dt = datetime.strptime(timestamp_str.rstrip("Z"), "%Y-%m-%dT%H:%M:%S.%f")
            latitude = float(data.get('latitude', 0))
            longitude = float(data.get('longitude', 0))

            # Ensure user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            record = LocationDetail.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp_dt
            )

            return JsonResponse({'message': 'Clock-in successful', 'record_id': record.id})

        except Exception as e:
            print("Clock-in error:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def attendanceDetailsClockout(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("All records for user:", [
                (r.id, r.timestamp, r.timestamp_clock_out) 
                for r in LocationDetail.objects.filter(user=request.user)
            ])
            print("Parsed JSON data:", data)

            # Find the latest record WITHOUT clock-out
            last_attendance = LocationDetail.objects.filter(
                user=request.user,
                timestamp_clock_out__isnull=True
            ).order_by('-timestamp').first()  # Using 'timestamp' instead of 'timestamp_clock_in'

            if not last_attendance:
                return JsonResponse({'error': 'No active clock-in found'}, status=400)

            # Update with clock-out data
            last_attendance.timestamp_clock_out = datetime.fromisoformat(
                data['timestamp_clock_out'].replace('Z', '+00:00')
            )
            last_attendance.latitude_clock_out = float(data['latitude_clock_out'])
            last_attendance.longitude_clock_out = float(data['longitude_clock_out'])
            last_attendance.save()

            return JsonResponse({'message': 'Clock-out saved successfully'})

        except Exception as e:
            print("!!! ERROR:", str(e))
            return JsonResponse({'error': str(e)}, status=500)


# def get_attendance_data(request):
#     data = LocationDetail.objects.all()
#     formatted_data = []

#     for entry in data:
#         formatted_data.append({
#             'user_id': entry.user_id,
#             'timestamp': entry.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),  # ISO-ish format
#             'timestamp_clock_out': entry.timestamp_clock_out.strftime('%Y-%m-%dT%H:%M:%S') if entry.timestamp_clock_out else '',
#         })

#     return JsonResponse(formatted_data, safe=False)
        

def get_attendance_data(request):
    data = LocationDetail.objects.all().order_by('-timestamp')  # optional: latest first
    return render(request, 'loginApp/attendance.html', {'attendance_data': data})

def user_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not logged in
    
    # Get the logged-in user
    user = request.user
    return render(request, 'loginApp/user.html', {'user': user})


@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # ⬅️ Keeps user logged in

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')  # ⬅️ Redirect to same page

    return render(request, 'loginApp/user_profile.html', {'user': user})


def export_attendance_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance Records"

    # Add header
    ws.append(["Username", "Clock In", "Clock Out"])

    # Get all attendance records
    attendance_records = LocationDetail.objects.all()

    for record in attendance_records:
        clock_in = record.timestamp.replace(tzinfo=None) if record.timestamp else ""
        clock_out = record.timestamp_clock_out.replace(tzinfo=None) if record.timestamp_clock_out else ""
        ws.append([
            record.user.username,
            clock_in,
            clock_out
        ])

    # Create HTTP response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
    wb.save(response)

    return response



#employee leave
@login_required
def request_leave(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            return redirect('employee_leave_history')
    else:
        form = LeaveRequestForm()
    return render(request, 'loginApp/request_leave.html', {'form': form})

@login_required
def employee_leave_history(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'loginApp/leave_history.html', {'leave_requests': leave_requests})


@user_passes_test(superuser_check)
def admin_leave_requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'loginApp/leave_requests.html', {'leave_requests': leave_requests})

@user_passes_test(superuser_check)
def approve_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.status = 'Approved'
    leave_request.save()
    return redirect('admin_leave_requests')

@user_passes_test(superuser_check)
def reject_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.status = 'Rejected'
    leave_request.save()
    return redirect('admin_leave_requests')



@login_required
def company_policies(request):
    policy_sections = [
        {
            'number': 1,
            'title': 'Code of Conduct',
            'items': [
                {'heading': 'Professionalism & Respect:', 'text': 'Treat everyone with courtesy. No harassment or discrimination.'},
                {'heading': 'Integrity & Ethics:',    'text': 'Conduct business honestly. Disclose conflicts of interest.'},
            ],
        },
        {
            'number': 2,
            'title': 'Attendance & Punctuality',
            'items': [
                {'heading': 'Work Hours:',          'text': '9 AM–5 PM, Mon–Fri. Clock in/out via the system.'},
                {'heading': 'Late & Early:',        'text': 'Notify manager 1 hr before start if late or leaving early.'},
                {'heading': 'Absence Reporting:',   'text': 'Report illness/emergencies at least 1 hr before shift.'},
            ],
        },
        # … add sections 3–8 similarly …
    ]
    return render(request, 'loginApp/company_policies.html', {
        'policy_sections': policy_sections
    })

@login_required
def org_chart(request):
    return render(request, 'loginApp/reference_docs.html')