from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review  # Assuming there is a Review model

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to execute after a review is created
        print(f'Review created: {instance}')
