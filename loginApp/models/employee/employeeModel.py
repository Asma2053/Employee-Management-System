from django.db import models


# Create your models here.

class Employee_Model(models.Model):
    name = models.CharField(max_length=50, default='Unknown')
    salary = models.IntegerField()
    position = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15, default='N/A')
    hiring_date = models.CharField(max_length=30, default='01-01-2000')


    def __str__(self):
        return f"{self.position} in {self.department}" 