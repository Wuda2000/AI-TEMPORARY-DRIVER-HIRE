import requests
from django.http import JsonResponse
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
import json
from .tracking_module import update_driver_location, get_driver_location
from django.shortcuts import get_object_or_404
from .models import Trip


def update_location(request):

    """
    Handles location updates for authenticated drivers.
    Rate limited to 10 requests per minute per IP.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            driver_id = request.user.unique_id  # Ensures only logged-in drivers update their location
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude is None or longitude is None:
                return JsonResponse({"error": "Missing parameters"}, status=400)

            update_driver_location(driver_id, latitude, longitude)
            return JsonResponse({"message": "Location updated successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def get_location(request, driver_id):
    """
    Retrieves the last known location of a driver.
    Requires authentication.
    """
    location = get_driver_location(driver_id)
    if location:
        return JsonResponse({"driver_id": driver_id, "latitude": location[0], "longitude": location[1]})
    return JsonResponse({"error": "Driver location not found"}, status=404)

@login_required
def calculate_eta(request):
    """
    Fetches the estimated time of arrival (ETA) using OpenRouteService.
    """
    from_coords = request.GET.get("from")
    to_coords = request.GET.get("to")

    if not from_coords or not to_coords:
        return JsonResponse({"error": "Missing coordinates"}, status=400)

    from_coords = from_coords.split(",")
    to_coords = to_coords.split(",")

    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [
            [float(from_coords[1]), float(from_coords[0])],  # [longitude, latitude]
            [float(to_coords[1]), float(to_coords[0])]
        ]
    }

    response = requests.post(ors_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        eta = round(data["routes"][0]["summary"]["duration"] / 60, 2)  # Convert seconds to minutes
        return JsonResponse({"eta": f"{eta} min"})

    return JsonResponse({"error": "Failed to fetch ETA"}, status=400)

@login_required
def trip_details(request):
    """
    API to return pickup and arrival locations.
    """
    trip_id = request.GET.get('trip_id')  # Ensure frontend passes this
    if not trip_id:
        return JsonResponse({"error": "Trip ID is required"}, status=400)

    trip = get_object_or_404(Trip, id=trip_id)
    return JsonResponse({
        "pickup_lat": trip.pickup_latitude,
        "pickup_lng": trip.pickup_longitude,
        "arrival_lat": trip.arrival_latitude,
        "arrival_lng": trip.arrival_longitude
    })
