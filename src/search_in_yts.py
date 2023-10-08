"""Extraer torrents de (yts.mx/)"""
import json
import requests

def get_torrent_links(imdb_id):
    url = f"https://yts.mx/api/v2/list_movies.json?query_term={imdb_id}"
    try:
        response = requests.get(url, timeout=25)
        data = json.loads(response.text)

        if "data" in data and "movies" in data["data"]:
            movies = data["data"]["movies"]
            if movies:
                movie = movies[0]
                torrents = movie["torrents"]
                links_with_quality = [
                    (torrent["url"], torrent["quality"]) for torrent in torrents]
                return links_with_quality
        return []
    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud a la API:", error)
        return None

def get_movie_data(imdb_id):
    url = f'https://yts.mx/api/v2/movie_details.json?imdb_id={imdb_id}&with_images=false&with_cast=true'
    try:
        response = requests.get(url, timeout=25)
        data = json.loads(response.text)["data"]["movie"]
        return data
    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud a la API:", error)
        return None
    