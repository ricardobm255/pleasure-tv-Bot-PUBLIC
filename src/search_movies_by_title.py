"""Busca la pelicula en sitio (https://www.themoviedb.org/)"""
import json
import requests
from config import API_KEY


def search_movies_by_title(query, api_key=API_KEY):
    """Funcion que busca la pelicula por el titulo introducido por el usuario
    y retorna los datos en español"""
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "language": "es"
    }
    try:
        response = requests.get(base_url, params=params, timeout=25)
        response.raise_for_status()
        data = json.loads(response.text)

        results = data["results"]
        if results:
            return results

    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud a la API:", error)
        return None
