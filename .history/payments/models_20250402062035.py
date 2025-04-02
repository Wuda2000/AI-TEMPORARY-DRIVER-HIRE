from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

CustomUser = get_user_model()  # Lazy import of User model

class Payment(models.Model): 
    trip = models.OneToOneField('auth_app.Trip', to_field='id', on_delete=models.CASCADE, related_name='payment')
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments_made')
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('completed', 'Completed')], 
        default='pending'
    )
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} from {self.payer} to {self.payee}"  # Direct reference to avoid potential username issues
