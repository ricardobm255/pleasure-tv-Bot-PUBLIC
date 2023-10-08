"""Buscar poster original de la pelicula por ID"""
import json
import requests
from config import API_KEY

def search_image_by_id(movie_id):
    """Funcion para buscar el poster con los parametros en ingles"""
    base_url = "https://api.themoviedb.org/3/"
    movie_url = f'{base_url}/movie/{movie_id}'
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }
    try:
        response = requests.get(movie_url, params=params, timeout=25)
        response.raise_for_status()
        details_data = json.loads(response.text)
        if details_data:
            image = details_data["poster_path"]
            return image
    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud a la API:", error)
        return None
