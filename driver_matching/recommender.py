import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import DriverProfile

def get_driver_recommendations(selected_driver):
    all_drivers = list(DriverProfile.objects.exclude(id=selected_driver.id))
    
    if not all_drivers:
        return []

    selected_vector = np.array([
        selected_driver.age,
        selected_driver.qualification_years,
        float(selected_driver.payment_range)
    ]).reshape(1, -1)

    driver_vectors = np.array([
        [driver.age, driver.qualification_years, float(driver.payment_range)]
        for driver in all_drivers
    ])

    similarities = cosine_similarity(selected_vector, driver_vectors)[0]
    
    sorted_indices = np.argsort(similarities)[::-1]
    recommended_drivers = [all_drivers[i] for i in sorted_indices[:5]]

    return recommended_drivers
