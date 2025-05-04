from django.db import models
from django.contrib.auth.models import User
from loginApp.models.employee.employeeModel import Employee_Model

class LeaveRequest(models.Model):
    LEAVE_CHOICES = [
        ('Sick', 'Sick'),
        ('Vacation', 'Vacation'),
        ('Casual', 'Casual'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} from {self.start_date} to {self.end_date}"
