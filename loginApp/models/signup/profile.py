from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Link this model to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Add any additional fields like 'role'
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.user.username
