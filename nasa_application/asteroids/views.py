# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from .models import Asteroide  
# from datetime import datetime, timedelta


# NASA_API_KEY = 'na8I8Z0xq2MlYS6y1XPq88kPtsxhixCLnnzU7Wci'


# class AsteroideSearchView(APIView):
#     def get(self, request, *args, **kwargs):
#         min_diameter = float(request.GET.get('min_diameter', 0))
#         max_diameter = float(request.GET.get('max_diameter', 1000000))
#         relative_velocity = float(request.GET.get('relative_velocity', 0))
#         miss_distance = float(request.GET.get('miss_distance', 0))
#         absolute_magnitude = float(request.GET.get('absolute_magnitude', 0))

#         start_date = datetime.now().strftime('%Y-%m-%d')
#         end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

#         url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}'

#         try:
#             response = requests.get(url)
#             response.raise_for_status() 
#             data = response.json()
#         except requests.exceptions.RequestException as e:
#             return Response(
#                 {'error': 'Erro ao entrar em contato com a API da NASA', 'message': str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         if 'near_earth_objects' not in data:
#             return Response(
#                 {'error': 'Não foram encontrados objetos próximos à Terra na resposta da API da NASA'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         asteroids = []

#         for date, asteroid_list in data['near_earth_objects'].items():
#             for item in asteroid_list:
#                 min_diameter_api = item.get('estimated_diameter', {}).get('kilometers', {}).get('min', 0)
#                 max_diameter_api = item.get('estimated_diameter', {}).get('kilometers', {}).get('max', 0)
#                 relative_velocity_kmps = float(
#                     item.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_second', 0)
#                 )
#                 miss_distance_au = float(
#                     item.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('astronomical', 0)
#                 )
#                 miss_distance_km = miss_distance_au * 149597870.7
#                 absolute_magnitude_api = float(item.get('absolute_magnitude_h', 0))

#                 diameter_diff = min(abs(min_diameter - min_diameter_api), abs(max_diameter - max_diameter_api))
#                 velocity_diff = abs(relative_velocity - relative_velocity_kmps)
#                 distance_diff = abs(miss_distance - miss_distance_km)
#                 magnitude_diff = abs(absolute_magnitude - absolute_magnitude_api)

#                 asteroid = {
#                     'name': item.get('name', 'Desconhecido'),
#                     'min_diameter': min_diameter_api,
#                     'max_diameter': max_diameter_api,
#                     'relative_velocity': relative_velocity_kmps,
#                     'miss_distance': miss_distance_km,
#                     'absolute_magnitude': absolute_magnitude_api,
#                     'diameter_diff': diameter_diff,
#                     'velocity_diff': velocity_diff,
#                     'distance_diff': distance_diff,
#                     'magnitude_diff': magnitude_diff
#                 }
#                 asteroids.append(asteroid)

#         asteroids = sorted(
#             asteroids,
#             key=lambda x: (
#                 x['diameter_diff'] + x['velocity_diff'] + x['distance_diff'] + x['magnitude_diff']
#             )
#         )

#         asteroids = asteroids[:20] 

#         return Response({'asteroids': asteroids})


# def index(request):
#     asteroids = Asteroide.objects.all()

#     min_diameter = request.GET.get('min_diameter', None)
#     max_diameter = request.GET.get('max_diameter', None)
#     relative_velocity = request.GET.get('relative_velocity', None)
#     miss_distance = request.GET.get('miss_distance', None)
#     absolute_magnitude = request.GET.get('absolute_magnitude', None)

#     if min_diameter:
#         asteroids = asteroids.filter(diameter__gte=min_diameter)
#     if max_diameter:
#         asteroids = asteroids.filter(diameter__lte=max_diameter)
#     if relative_velocity:
#         asteroids = asteroids.filter(velocity__gte=relative_velocity)
#     if miss_distance:
#         asteroids = asteroids.filter(distance__lte=miss_distance)
#     if absolute_magnitude:
#         asteroids = asteroids.filter(magnitude__lte=absolute_magnitude)

#         return render(request, 'asteroids/index.html', {'asteroids': asteroids})



from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import joblib  
import os
import numpy as np
from datetime import datetime, timedelta
from .models import Asteroide

NASA_API_KEY = 'na8I8Z0xq2MlYS6y1XPq88kPtsxhixCLnnzU7Wci'

def carregar_modelo():
    try:
        modelo_path = os.path.join(os.path.dirname(__file__), 'modelo_rede_neural.pkl')
        modelo = joblib.load(modelo_path)
        return modelo
    except FileNotFoundError:
        print("Erro: O arquivo modelo_rede_neural.pkl não foi encontrado.")
        return None

modelo = carregar_modelo()

def predizer_perigo(diametro_min, diametro_max, velocidade_relativa, magnitude_absoluta, miss_distance):
    if modelo is None:
        return "Erro no modelo"

    dados_entrada = np.array([[diametro_min, diametro_max, velocidade_relativa, magnitude_absoluta, miss_distance]])
    
    previsao = modelo.predict(dados_entrada)
    
    return "Perigoso" if previsao[0] == 1 else "Não perigoso"

class AsteroideSearchView(APIView):
    def get(self, request, *args, **kwargs):
        min_diameter = float(request.GET.get('min_diameter', 0))
        max_diameter = float(request.GET.get('max_diameter', 1000000))
        relative_velocity = float(request.GET.get('relative_velocity', 0))
        miss_distance = float(request.GET.get('miss_distance', 0))
        absolute_magnitude = float(request.GET.get('absolute_magnitude', 0))

        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': 'Erro ao entrar em contato com a API da NASA', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if 'near_earth_objects' not in data:
            return Response(
                {'error': 'Não foram encontrados objetos próximos à Terra na resposta da API da NASA'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        asteroids = []

        for date, asteroid_list in data['near_earth_objects'].items():
            for item in asteroid_list:
                min_diameter_api = item.get('estimated_diameter', {}).get('kilometers', {}).get('min', 0)
                max_diameter_api = item.get('estimated_diameter', {}).get('kilometers', {}).get('max', 0)
                relative_velocity_kmps = float(
                    item.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_second', 0)
                )
                miss_distance_au = float(
                    item.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('astronomical', 0)
                )
                miss_distance_km = miss_distance_au * 149597870.7
                absolute_magnitude_api = float(item.get('absolute_magnitude_h', 0))

                asteroid = {
                    'name': item.get('name', 'Desconhecido'),
                    'min_diameter': min_diameter_api,
                    'max_diameter': max_diameter_api,
                    'relative_velocity': relative_velocity_kmps,
                    'miss_distance': miss_distance_km,
                    'absolute_magnitude': absolute_magnitude_api
                }
                asteroids.append(asteroid)

        return Response({'asteroids': asteroids})

def index(request):
    asteroids = Asteroide.objects.all()

    min_diameter = request.GET.get('min_diameter', None)
    max_diameter = request.GET.get('max_diameter', None)
    relative_velocity = request.GET.get('relative_velocity', None)
    miss_distance = request.GET.get('miss_distance', None)
    absolute_magnitude = request.GET.get('absolute_magnitude', None)

    if min_diameter:
        asteroids = asteroids.filter(diameter__gte=min_diameter)
    if max_diameter:
        asteroids = asteroids.filter(diameter__lte=max_diameter)
    if relative_velocity:
        asteroids = asteroids.filter(velocity__gte=relative_velocity)
    if miss_distance:
        asteroids = asteroids.filter(distance__lte=miss_distance)
    if absolute_magnitude:
        asteroids = asteroids.filter(magnitude__lte=absolute_magnitude)

   
    if request.method == 'POST':
      
        diametro_min = float(request.POST.get('diametro_min', 0))
        diametro_max = float(request.POST.get('diametro_max', 0))
        velocidade_relativa = float(request.POST.get('velocidade_relativa', 0))
        magnitude_absoluta = float(request.POST.get('magnitude_absoluta', 0))
        miss_distance = float(request.POST.get('miss_distance', 0)) 
        
        
        resultado = predizer_perigo(diametro_min, diametro_max, velocidade_relativa, magnitude_absoluta, miss_distance)
        
       
        return render(request, 'asteroids/index.html', {'resultado': resultado, 'asteroids': asteroids})

   
    return render(request, 'asteroids/index.html', {'asteroids': asteroids})

