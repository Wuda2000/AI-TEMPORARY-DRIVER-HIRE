from django.urls import path
from .views import update_location, get_location, calculate_eta

urlpatterns = [
    path('api/update_location/', update_location, name='update_location'),
    path('api/get_location/<int:driver_id>/', get_location, name='get_location'),
    path('api/calculate_eta/', calculate_eta, name='calculate_eta'),
]
