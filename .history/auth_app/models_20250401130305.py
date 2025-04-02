from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.utils.timezone import now
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
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

class CarOwner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_owners')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"

# Existing classes remain unchanged...
