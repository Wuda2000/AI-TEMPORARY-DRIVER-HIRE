from django.contrib import admin
from .models import Review

# Check if Review is already registered
if not admin.site.is_registered(Review):
    admin.site.register(Review)
