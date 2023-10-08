"""Formatear datos recibidos de la web"""

def formatting_language(language_code):
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

    return language_names.get(language_code, "Unknown")

def formatting_hours_minutes(runtime):
    hours, minutes = divmod(runtime, 60)
    formatted_time = f"{hours}h {minutes}m"
    return formatted_time
