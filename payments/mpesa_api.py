import requests
import base64
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
import os
import logging

class MpesaGateway:
    # Configure logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def __init__(self):
        """Initialize M-Pesa API credentials from environment variables."""
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = os.getenv("MPESA_SHORTCODE")
        self.passkey = os.getenv("MPESA_PASSKEY")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL")
        self.token_url = os.getenv("MPESA_TOKEN_URL", "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials")  # Production
        self.stk_url = os.getenv("MPESA_STK_URL", "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest")  # Production

        self.access_token = None
        self.token_expiry = None  # Store token expiration time

    def get_access_token(self):
        """Retrieves and caches M-Pesa API access token."""
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token  # Return cached token if still valid

        try:
            response = requests.get(
                self.token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
                timeout=10  # Set timeout
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get("access_token")
            self.token_expiry = datetime.now() + timedelta(seconds=3500)  # Tokens expire in ~1 hour

            return self.access_token
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch access token: {str(e)}")
            return None  # Return None instead of error dictionary

    def generate_password(self):
        """Generates password and timestamp for STK push request."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(data_to_encode.encode()).decode()
        return password, timestamp

    def initiate_payment(self, phone_number, amount):
        """Initiates a payment request using M-Pesa STK push."""
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}

        password, timestamp = self.generate_password()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": "AutoTempoHire",
            "TransactionDesc": "Payment for driver hire"
        }

        try:
            response = requests.post(self.stk_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            response_data = response.json()

            if response.status_code != 200:
                self.logger.error(f"Payment failed: {response_data}")
                return {"error": "Payment request failed", "details": response_data}

            return response_data

        except requests.RequestException as e:
            self.logger.error(f"Payment request failed: {str(e)}")
            return {"error": f"Payment request failed: {str(e)}"}
