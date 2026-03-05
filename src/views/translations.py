SUPPORTED_LANGS=["English", "Español"]

TRANSLATIONS=[
    {
        "English": "Your Storage",
        "Español": "Tú Almacenamiento"
    },
    {
        "English": "Your club",
        "Español": "Tú club"
    },
    {
        "English": "Welcome Back Trainer!",
        "Español": "¡Bienvenido nuevamente entrenador!"
    },
    {
        "English": "Daily Races",
        "Español": "Carreras Diarias"
    },
    {
        "English": "Scouting",
        "Español": "Escultismo"
    },
    {
        "English": "Choose a language",
        "Español": "Elige un idioma"
    },
    {
        "English": "Start my adventure",
        "Español": "Comenzar mi aventura"
    }
]

def tr(lang, index):
    return TRANSLATIONS[index%len(TRANSLATIONS)][lang]
