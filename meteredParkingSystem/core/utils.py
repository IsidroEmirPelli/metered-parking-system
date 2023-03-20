from django.utils import timezone
from .models import Parked, Vehicle
from rest_framework.response import Response
from api.constants import MSG_VEHICLE_NOT_EXIST, MSG_ALREADY_PARKED, MSG_NOT_ENOUGH_MONEY, MSG_NOT_PARK_NOW, MSG_NOT_WORKING, MSG_VEHICLE_NOT_PARKED

def discount_time_parked(parked, user_profile):
    """ Calculate the discount time """
    if parked.end_time is not None:
        end_time = parked.end_time.astimezone(timezone.utc).replace(tzinfo=None)
        start_time = parked.start_time.astimezone(timezone.utc).replace(tzinfo=None)
        time_parked = end_time - start_time
        hours_parked = time_parked.total_seconds() / 3600
        price = float(hours_parked) * float(user_profile.company.parking_price)
        return price
    Exception('The vehicle is still parked')



def get_vehicle_by_matricule(matricule):
    """ Get a vehicle by matricule """
    if matricule is  None or matricule is '':
            return Response({'message': MSG_VEHICLE_NOT_EXIST})
    vehicle = Vehicle.objects.filter(vehicle_matricule=matricule).first()
    if vehicle is None:
            return Response({'message': MSG_VEHICLE_NOT_EXIST})
    return vehicle