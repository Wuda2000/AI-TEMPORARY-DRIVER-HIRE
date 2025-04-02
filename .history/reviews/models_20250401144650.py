from django.db import models
from auth_app.models import CarOwner, Driver

class Review(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.driver.user.username} by {self.car_owner.user.username}'
