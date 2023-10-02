'''Importamos las librerias  necesarias'''
import logging
import telebot
import pyfiglet
import requests

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate bot
bot = telebot.TeleBot('6666929357:AAFk2Wd7K13VPV8P-KB8X1A0Uu9pa46AENc')
word = pyfiglet.figlet_format('SERVER IS ONLINE')
print(word)


@bot.message_handler(commands=['start'])
def handle_start(message):
    '''Funcion que da inicio al bot'''
    user_first_name = str(message.chat.first_name)
    # current_time = datetime.datetime.now().time()
    welcome_message = f"🎉Bienvenido {user_first_name}! \n🔍Escribe el título de la película que deseas buscar..."

    logger.info("El usuario %s ha iniciado el bot.", user_first_name)

    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    '''Funcion para buscar peliculas por el titulo y devuelve la informacion'''
    user_first_name = str(message.chat.first_name)
    user_input = message.text
    print(f"El usuario {user_first_name} esta buscando '{user_input}'")
    bot.send_message(message.chat.id, "Espere por favor, buscando...!")
    try:
        # Set the API key (https://www.themoviedb.org/ )
        api_key = "efcfe9f6ebd1de85441306f3a65d6159"

        # Set the base URL of the API
        base_url = "https://api.themoviedb.org/3/"

        # Set the endpoint for movie search
        endpoint = "search/movie"

        # Set the query parameters
        params = {
            "api_key": api_key,
            "query": user_input,  # Replace with the actual movie title
            "language": "es",  # Set language to Spanish
            "page": 1  # Set the page number
        }

        # Make the API request Spanish
        response = requests.get(base_url + endpoint,
                                params=params, timeout=10.001)
        # Raise an exception if an error occurs with the API request
        response.raise_for_status()

        # Get the JSON data from the response
        data = response.json()

        # Extract the list of movies from the response
        results = data["results"]

        if results:

            # Get the first movie
            first_movie = results[0]

            # Extract the desired data
            # poster_path = first_movie["poster_path"]
            original_title = first_movie["original_title"]
            title = first_movie["title"]
            overview = first_movie["overview"]
            original_language = first_movie["original_language"]
            movie_id = first_movie["id"]

            # Formatear la Sinopsis(overview) para q el mensaje no supere los 1024 characters
            num_caract = 600
            substring = overview[:num_caract]

            # Formatear el lenguaje original de la pelicula
            def get_language_name(original_language):
                language_names = {
                    "en": "Inglés",
                    "es": "Español",
                    "fr": "Francés",
                    "pt": "Portugués",
                    "it": "Italiano",
                    "ja": "Japonés",
                    "ko": "Coreano",
                    "ru": "Ruso",
                    "uk": "Ucraniano"
                }

                return language_names.get(original_language, "Unknown")

            language_name = get_language_name(original_language)

            # Get the details of the movie
            movie_details_endpoint = f"movie/{movie_id}"
            details_params = {
                "api_key": api_key,
                "language": "es"  # Set language to Spanish
            }
            details_response = requests.get(base_url + movie_details_endpoint,
                                            params=details_params, timeout=10.001)
            # Raise an exception if an error occurs with the API request
            details_response.raise_for_status()
            details_data = details_response.json()

            # Get the genres of the movie
            genres = details_data.get("genres")

            # Get the IMDb_ID of the movie
            imdb_id = details_data.get("imdb_id")

            # Extract torrents links
            def get_torrent_links(imdb_id):
                url = f"https://yts.mx/api/v2/list_movies.json?query_term={imdb_id}"
                response = requests.get(url, timeout=10.001)
                data = response.json()

                if "data" in data and "movies" in data["data"]:
                    movies = data["data"]["movies"]
                    if movies:
                        movie = movies[0]
                        torrents = movie["torrents"]
                        links_with_quality = [
                            (torrent["url"], torrent["quality"]) for torrent in torrents]
                        return links_with_quality
                return []

            torrent_links = get_torrent_links(imdb_id)

            message_torrent ="Torrent Links:\n"
            for link, quality in torrent_links:
                message_torrent += f"🥇 Quality: {quality}\n🔗 Torrent Link: {link}"'\n''\n'
            # Make the HTTP GET request to the API
            response = requests.get(
                f"https://yts.mx/api/v2/movie_details.json?with_images=false&with_cast=true&imdb_id={imdb_id}", timeout=10.001)

            # Check if the request was successful (status code 200)
            response.raise_for_status()
            # Get the JSON data from the response
            movie_details = response.json()["data"]["movie"]

            # Extract all genre names
            genre_names = [genre["name"] for genre in genres]
            formatted_genres = ' #'.join(genre_names)

            # Extraer el valor de "runtime" de los datos de la primera pelicula
            runtime_in_minutes = movie_details["runtime"]

            # Convertir "runtaime" en horas y minutos
            hours, minutes = divmod(runtime_in_minutes, 60)

            def format_hours_minutes(hours, minutes):

                formatted_time = f"{hours}h {minutes}m"
                return formatted_time

            formatted_time = format_hours_minutes(hours, minutes)

            # Set the query parameters for search the original image in English
            params_en = {
                "api_key": api_key,
                "query": user_input,
                "language": "en",  # Set language to English
                "page": 1  # Set the page number
            }

            # Make the API request
            response = requests.get(base_url + endpoint,
                                    params=params_en, timeout=10.001)
            # Raise an exception if an error occurs with the API request English
            response.raise_for_status()

            # Get the JSON data from the response English
            data = response.json()

            # Extract the list of movies from the response English
            results = data["results"]

            # Get the first movie English
            first_movie_english = results[0]

            poster_path = first_movie_english["poster_path"]

            # Evaluate what if the best quality image
            # Add the desired qualities in the order you want to check
            qualities = ["w500"]  # Incluide "w780", "original"

            # Construct the API endpoint URL for fetching the image details
            api_url = f"https://api.themoviedb.org/3/configuration?api_key={api_key}"

            # Make a GET request to fetch the configuration details
            response = requests.get(api_url, timeout=10.001)
            if response.status_code != 200:
                print("Failed to fetch configuration details")
                exit()

            # Extract the base URL for images from the response
            base_url = response.json()["images"]["secure_base_url"]

            # Initialize the best quality link and its width as None
            best_quality_link = None
            best_quality_width = 0

            # Iterate over the qualities to check the availability of each quality
            for quality in qualities:
                # Construct the complete image URL for the current quality
                image_url = f"{base_url}{quality}{poster_path}"

                # Make a GET request to the image URL
                response = requests.get(image_url, timeout=10.001)

                # Check if the request was successful (status code 200) and the content type is an image
                if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
                    # Extract the width of the available image
                    width = int(response.headers["content-length"])

                    # Update the best quality link if the current quality is higher than the previous best
                    if width > best_quality_width:
                        best_quality_link = image_url
                        best_quality_width = width

            try:
                bot.send_photo(message.chat.id, best_quality_link, f"📺 Título: {original_title}" '\n'
                               f"🖥 Otro Título: {title}" '\n'
                               f"📆 Año: {movie_details['year']}" '\n'
                               f"🎙 Audio: {language_name}" '\n'
                               f"🕰 Duración: {formatted_time}" '\n'
                               f"🌟 IMDb: {movie_details['rating']}" '\n'
                               f"🎟 Reparto: {', '.join([cast['name']for cast in movie_details['cast'][:4]])}"'\n'
                               f"🔣 Géneros: #{formatted_genres}"'\n''\n'
                               f"🏷 Sinopsis: {substring}"'\n''\n'
                               f"▶️ DESCARGAR ▶️"'\n''\n'
                               f"⚠️ Subtítulos en los comentarios ⚠️")
                bot.send_message(message.chat.id, message_torrent)
                print("Busqueda completada!!!")
            except telebot.apihelper.ApiException as err:
                logger.error('BadRequest error: %s', err)
                bot.send_message(
                    message.chat.id, 'Se produjo un error al procesar su solicitud. Por favor, inténtelo de nuevo.')
        else:
            bot.send_message(
                message.chat.id, "No se encontraron resultados para su consulta.")
            # If the request was not successful, print the status code
            logger.error(
                "No se encontraron resultados para la consulta del usuario.")
            logger.error("Código de estado: %s", response.status_code)

    except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as error:
        logger.error(
            "Se produjo un error en la solicitud de la API: %s", str(error))
        bot.send_message(
            message.chat.id, "Se produjo un error al procesar su solicitud. Por favor, inténtelo de nuevo.")


bot.polling(none_stop=True)
