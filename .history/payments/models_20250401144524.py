from django.db import models
from auth_app.models import CustomUser
from trips.models import Trip

class Payment(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)
    payer = models.ForeignKey(CustomUser, related_name='payer', on_delete=models.CASCADE)
    payee = models.ForeignKey(CustomUser, related_name='payee', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Trip {self.trip.id}'
