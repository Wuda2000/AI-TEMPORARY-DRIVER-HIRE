import uuid
import random
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.apps import apps  # ✅ Used for lazy import
from django.contrib.auth import get_user_model
from auth_app.models import Trip

User = get_user_model()

def get_trip_model():
    """Lazy import of the Trip model to avoid circular imports."""
    return apps.get_model('trips', 'Trip')  # ✅ Corrected reference to 'trips' app

def generate_unique_id():
    """Generate a unique trip ID ensuring no duplicates."""
    Trip = get_trip_model()  # ✅ Lazy import to prevent circular dependencies
    while True:
        trip_id = str(random.randint(100000, 999999))
        if not Trip.objects.filter(trip_id=trip_id).exists():
            return trip_id


class Tracking(models.Model):
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, null=True, blank=True)  # ✅ Corrected reference
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
