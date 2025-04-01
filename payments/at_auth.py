import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

# Safaricom API Credentials
CONSUMER_KEY = os.getenv("SAFARICOM_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("SAFARICOM_CONSUMER_SECRET")

def get_access_token():
    """Generates OAuth access token for Safaricom API."""
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        return {"error": "Missing API credentials in environment variables"}

    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()  # Raise an error for failed requests
        return response.json().get("access_token")
    except requests.RequestException as e:
        return {"error": f"Failed to fetch access token: {str(e)}"}
