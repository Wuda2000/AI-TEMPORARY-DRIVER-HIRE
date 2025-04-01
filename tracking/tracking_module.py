import redis
import os
from django.conf import settings

# Connect to Redis
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)
driver_locations = {}

def update_driver_location(driver_id, latitude, longitude):
    """
    Updates the driver's real-time location.
    """
    driver_locations[driver_id] = (latitude, longitude)

def get_driver_location(driver_id):
    """
    Retrieves the last known location of a driver.
    """
    return driver_locations.get(driver_id, None)

def get_all_driver_locations():
    """
    Retrieves all driver locations.
    """
    return driver_locations

def clear_driver_locations():
    """
    Clears all driver locations.
    """
    driver_locations.clear()
