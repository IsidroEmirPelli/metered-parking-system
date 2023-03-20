import datetime
from django.shortcuts import render
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from core.models import( UserProfile, Vehicle, Parked)
from core.utils import discount_time_parked
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
        matricule = request.data.get('matricule')
        if matricule is not None and matricule != '':
            vehicle = Vehicle.objects.filter(vehicle_matricule=matricule).first()
            if vehicle is not None:
                person = vehicle.owner
                if person.company.is_working is False:
                    return Response({'message': 'The system is not working'})
                if datetime.datetime.now().time() > person.company.end_parking_hour or datetime.datetime.now().time() < person.company.start_parking_hour:
                    return Response({'message': 'You can not park now'})
                parked = Parked.objects.filter(vehicle=vehicle).last()
                if parked is not None and parked.end_time is None:
                    return Response({'message': 'This vehicle is already parked'})
                if person.balance < person.company.minumum_balance or person.company.negative_allowed >= person.balance or person.balance < 0:
                    return Response({'message': 'You do not have enough money to park'})
                request.data._mutable = True
                request.data['vehicle'] = vehicle.id
                request.data._mutable = False
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(serializer.data)
            return Response({'message': 'This vehicle does not exist'})

    def update(self, request, *args, **kwargs):
        """ Update the parking status of a vehicle """
        matricule = request.data.get('matricule')
        if matricule is not None and matricule != '':
            vehicle = Vehicle.objects.filter(vehicle_matricule=matricule).first()
            if vehicle is not None:
                person = vehicle.owner
                parked = Parked.objects.filter(vehicle=vehicle).last()
                if parked is not None:
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
                else:
                    return Response({'message': 'This vehicle is not parked'})
            else:
                return Response({'message': 'This vehicle does not exist'})

    # return the status of the vehicle
    def retrieve(self, request, *args, **kwargs):
        """ Get the parking status of a vehicle """
        matricule = request.data.get('matricule')
        if matricule is not None and matricule != '':
            vehicle = Vehicle.objects.filter(vehicle_matricule=matricule).first()
            if vehicle is not None:
                parked = Parked.objects.filter(vehicle=vehicle).last()
                if parked is not None:
                    return Response({'message': 'This vehicle is parked'})
                else:
                    return Response({'message': 'This vehicle is not parked'})
            else:
                return Response({'message': 'This vehicle does not exist'})

