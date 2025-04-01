from rest_framework import serializers
from auth_app.models import CustomUser

from .models import CustomUser, DriverApplication, Driver


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active']

class DriverApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverApplication
        fields = ['id', 'user', 'first_name', 'surname', 'age', 'ethnicity', 'experience_years', 'status', 'applied_at']
