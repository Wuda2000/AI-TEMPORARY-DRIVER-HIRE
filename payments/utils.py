from django.http import JsonResponse
from payments.mpesa_api import MpesaGateway

def create_json_response(data, status=200):
    """Create a JSON response with the given data and status code."""
    return JsonResponse(data, status=status)

def process_payment(payment_data):
    """Process payment using MpesaGateway."""
    gateway = MpesaGateway()
    return gateway.process_payment(payment_data)
