import random
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from auth_app.models import Trip  # Direct import is fine since Trip is from the same app
import u

User = get_user_model()

def get_trip_model():
    """Lazy import of the Trip model to avoid circular imports."""
    return apps.get_model('trips', 'Trip')  # Correctly referencing the 'trips' app

def generate_unique_id():
    """Generate a unique trip ID ensuring no duplicates."""
    Trip = get_trip_model()  # Lazy import to prevent circular dependencies
    while True:
        trip_id = str(random.randint(100000, 999999))
        if not Trip.objects.filter(trip_id=trip_id).exists():
            return trip_id

class TripDetail(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # Linking to the Trip model
    additional_info = models.TextField(null=True, blank=True)  # Optional field for additional trip details

    def __str__(self):
        return f"Detail for trip {self.trip.id}: {self.additional_info}"

class Tracking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)  # Reference to the Trip model
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking {self.trip.trip_id} at {self.timestamp}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
