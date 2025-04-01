from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DriverMatch  # Assuming there is a DriverMatch model

@receiver(post_save, sender=DriverMatch)
def driver_match_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to execute after a driver match is created
        print(f'Driver match created: {instance}')
