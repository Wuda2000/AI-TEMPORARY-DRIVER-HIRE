from django.db import models
from auth_app.models import Trip  # Ensure this points to the correct Trip model
import uuid
class Tracking(models.Model):
    trip = models.ForeignKey(Trip, related_name='trackings_tracking', on_delete=models.CASCADE)  # Change related_name to 'trackings_tracking'
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
