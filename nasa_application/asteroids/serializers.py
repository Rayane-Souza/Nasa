# asteroids/serializers.py
from rest_framework import serializers
from .models import Asteroide

class AsteroideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroide
        fields = ['name', 'min_diameter', 'max_diameter', 'relative_velocity', 'miss_distance', 'absolute_magnitude']
