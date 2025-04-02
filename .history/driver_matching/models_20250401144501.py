from django.db import models
from auth_app.models import Driver, CarOwner

class DriverMatch(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    match_score = models.FloatField()

    def __str__(self):
        return f'Match between {self.car_owner.user.username} and {self.driver.user.username}'
