# Employee-Management-System
useful to manage the employee of an organization
# 🧑‍💼 Employee Management System (EMS)

A comprehensive web-based Employee Management System developed using **Python (Django Framework)** with **HTML, CSS, and JavaScript** for the frontend. This system allows organizations to efficiently manage employee information, project assignments, attendance, and leave requests.

## 📌 Features

- **Project Module**:  
  - Admin can add, edit, delete, and view projects.
  - Admin can upload and view files (PDF, TXT, etc.).
  - Normal users can view project listings.

- **Employee Module**:  
  - Admin can add (only logged-in employees), edit, delete, and view employees.
  - Normal users can view employee listings.

- **Leave Management Module**:  
  - Admin can accept or reject leave requests.
  - Employees can apply for different types of leave (sick, vacation, casual, etc.) and view history.

- **Clock In / Clock Out**:  
  - All users can record their clock-in and clock-out times.

- **Authentication**:  
  - Admins create employee credentials.
  - Secure login/logout system for both admin and employees.

- **Attendance Module**:  
  - Admin can view and download attendance reports in Excel format.

- **Dashboard**:  
  - Role-based dashboards for admin and employees.
  - Access to Home, Policies, Organization Chart, and quick-action buttons (profile, leave, resources).

---

## 🛠️ Tech Stack

| Layer       | Technology             |
|-------------|------------------------|
| Backend     | Python, Django         |
| Frontend    | HTML, CSS, JavaScript  |
| Database    | SQLite (default Django DB) |

---

## 📦 Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ems-django.git
   cd ems-django

2. Install Dependencies
    install pip

3. Run Migrations
   python manage.py migrate

4. Create Superuser
   python manage.py createsuperuser

5. Run the Server
   python manage.py runserver

6. Access the System
  http://127.0.0.1:8000/


