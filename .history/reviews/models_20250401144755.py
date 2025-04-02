from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

class Review(models.Model):
    driver = models.ForeignKey(
        'auth_app.Driver',
        on_delete=models.CASCADE,
        null=True,  # Allow existing reviews to not have a driver
        blank=True
    )  
    car_owner = models.ForeignKey(
        'auth_app.CarOwner',
        on_delete=models.CASCADE,
        null=True,  # Allow existing records without a car owner
        blank=True
    )  

    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def get_driver(self):
        """Lazy load the Driver model to avoid import errors"""
        Driver = apps.get_model('auth_app', 'Driver')
        return Driver.objects.get(id=self.driver.id) if self.driver else None

    def get_car_owner(self):
        """Lazy load the CarOwner model to avoid import errors"""
        CarOwner = apps.get_model('auth_app', 'CarOwner')
        return CarOwner.objects.get(id=self.car_owner.id) if self.car_owner else None

    def __str__(self):
        return f"Review by {self.car_owner} for {self.driver}: {self.rating} stars"
