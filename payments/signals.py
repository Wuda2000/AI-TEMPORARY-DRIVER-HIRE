from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment  # Assuming there is a Payment model

@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to execute after a payment is created
        print(f'Payment created: {instance}')
