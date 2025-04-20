from django.db import models
from django.contrib.auth.models import User


class LocationDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude_clock_out = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude_clock_out = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    timestamp_clock_out = models.DateTimeField(null=True, blank=True)