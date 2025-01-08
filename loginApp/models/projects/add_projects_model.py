from django.db import models


# Create your models here.

class AddProjects(models.Model):
    
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    start_date = models.CharField(max_length=20, default='01-01-2000')
    end_date = models.CharField(max_length=20, default='01-01-2000')
    document = models.FileField(upload_to='documents/')


    def __str__(self):
        return self.name