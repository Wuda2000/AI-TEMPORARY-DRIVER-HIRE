from rest_framework import serializers
from .models import DriverMatch

class DriverMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverMatch
        fields = ['id', 'driver', 'criteria', 'matched_at']
