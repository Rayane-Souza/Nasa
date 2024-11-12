# asteroids/models.py
from django.db import models

class Asteroide(models.Model):
    name = models.CharField(max_length=100)
    min_diameter = models.FloatField()
    max_diameter = models.FloatField()
    relative_velocity = models.FloatField()
    miss_distance = models.FloatField()
    absolute_magnitude = models.FloatField()
    # Adicione outros campos conforme necessário
