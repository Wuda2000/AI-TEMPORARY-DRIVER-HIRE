from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tracking  # Assuming there is a Tracking model

@receiver(post_save, sender=Tracking)
def tracking_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to execute after a tracking instance is created
        print(f'Tracking created: {instance}')
