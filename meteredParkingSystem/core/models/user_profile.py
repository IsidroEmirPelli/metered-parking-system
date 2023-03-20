from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    is_autority = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username