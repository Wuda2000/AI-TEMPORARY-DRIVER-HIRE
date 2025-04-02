# Utility functions for auth_app

import jwt
import datetime
from django.core.mail import send_mail
from django.conf import settings

def generate_token(user):
    """Generate a token for the user."""
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token expires in 1 day
        'iat': datetime.datetime.utcnow()  # Issued at
    }
    secret_key = 'your_secret_key'  # Replace with your actual secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validate_email(email):
    """Validate the email format."""
    pass

def send_verification_email(user):
    """Send a verification email to the user."""
    token = generate_token(user)
    subject = 'Verify your email'
    message = f'Please verify your email by clicking the link: {settings.FRONTEND_URL}/verify?token={token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
