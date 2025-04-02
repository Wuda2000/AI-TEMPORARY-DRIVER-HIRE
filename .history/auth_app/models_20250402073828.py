
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
from django.apps import apps  
from datetime import timedelta
from django.core.exceptions import ValidationError


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
     
class CarOwnerApplication(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="carowner_applications")
    owner_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, default="", blank=True)
    email = models.EmailField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner_name} - {self.status}"
    
class CarOwner(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='car_owner_profile')
    name = models.CharField(max_length=100)  # Must exist
    email = models.EmailField()  # Must exist
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.user.username} - Car Owner"
    
class Car(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=50, default="UNKNOWN")
    model = models.CharField(max_length=50, default="UNKNOWN")  # Removed to avoid confusion
    created_at = models.DateTimeField(default=now)
    plate_number = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    car_type = models.CharField(max_length=50)
    car_color = models.CharField(max_length=30)
    car_image = models.ImageField(upload_to='car_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} "
 
class CarOwnerApplicationContent(models.Model):
    application = models.ForeignKey(CarOwnerApplication, on_delete=models.CASCADE, related_name="application_contents")
    document = models.FileField(upload_to="carowner_applications/", default='default.pdf')
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Documents for {self.application.owner_name}"

class Driver(models.Model):
    user = models.OneToOneField('auth_app.CustomUser', on_delete=models.CASCADE, related_name='auth_driver_profile')
    id = models.BigAutoField(primary_key=True)  
    name = models.CharField(max_length=255)  # Driver's full name
    license_number = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField(upload_to='driver_images/', null=True, blank=True) 
    bio = models.TextField(blank=True, null=True)  
    experience_years = models.PositiveIntegerField(default=0)  # Default to 0 years

    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)
    trips_accomplished = models.PositiveIntegerField(default=0)

    location = models.CharField(max_length=255, blank=True, null=True)  
    phone_number = models.CharField(max_length=15, default="", blank=True)

    price_per_trip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default trip price
    
    def __str__(self):
        return f"{self.user.username} - {self.experience_years} years experience"

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
    cover_letter = models.FileField(upload_to="documents/", null=True, blank=True)  # Added cover letter field
    experience_years = models.IntegerField(default=0)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    kcse_certificate = models.FileField(upload_to='documents/', null=True, blank=True) 
    cv = models.FileField(upload_to='documents', null=True, blank=True)
    good_conduct = models.FileField(upload_to='documents/', null=True, blank=True)  # Ensure this field is defined 
    applied_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

class DriverApplicationContent(models.Model): 
    application = models.ForeignKey(
        DriverApplication,
        on_delete=models.CASCADE,
        null=True,  # Temporarily allow null values
        blank=True
    )
    document = models.FileField(upload_to="driver_applications/", default='default.pdf')  # Added default value
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Documents for {self.application.user.username}"

class Trip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    car_owner = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='car_owner_trips')
    driver = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='driver_trips')
    pickup_location = models.CharField(max_length=255, default="Unknown Location")  # Set a default value
    destination = models.CharField(max_length=255)
    trip_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    trip_duration = models.DurationField(default=timedelta(hours=1))
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_offered = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    trip_distance = models.FloatField(default=0.0)  # Set a default value
    pickup_point = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Added status field

    def clean(self):
        """Ensure arrival time is not before departure time"""
        if self.arrival_time and self.arrival_time < self.departure_time:
            raise ValidationError("Arrival time cannot be before departure time.")
    
    def get_tracking_entries(self):
        """Retrieve all tracking records for this trip"""
        return self.trackings.all()

    def __str__(self):
        return f"Trip by {self.car_owner.username} with {self.driver.username} - {self.pickup_location} to {self.destination} ({self.status})"

class Tracking(models.Model):
    trip = models.ForeignKey(Trip, related_name='trackings', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tracking for Trip {self.trip.trip_id} at {self.timestamp} - {self.location}"
