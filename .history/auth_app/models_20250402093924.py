from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.utils.timezone import now
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.apps import apps
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a user with an email, username, and password."""
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser with an email, username, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()  # Set the custom manager

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
