from django.db import models
class Prediction(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    housing_median_age = models.FloatField(default = 0)
    total_rooms = models.FloatField(default = 0)
    population = models.FloatField(default = 0)
    households = models.FloatField(default=0)
    median_income = models.FloatField(default = 0)
    predicted_price = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_price}"
