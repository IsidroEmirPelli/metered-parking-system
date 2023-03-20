from django.db import models

# Create your models here.

class Company(models.Model):
    start_parking_hour = models.TimeField()
    end_parking_hour = models.TimeField()
    parking_price = models.DecimalField(max_digits=5, decimal_places=2)
    minumum_balance = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    negative_allowed = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    is_working = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parking_price}"