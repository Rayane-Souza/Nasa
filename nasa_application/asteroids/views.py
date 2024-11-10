import requests
from django.http import JsonResponse
from django.shortcuts import render

NASA_API_KEY = 'Fvgf1YyhX9ARFS2xEpxvbgcoD6oTZqYwkmd2Hr4G'

def get_asteroids(request):
    min_diameter = float(request.GET.get('min_diameter', 0))  
    max_diameter = float(request.GET.get('max_diameter', 1000000)) 
    relative_velocity = float(request.GET.get('relative_velocity', 0))  
    miss_distance = float(request.GET.get('miss_distance', 0))  
    absolute_magnitude = float(request.GET.get('absolute_magnitude', 0))  

    url = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={NASA_API_KEY}'

    response = requests.get(url)
    data = response.json()

    asteroids = []

    for item in data['near_earth_objects']:
        min_diameter_api = item['estimated_diameter']['kilometers']['min']
        max_diameter_api = item['estimated_diameter']['kilometers']['max']

        relative_velocity_kmps = float(item['close_approach_data'][0]['relative_velocity']['kilometers_per_second'])

        miss_distance_au = float(item['close_approach_data'][0]['miss_distance']['astronomical'])

        miss_distance_km = miss_distance_au * 149597870.7

        absolute_magnitude_api = float(item['absolute_magnitude_h'])

        if (min_diameter <= min_diameter_api <= max_diameter and
            relative_velocity_kmps >= relative_velocity and
            miss_distance_km <= miss_distance and
            absolute_magnitude_api <= absolute_magnitude):
            asteroids.append({
                'name': item['name'],
                'min_diameter': min_diameter_api,
                'max_diameter': max_diameter_api,
                'relative_velocity': relative_velocity_kmps,
                'miss_distance': miss_distance_km,
                'absolute_magnitude': absolute_magnitude_api
            })

    return JsonResponse({'asteroids': asteroids})
def index(request):

    context = {
        'message': 'Bem-vindo à página inicial da aplicação de asteroides!'
    }
    return render(request, 'index.html', context)