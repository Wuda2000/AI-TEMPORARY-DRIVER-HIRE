from django.urls import path
from .payment_history_view import payment_history_view  # Import the payment history view

urlpatterns = [
    path('payment/history/', payment_history_view, name='payment_history'),  # Added payment history path
]
