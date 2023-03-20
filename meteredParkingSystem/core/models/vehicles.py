from django.db import models


class Vehicle(models.Model):
    vehicle_matricule = models.CharField(max_length=10)
    is_parked = models.BooleanField(default=False)
    owner = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vehicle_matricule
