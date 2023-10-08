'''Archivo ejecutable'''
import logging
import os
import sys
import telebot
import pyfiglet

from src import get_first_movie_data, search_in_yts, search_image, format_data
from config import BOT_TOKEN, NUM_CHARACTER

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_ID = (717325553,)

# Instantiate bot
bot = telebot.TeleBot(BOT_TOKEN)

word = pyfiglet.figlet_format('SERVER IS ONLINE')
print(word)

@bot.message_handler(commands=['start'])
def handle_start(message):
    '''Mensaje de bienvenida al usuario'''
    user = str(message.chat.first_name)

    welcome_message = f"🎉Bienvenido {user}! \n🔍Escribe el título de la película que deseas buscar.."

    logger.info("El usuario %s ha iniciado el bot.", user)

    bot.send_message(message.chat.id, welcome_message)

def is_admin(chat_id, info=True):
    if chat_id in ADMIN_ID:
        return True
    else:
        if info:
            print(f'{chat_id} no esta autorizado')
            bot.send_message(chat_id, "No estas autorizado", parse_mode="html")
        return False

@bot.message_handler(commands=["restart"])
def handle_restart(message):
    """Reinicia el bot"""
    logger.info("### Reiniciando el BOT ###\n")
    bot.send_message(message.chat.id, "### Reiniciando el BOT ###", parse_mode="html")
    bot.stop_polling()
    os.execv(sys.executable, [sys.executable] + sys.argv + sys.argv)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    '''Funcion que envia el poster, junto con la informacion del 
    titulo de la pelicula entrado por el Usuario y los respectivos torrents'''
    try:
        user = str(message.chat.first_name)
        user_input = message.text
        logger.info("El usuario %s esta buscando '%s'", user, user_input)
        bot.send_message(message.chat.id, "Espere por favor, buscando...!")

        movie_title = user_input
        movie_data = get_first_movie_data.get_first_movie_data(movie_title)
        if movie_data:
            original_title = movie_data['original_title']
            other_title = movie_data["title"]
            year = movie_data["release_date"][:4]
            original_language = format_data.formatting_language(movie_data["original_language"])
            formatted_minutes = format_data.formatting_hours_minutes(movie_data["runtime"])
            overview = movie_data["overview"]
            sub_overview = overview[:NUM_CHARACTER]
            imdb_id = movie_data["imdb_id"]
            genres = [genre['name'] for genre in movie_data['genres']]
            movie_id = movie_data["id"]

            image = search_image.search_image_by_id(movie_id)
            poster = f"https://image.tmdb.org/t/p/w500{image}"

            get_data = search_in_yts.get_movie_data(imdb_id)
            if get_data:
                rating = get_data["rating"]

                bot.send_photo(message.chat.id, photo=poster,
                               caption=f"📺 Título: {original_title}" '\n'
                                        f"🖥 Otro Título: {other_title}" '\n'
                                        f"📆 Año: {year}" '\n'
                                        f"🎙 Audio: {original_language}" '\n'
                                        f"🕰 Duración: {formatted_minutes}" '\n'
                                        f"🌟 IMDb: {rating}" '\n'
                                        f"🎟 Reparto: {', '.join([cast['name']for cast in get_data['cast'][:4]])}"'\n'
                                        f"🔣 Géneros: #{' #'.join(genres)}"'\n''\n'
                                        f"🏷 Sinopsis: {sub_overview}"'\n''\n'
                                        f"▶️ DESCARGAR ▶️"'\n''\n'
                                        f"⚠️ Subtítulo en los comentarios ⚠️")

            message_torrent = search_in_yts.get_torrent_links(imdb_id)
            if message_torrent:
                send_torrent = "Torrent Links:\n"
                for link, quality in message_torrent:
                    send_torrent += f"🥇 Calidad: {quality}\n🔗 Torrent Link: {link}"'\n''\n'
                bot.send_message(message.chat.id, send_torrent)
                logger.info("El usuario %s ha finalizado la búsqueda con exito", user)
    except Exception as e:
        logger.exception("Ocurrió un error durante la búsqueda de películas: %s", e)
        error_message = "Ocurrió un error al buscar la película. Por favor, inténtalo nuevamente."
        bot.send_message(message.chat.id, error_message)

if __name__ == '__main__':
    print("### Iniciando el Bot... ###")
    bot.infinity_polling()
