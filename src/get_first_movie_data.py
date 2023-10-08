"""Busca la pelicula por el Titulo introducido y retorna
el ID de la primera pelicula de la lista"""
from src import search_movies_by_title, search_movie_by_id

def get_first_movie_data(query):
    """Funcion que retorna el id de la pelicula buscada"""
    movies = search_movies_by_title.search_movies_by_title(query)
    if len(movies) > 0: # type: ignore
        movie_id = movies[0]['id'] # type: ignore
        return search_movie_by_id.search_movie_by_id(movie_id)
    return None
