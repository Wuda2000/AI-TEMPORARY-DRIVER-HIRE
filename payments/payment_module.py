import requests
import base64
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
import logging
import os
import re  # Ensure re is imported for validation
from payments.models import Transaction  # Adjust based on your app name
# Ensure Transaction model is imported

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MpesaPayment:
    def __init__(self):
        # Load environment variables
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = os.getenv("MPESA_SHORTCODE")
        self.passkey = os.getenv("MPESA_PASSKEY")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL")  # Fix: Added missing callback_url

        # Ensure all required credentials are set and initialize token variables
        self.access_token = None
        self.token_expiry = None  # Store token expiration time

        if not all([self.consumer_key, self.consumer_secret, self.shortcode, self.passkey, self.callback_url]):
            logger.error("Missing one or more MPESA environment variables.")
            raise ValueError("Ensure all required MPESA credentials are set in the .env file.")

        self.base_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def get_access_token(self):
        """Retrieves and caches M-Pesa API access token."""
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token  # Return cached token if still valid

        try:
            response = requests.get(
                self.base_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
                timeout=10  # Set timeout
            )
            response.raise_for_status()  # Raise an error for failed requests
            data = response.json()
            self.access_token = data.get("access_token")
            self.token_expiry = datetime.now() + timedelta(seconds=3500)  # Tokens expire in ~1 hour

            return self.access_token

        except requests.RequestException as e:
            logger.error(f"Error fetching access token: {e}")
            return None

    def generate_password(self):
        """
        Generates the base64-encoded password for STK Push authentication.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(data_to_encode.encode()).decode(), timestamp

    def initiate_payment(self, phone_number, amount):
        """
        Initiates an M-Pesa STK Push request.

        :param phone_number: The phone number making the payment.
        :param amount: The amount to be paid.
        :return: JSON response from M-Pesa API.
        """
        access_token = self.get_access_token()  # Get access token
        if not access_token:
            return {"error": "Failed to get access token"}

        password, timestamp = self.generate_password()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Validate user payment details
        if not self.validate_payment_details(phone_number, amount):
            return {"error": "Invalid payment details"}

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,  # Fix: Now correctly uses self.callback_url
            "AccountReference": "AutoTempoHire",
            "TransactionDesc": "Payment for driver hire"
        }

        try:
            response = requests.post(self.stk_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for failed requests
            response_data = response.json()

            # Log response for debugging
            logger.info(f"STK Push Response: {response_data}")

            # Handle different response statuses
            if response_data.get("ResponseCode") == "0":
                return {"status": "success", "message": "Payment initiated successfully."}
            elif response_data.get("ResponseCode") in ["1", "2"]:
                return {"status": "pending", "message": "Payment is pending. Please check back later."}
            else:
                return {"status": "error", "message": "Payment failed. Please try again."}

        except requests.RequestException as e:
            logger.error(f"STK Push request failed: {e}")
            return {"error": str(e)}

    def validate_payment_details(self, phone_number, amount):
        """Validate user payment details before processing."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        if not re.match(r"^\+?254\d{9}$", phone_number):  # Validate Kenyan phone number format
            return False
        return True


def process_payment(user, driver, amount, transaction_id, retry_count=0):
    """
    Handles the payment process when hiring a driver.

    :param user: The user making the payment (CarOwner).
    :param driver: The driver being hired.
    :param amount: The amount to be paid.
    :param transaction_id: Unique transaction ID.
    :return: Success or error message.
    """
    if retry_count > 3:
        return {"status": "error", "message": "Maximum retry attempts reached. Please try again later."}

    # Record transaction in database
    transaction = Transaction.objects.create(user=user, driver=driver, amount=amount, transaction_id=transaction_id, status="pending")

    mpesa = MpesaPayment()
    response = mpesa.initiate_payment(user.phone_number, amount)

    if response.get("status") == "success":
        driver.available = False
        driver.save()
        transaction.status = "completed"
        transaction.save()
        return {"status": "success", "message": "Payment successful. Driver hired."}

    elif response.get("status") == "pending":
        transaction.status = "pending"
        transaction.save()
        return {"status": "pending", "message": "Payment is being processed. Check back later."}

    else:
        transaction.status = "failed"
        transaction.save()
        return {"status": "error", "message": response.get("message", "Payment failed. Try again.")}


# Example usage (for debugging)
if __name__ == "__main__":
    test_phone = "+2547XXXXXXXX"  # Replace with a valid Safaricom number
    test_amount = 500  # Example amount

    payment_response = MpesaPayment().initiate_payment(test_phone, test_amount)
    print(payment_response)
