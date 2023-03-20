from django.contrib import admin

# Register your models here.
from .models import( UserProfile, Vehicle, Parked, Company)

admin.site.register(UserProfile)
admin.site.register(Vehicle)
admin.site.register(Parked)
admin.site.register(Company)
