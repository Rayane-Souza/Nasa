from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime, timedelta
from .models import Asteroide
from .serializers import AsteroideSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

NASA_API_KEY = 'na8I8Z0xq2MlYS6y1XPq88kPtsxhixCLnnzU7Wci'

def index(request):
    asteroids = Asteroide.objects.all()
    return render(request, 'asteroids/index.html', {'asteroids': asteroids})

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
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': 'Erro ao entrar em contato com a API da NASA', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = response.json()
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
                miss_distance_km = miss_distance_au * 149597870.7  # Converte de AU para quilômetros
                absolute_magnitude_api = float(item.get('absolute_magnitude_h', 0))

                if (min_diameter <= max_diameter_api <= max_diameter and
                    relative_velocity <= relative_velocity_kmps and
                    miss_distance <= miss_distance_km and
                    absolute_magnitude <= absolute_magnitude_api):
                    asteroid = {
                        'name': item.get('name', 'Desconhecido'),
                        'min_diameter': min_diameter_api,
                        'max_diameter': max_diameter_api,
                        'relative_velocity': relative_velocity_kmps,
                        'miss_distance': miss_distance_km,
                        'absolute_magnitude': absolute_magnitude_api
                    }
                    asteroids.append(asteroid)

        if not asteroids:
            return Response({'message': 'Nenhum asteroide encontrado com os filtros aplicados'}, status=status.HTTP_200_OK)

        return Response({'asteroids': asteroids})
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

class AsteroideListView(APIView):
    def get(self, request, *args, **kwargs):
        asteroids = Asteroide.objects.all()
        serializer = AsteroideSerializer(asteroids, many=True)
        return Response(serializer.data)

class AsteroideCreateView(APIView):
    @swagger_auto_schema(
        request_body=AsteroideSerializer,
        responses={201: AsteroideSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = AsteroideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AsteroideDetailView(APIView):
    def get_object(self, pk):
        try:
            return Asteroide.objects.get(pk=pk)
        except Asteroide.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: AsteroideSerializer})
    def get(self, request, pk, *args, **kwargs):
        asteroid = self.get_object(pk)
        if asteroid is None:
            return Response({'error': 'Asteroide não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AsteroideSerializer(asteroid)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=AsteroideSerializer,
        responses={200: AsteroideSerializer, 400: 'Bad Request'}
    )
    def put(self, request, pk, *args, **kwargs):
        asteroid = self.get_object(pk)
        if asteroid is None:
            return Response({'error': 'Asteroide não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AsteroideSerializer(asteroid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Exclui o asteroide. Não é necessário corpo na requisição.",
        responses={204: 'No Content'}
    )
    def delete(self, request, pk, *args, **kwargs):
        asteroid = self.get_object(pk)
        if asteroid is None:
            return Response({'error': 'Asteroide não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        asteroid.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


import numpy as np
import joblib
import pandas as pd
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

modelo = joblib.load('./asteroids/mlp.pkl')  
scaler = joblib.load('./asteroids/dadosescalonados.pkl')  

def index(request):
    return render(request, 'asteroids/index.html')

@csrf_exempt
def verificar_asteroide(request):
    if request.method == 'POST':
        try:
           
            dados = json.loads(request.body)
            print("Dados recebidos no backend:", dados) 

            diametro_min = float(dados['diametro_min'])
            diametro_max = float(dados['diametro_max'])
            velocidade_relativa = float(dados['velocidade_relativa'])
            miss_distance = float(dados['miss_distance'])
            magnitude_absoluta = float(dados['magnitude_absoluta'])

            dados_entrada = pd.DataFrame([[diametro_min, diametro_max, velocidade_relativa, miss_distance, magnitude_absoluta]],
                                         columns=['est_diameter_min', 'est_diameter_max', 'relative_velocity', 'miss_distance', 'absolute_magnitude'])

            dados_entrada_scaled = scaler.transform(dados_entrada)

            predicao = modelo.predict(dados_entrada_scaled)
            print("Predição:", predicao)  

            probabilidade_array = modelo.predict_proba(dados_entrada_scaled)[0]
            probabilidade = probabilidade_array[1 if predicao[0] else 0] * 100
            print("Probabilidade de risco:", probabilidade) 

            predicao_str = 'Perigoso' if predicao[0] == 1 else 'Não Perigoso'

            return JsonResponse({'resultado': predicao_str, 'probabilidade': round(float(probabilidade), 2)})

        except Exception as e:
          
            print("Erro no backend:", str(e))  
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Método não permitido. Use POST.'})





