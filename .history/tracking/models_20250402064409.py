from django.db import models
from auth_app.models import Trip  # Ensure this points to the correct Trip model
import uuid

class Tracking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trackings")  # Ensure related_name is set
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    trip_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('completed', 'Completed'), ('in-progress', 'In Progress')],
        default='in-progress'
    )

    def __str__(self):
        return f"Tracking for Trip {self.trip.id} from {self.start_location} to {self.end_location}"
