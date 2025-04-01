import json
import logging
from django.http import JsonResponse
from .models import Transaction  # Assuming Transaction model exists

# Configure logging
logger = logging.getLogger(__name__)

def handle_callback(request):
    """
    Handles the callback from M-Pesa after payment processing.
    
    :param request: The HTTP request containing the callback data.
    :return: JSON response indicating success or failure.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            transaction_id = data.get("TransactionID")
            response_code = data.get("ResponseCode")

            # Check if the transaction has already been updated to avoid duplicate processing
            existing_transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
            if existing_transaction and existing_transaction.status in ["success", "failed"]:
                logger.info(f"Transaction {transaction_id} has already been processed.")
                return JsonResponse({"status": "success", "message": "Callback processed."})

            # Update the transaction status in the database
            if existing_transaction:
                existing_transaction.status = "success" if response_code == "0" else "failed"
                existing_transaction.save()

            logger.info(f"Transaction {transaction_id} status updated to {'success' if response_code == '0' else 'failed'}.")
            return JsonResponse({"status": "success", "message": "Callback processed successfully."})

        except Exception as e:
            logger.error(f"Error processing callback: {str(e)}")
            return JsonResponse({"status": "error", "message": "Error processing callback."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
