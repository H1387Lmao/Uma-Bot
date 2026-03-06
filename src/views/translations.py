SUPPORTED_LANGS=["English", "Español"]

LANG_OFF = 0
MAIN_PAGE_OFF = LANG_OFF+2
BUTTON_OFF = MAIN_PAGE_OFF+3
STORAGE_OFF = BUTTON_OFF+2

TRANSLATIONS=[
    # Choose Language Setting
    {
        "English": "Choose a language",
        "Español": "Elige un idioma"
    },
    {
        "English": "Continue",
        "Español": "Continuar"
    },
    # Main Page
    {
        "English": "Welcome Back Trainer!",
        "Español": "¡Bienvenido entrenador!"
    },
    {
        "English": "Club",
        "Español": "Clubes"
    },
    {
        "English": "Settings",
        "Español": "Configuración"
    },
    # Main Page Buttons
    {
        "English": "Storage",
        "Español": "Almacenaje"
    },
    {
        "English": "Career",
        "Español": "Carerra"
    },
    {
        "English": "Scouting",
        "Español": "Búsqueda"
    },
    {
        "English": "Daily Races",
        "Español": "Carerras Diarias"
    },
    # Club Page Buttons
    {
        "English": "Your Club",
        "Español": "Tú Club"
    },
    {
        "English": "Find Clubs",
        "Español": "Buscar clubes"
    },
    {
        "English": "Pretty Derby Scout",
        "Español": ""
    },
    {
        "English": "Support Card Scout",
        "Español": ""
    },
]

def tr(lang, index):
    trans = TRANSLATIONS[index%len(TRANSLATIONS)]
    res = trans.get(lang)
    if not res:
        res = f"[no translation [{lang}] for {trans['English']:!r}]"
