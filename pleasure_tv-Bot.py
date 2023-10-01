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
bot = telebot.TeleBot('5900264461:AAHxo563dyySXhgq3_J06OFvb_v_WMfQlCQ')
word = pyfiglet.figlet_format('SERVER IS ONLINE')
print(word)


@bot.message_handler(commands=['start'])
def handle_start(message):
    '''Funcion que da inicio al bot'''
    user_first_name = str(message.chat.first_name)
    # current_time = datetime.datetime.now().time()
    welcome_message = f"Bienvenido {user_first_name}! 🎉\nel título de la película que desea buscar 🔍"

    logger.info("El usuario %s ha iniciado el bot.", user_first_name)

    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    '''Funcion para buscar peliculas por el titulo y devuelve la informacion'''
    user_input = message.text
    bot.send_message(message.chat.id, "Espere por favor, buscando...!")
    try:
        # Set the API key (sign up at https://www.themoviedb.org/ to obtain your own API key)
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

        # Make the API request
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
            poster_path = first_movie["poster_path"]
            original_title = first_movie["original_title"]
            title = first_movie["title"]
            overview = first_movie["overview"]
            original_language = first_movie["original_language"]
            movie_id = first_movie["id"]

            num_caract = 400
            substring = overview[:num_caract]

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

            # Make the HTTP GET request to the API
            response = requests.get(
                f"https://yts.mx/api/v2/movie_details.json?with_images=false&with_cast=false&imdb_id={imdb_id}", timeout=10.001)

            # Check if the request was successful (status code 200)
            response.raise_for_status()
            # Get the JSON data from the response
            movie_details = response.json()["data"]["movie"]

            # Extract all genre names
            genre_names = [genre["name"] for genre in genres]
            formatted_genres = ' #'.join(genre_names)

            # Evaluate what if the best quality image
            # Add the desired qualities in the order you want to check
            qualities = ["w500"]

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

            # Print the best quality link (if available)
            if best_quality_link:
                print("The link with the highest available quality:",
                      best_quality_link)
            else:
                print("No available image links found.")

            try:
                bot.send_photo(message.chat.id, best_quality_link, f"📺 Título: {original_title}" '\n'
                               f"🖥 Otro Título: {title}" '\n'
                               f"📆 Año: {movie_details['year']}" '\n'
                               f"🎙 Audio: {original_language}" '\n'
                               f"🕰 Duración: {movie_details['runtime']}" '\n'
                               f"🌟 IMDb: {movie_details['rating']}" '\n'
                               f"🔣 Géneros: #{formatted_genres}"'\n''\n'
                               f"🏷 Sinopsis: {substring}..."'\n''\n'
                               f"▶️ DESCARGAR ▶️"'\n''\n'
                               f"⚠️ Subtítulos en los comentarios ⚠️")
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
