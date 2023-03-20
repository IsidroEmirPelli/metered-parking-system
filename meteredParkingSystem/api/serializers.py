from rest_framework import serializers


from core.models import( UserProfile, Vehicle, Parked)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('__all__')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('__all__')

class ParkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parked
        fields = ('__all__')
