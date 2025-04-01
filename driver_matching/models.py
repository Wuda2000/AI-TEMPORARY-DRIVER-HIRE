from django.db import models  
from django.contrib.auth import get_user_model  

User = get_user_model()  


class DriverMatch(models.Model):  
    driver = models.ForeignKey(  
        User,  
        on_delete=models.CASCADE,  
        related_name="driver_matches"  
    )  

    car_owner = models.ForeignKey(  
        User,  
        on_delete=models.CASCADE,  
        related_name="driver_matching_owner_matches"  
    )  
    trip_date = models.DateTimeField(auto_now_add=True)  
    match_score = models.FloatField(default=0.0)  

    def __str__(self):  
        return f"Match: {self.driver.username} with {self.car_owner.username} (Score: {self.match_score})"
