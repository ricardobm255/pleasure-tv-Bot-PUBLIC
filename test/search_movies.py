import requests
import json

def search_movies_by_title(title, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": title,
        "language": "es",
        "page": 1
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = json.loads(response.text)

        results = data["results"]

        if results:
            return results
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error al hacer la solicitud a la API:", e)
        return None

# Ejemplo de uso
api_key = "7c35175bd929415d243d6bf2e1a6bb02"
movie_title = "Avengers"
movies = search_movies_by_title(movie_title, api_key)

if movies:
    for movie in movies:
        print("Título:", movie["title"])
        print("Descripción:", movie["overview"])
        print("----")
else:
    print("No se encontraron películas con ese título.")