from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.utils.timezone import now
from django.utils import timezone
from django.utils.timezone import timedelta
from django.apps import apps

def get_payment_model():
    return apps.get_model('payments', 'Payment')  # ✅ Lazy Import

def generate_unique_id():
    return str(uuid.uuid4().hex[:12]) 

class CustomUser(AbstractUser):
    CAR_OWNER = 'car_owner'
    DRIVER = 'driver'

    ROLE_CHOICES = [
        (CAR_OWNER, 'Car Owner'),
        (DRIVER, 'Driver'),
    ]

    unique_id = models.CharField(default=generate_unique_id, editable=False, max_length=12, unique=True)
    password_last_changed = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)  # If this was changed to is_verified

    def __str__(self):
        return self.username

    def get_review_model(self):
        """Dynamically import the Review model when needed to avoid AppRegistryNotReady error."""
        Review = apps.get_model('reviews', 'Review')
        return Review

class DriverApplication(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="driver_applications")
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    license_number = models.CharField(max_length=50, unique=True, default="UNKNOWN")  # Default to "UNKNOWN"
    experience_years = models.IntegerField(default=0)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    cover_letter = models.FileField(upload_to="driver_applications/", default='default_cover_letter.pdf', blank=True)  # Added cover letter field
    applied_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

# Other models remain unchanged...
