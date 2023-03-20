from django.db import models

from django.utils import timezone
# Create your models here.

class Parked(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now(), blank=False)
    end_time = models.DateTimeField(null=True, blank=True)
    max_time = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(default=0)
    def __str__(self):
        return self.vehicle

    def __str__(self):
        return f"{self.vehicle} - {self.start_time} - {self.end_time}"