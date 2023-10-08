"""Buscar peliculas por ID"""
import json
import requests
from config import API_KEY

def search_movie_by_id(movie_id):
    """Funcion que busca la pelicula por el id de themoviedb 
    y retorna toda la informacion en español"""
    base_url = "https://api.themoviedb.org/3/"
    movie_url = f'{base_url}/movie/{movie_id}'
    params = {
        'api_key': API_KEY,
        'language': 'es-ES'
    }
    try:
        response = requests.get(movie_url, params=params, timeout=25)
        response.raise_for_status()
        details_data = json.loads(response.text)
        if details_data:
            return details_data
    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud a la API:", error)
        return None
