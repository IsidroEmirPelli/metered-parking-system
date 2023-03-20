import datetime
from django.shortcuts import render
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .constants import (MSG_NOT_WORKING, MSG_NOT_PARK_NOW, MSG_ALREADY_PARKED, MSG_NOT_ENOUGH_MONEY, MSG_VEHICLE_NOT_EXIST, MSG_VEHICLE_NOT_PARKED)
from core.models import( UserProfile, Vehicle, Parked)
from core.utils import discount_time_parked, get_vehicle_by_matricule
from .serializers import( UserProfileSerializer, VehicleSerializer, ParkedSerializer)

# create a endpoint to set the parking status of a vehicle
class ParkedViewSet(ModelViewSet):
    """ In this viewset we create a new parking
        update the parking status of a vehicle and
        get the parking status of a vehicle """

    queryset = Parked.objects.all()
    serializer_class = ParkedSerializer

    def create(self, request, *args, **kwargs):
        """ Create a new parking """
        vehicle = get_vehicle_by_matricule(request.data.get('matricule'))

        if type(vehicle) is Response:
            return vehicle

        person = vehicle.owner
        if person.company.is_working:
            if datetime.datetime.now().time() > person.company.end_parking_hour or datetime.datetime.now().time() < person.company.start_parking_hour:
                return Response({'message': MSG_NOT_PARK_NOW})
            parked = Parked.objects.filter(vehicle=vehicle).last()
            if parked is not None and parked.end_time is None:
                return Response({'message': MSG_ALREADY_PARKED})
            if person.balance < person.company.minumum_balance or person.company.negative_allowed >= person.balance or person.balance < 0:
                return Response({'message': MSG_NOT_ENOUGH_MONEY})
            request.data._mutable = True
            request.data['vehicle'] = vehicle.id
            request.data._mutable = False
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        return Response({'message': MSG_NOT_WORKING})


    def update(self, request, *args, **kwargs):
        """ Update the parking status of a vehicle """
        vehicle = get_vehicle_by_matricule(request.data.get('matricule'))
        
        if type(vehicle) is Response:
            return vehicle

        person = vehicle.owner
        if person.company.is_working:
            parked = Parked.objects.filter(vehicle=vehicle).last()
            if parked is None:
                return Response({'message': MSG_VEHICLE_NOT_PARKED})

            parked.end_time = timezone.now()
            parked.save()
            vehicle.is_parked = False
            vehicle.save()
            total_price = discount_time_parked(parked, person)
            parked.price = total_price
            parked.save()
            person.balance -= total_price
            person.save()
            return Response({'message': f'This vehicle is not parked anymore, you payed {total_price} '})
        return Response({'message': MSG_NOT_WORKING})

    # return the status of the vehicle
    def retrieve(self, request, *args, **kwargs):
        """ Get the parking status of a vehicle """
        vehicle = get_vehicle_by_matricule(request.data.get('matricule'))
        
        if type(vehicle) is Response:
            return vehicle

        if vehicle.is_parked is True:
            return Response({'message': MSG_ALREADY_PARKED})

        return Response({'message': MSG_VEHICLE_NOT_PARKED})        

