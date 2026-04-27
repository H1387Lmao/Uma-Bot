import re
import unicodedata

FIGURE_SPACE = "\u2007"

def typewriter(text: str) -> str:
    result = []

    for char in text:
        if char == " ":
            result.append(FIGURE_SPACE)
            continue

        decomposed = unicodedata.normalize("NFD", char)

        base = decomposed[0]
        accents = decomposed[1:]

        code = ord(base)

        if 65 <= code <= 90:
            base = chr(0x1D670 + code - 65)
        elif 97 <= code <= 122:
            base = chr(0x1D68A + code - 97)
        elif 48 <= code <= 57:
            base = chr(0x1D7F6 + code - 48)

        result.append(base + accents)

    return "".join(result)

SUPPORTED_LANGS = ["English", "Español"]
DISABLED_LANGS = []#"Español"]
TRANSLATIONS = {
    "settings.lang": [
        {"English": "Choose a language", "Español": "Elige un idioma"},
        {"English": "Continue", "Español": "Continuar"},
    ],
    "ui.label": [
        {"English": "Back", "Español": "Atrás"},
    ],
    "page.titles": [
        {"English": "Welcome Back Trainer!", "Español": "¡Bienvenido de vuelta, entrenador!", "_emoji": "Tazuna"},
        {"English": "Club", "Español": "Club", "_emoji": "ui_club"},
        {"English": "Settings", "Español": "Configuración", "_emoji": "settings_icon"},
    ],
    "page.main.btns": [
        {"English": "Storage", "Español": "Almacenamiento", "_emoji": "ui_inventory"},
        {"English": "Career", "Español": "Carrera", "_emoji": "ui_career"},
        {"English": "Scouting", "Español": "Gacha", "_emoji": "ui_scouting"},
        {"English": "Daily Races", "Español": "Carreras", "_emoji": "ui_race"},
    ],
    "page.club.btns": [
        {"English": "Your Club", "Español": "Tu club", "_emoji": "ui_club"},
        {"English": "Find Clubs", "Español": "Buscar clubes", "_emoji": "ui_clubsearch"},
        {"English": "Leaderboards", "Español": "Ránking", "_emoji": None},
    ],
    "page.single_words": [
        {"English": "Options", "Español": "Opciones"}
    ],
    "page.settings.options": [
        {"English": "Triangle Gacha", "Español": "Gacha triangular", "_default": True, "_type": "toggle", "_id": "triangle_gacha"},
        {"English": "Skip Gacha", "Español": "Saltar gacha", "_default": False, "_type": "toggle", "_id": "skip_gacha"},
        {"English": "Compact UI", "Español": "Interfaz compacta", "_default": True, "_type": "toggle", "_id": "mobile_mode"},
        {"English": "Skip race", "Español": "Saltar carrera", "_default": True, "_type": "toggle", "_id": "skip_race"},
        {"English": "Language", "Español": "Idioma", "_default": "English", "_type": "choices", "_id": "lang", "_values": SUPPORTED_LANGS}
    ],
    "page.gacha.titles": [
        {"English": "🏇 Pretty Derby Scout", "Español": "🏇 Gacha de Pretty Derby"},
        {"English": "🃏 Support Card Scout", "Español": "🃏 Gacha de cartas de apoyo"},
    ],
    "page.gacha.spin_labels": [
        {"English": "150 | 1 Roll", "Español": "150 | 1 tirada"},
        {"English": "1500 | 10 Rolls", "Español": "1500 | 10 tiradas"},
    ],
    "page.gacha.result_one": [
        {"English": "🎉 You obtained **<0>**\n-# You have <1> carats left.",
         "Español": "🎉 ¡Obtuviste **<0>**!\n-# Te quedan <1> carats."},
    ],
    "page.gacha.carat_label": [
        {"English": "-# You have <0> carats<1> left.",
         "Español": "-# Te quedan <0> carats<1>."},
    ],
    "page.gacha.result_multi_rolling": [
        {"English": "-# Rolling <0> times!\n**<1>**",
         "Español": "-# ¡Tirando <0> veces!\n**<1>**"},
    ],
    "page.gacha.result_multi_done": [
        {"English": "-# Finished rolling!\n**<0>**",
         "Español": "-# ¡Tiradas completadas!\n**<0>**"},
    ],
    "page.storage.titles": [
        {"English": "Umamusume"},
        {"English": "Support Cards", "Español": "Cartas de apoyo"},
        {"English": "Items", "Español": "Objetos"},
        {"English": "Badges", "Español": "Insignias"}
    ],
    "page.storage.no_umas": [
        {"English": "You don't have anything!", "Español": "¡No tienes nada!"},
    ],
    "page.credits": [
        {"English": "CREDITS", "Español": "CRÉDITOS"},
        {"English": "Assets", "Español": "Recursos"},
        {"English": "In-game sprites", "Español": "Sprites del juego"},
        {"English": "Development", "Español": "Desarrollo"},
        {"English": "Programmer", "Español": "Programador"},
        {"English": "Community", "Español": "Comunidad"},
        {"English": "English Manager", "Español": "Responsable de inglés"},
        {"English": "Spanish Manager", "Español": "Responsable de español"},
    ],
    "cmd.start": [
        {"English": "start", "Español": "iniciar"},
    ],
    "cmd.profile": [
        {"English": "profile", "Español": "perfil"},
    ],
    "ui.loading": [
        {"English": "<0>Please wait while the bot starts to load!",
         "Español": "<0>Por favor, espera mientras el bot termina de cargarse."},
        {"English": "This page will automatically refresh after the bot loads successfully!",
         "Español": "Esta página se actualizará automáticamente cuando el bot termine de cargarse."},
    ],
    "errors.insufficient_currency": [
        {"English": "Insufficient!", "Español": "¡Fondos insuficientes!"},
        {"English": "You don't have enough carats!", "Español": "¡No tienes suficientes carats!"},
    ],

    "stats.spd":   [{"English": "Speed",   "Español": "Velocidad"}],
    "stats.stm":   [{"English": "Stamina", "Español": "Resistencia"}],
    "stats.pwr":   [{"English": "Power",   "Español": "Potencia"}],
    "stats.gut":   [{"English": "Guts",    "Español": "Coraje"}],
    "stats.wit":   [{"English": "Wit",     "Español": "Ingenio"}],

    "training.header": [
        {"English": "<0><1>⚡ <2>"}
    ],
    "career.header": [
        {"English": "## <0> **<1>**\n-# **<2>** 📅 **<3> <4> <5>**",
         "Español": "## <0> **<1>**\n-# **<2>** 📅 **<3> <4> <5>**"}
    ],
    "career.half.early": [{"English": "Early", "Español": "Inicio"}],
    "career.half.late":  [{"English": "Late",  "Español": "Final"}],

    "career.months": [
        {"English": "January", "Español": "Enero"},
        {"English": "February", "Español": "Febrero"},
        {"English": "March", "Español": "Marzo"},
        {"English": "April", "Español": "Abril"},
        {"English": "May", "Español": "Mayo"},
        {"English": "June", "Español": "Junio"},
        {"English": "July", "Español": "Julio"},
        {"English": "August", "Español": "Agosto"},
        {"English": "September", "Español": "Septiembre"},
        {"English": "October", "Español": "Octubre"},
        {"English": "November", "Español": "Noviembre"},
        {"English": "December", "Español": "Diciembre"}
    ],
    "career.year": [
        {"English": "Junior Year", "Español": "Año junior"},
        {"English": "Classic Year", "Español": "Año clásico"},
        {"English": "Senior Year", "Español": "Año senior"},
    ],

    "training.skill_info": [
        {"English": "Skill Points: <0>  |  Skills: <1>",
         "Español": "Puntos de habilidad: <0>  |  Habilidades: <1>"},
    ],
    "training.skill_pts_label": [
        {"English": "SP", "Español": "SP"},
    ],
    "training.train_button": [
        {"English": "Train <0>", "Español": "Entrenar <0>"},
    ],

    "career.btn.train": [{"English": "Train", "Español": "Entrenar"}],
    "career.btn.rest": [{"English": "Rest", "Español": "Descansar"}],
    "career.btn.recreate": [{"English": "Recreation", "Español": "Recreación"}],
    "career.btn.restcreate": [{"English": "Rest & Recreation", "Español": "Descanso y recreación"}],
    "career.btn.infirmary": [{"English": "Infirmary", "Español": "Enfermería"}],
    "career.btn.race": [{"English": "Race", "Español": "Carrera"}],
    "career.btn.skills": [{"English": "Skills", "Español": "Habilidades"}],
    "career.btn.complete": [{"English": "Complete Career", "Español": "Completar carrera"}],
    "career.btn.complete_confirm": [{"English": "Are you sure?", "Español": "¿Estás seguro?"}],
    "career.btn.end": [{"English": "End Career", "Español": "Finalizar carrera"}],

    "career.goal.next": [{"English": "Next Goal", "Español": "Próximo objetivo"}],
    "career.goal.completed": [{"English": "All Goals Completed", "Español": "Todos los objetivos completados"}],
    "career.goal.header": [{"English": "<0> <1>"}],
    "career.turns": [
        {"English": "in <0> turns", "Español": "en <0> turnos"},
        {"English": "in <0> turn", "Español": "en <0> turno"}
    ],
    "career.conditions": [{"English": "Conditions", "Español": "Condiciones"}],
    "career.over.title": [{"English": "Career Over", "Español": "Carrera terminada"}],

    "career.select.title": [
        {"English": "### Choose Your Uma", "Español": "### Elige tu Uma"},
    ],
    "career.select.start": [
        {"English": "Start Career! 🏁", "Español": "¡Iniciar carrera! 🏁"},
    ],

    "career.complete.title": [
        {"English": "🏆 Career Complete – <0>!", "Español": "🏆 ¡Carrera completada – <0>!"},
    ],
    "career.complete.stats": [
        {"English": "Fans: <0>  |  Goals: <1>/<2>",
         "Español": "Fans: <0>  |  Objetivos: <1>/<2>"},
    ],
    "career.complete.view": [
        {"English": "View Summary", "Español": "Ver resumen"},
    ],
    "career.summary.fans": [
        {"English": "<0> Total Fans", "Español": "<0> fans totales"},
    ],
    "career.attained_condition": [
        {"English": "You attained the condition **<0>**", "Español": "Has obtenido la condición **<0>**"},
    ],
    "career.removed_conditions": [
        {"English": "Removed conditions", "Español": "Condiciones eliminadas"},
    ],

    "career.skillpoints.label": [
        {"English": "SP", "Español": "SP"},
    ],

    "career.skills.buy": [
      {"English": "Buy Skills", "Español": "Comprar habilidades"}
    ],
    "career.skills.title": [
      {"English": "Skill Shop", "Español": "Tienda de habilidades"}
    ],

    "race.schedule.title": [
        {"English": "### Schedule a Race\n-# **<0>**  📅 **<1> <2> <3>**",
        "Español": "### Programar una carrera\n-# **<0>** 📅 **<1> <2> <3>**"},
    ],
    "race.schedule.queued": [
        {"English": "Queued <0>", "Español": "<0> en cola"},
    ],
    "race.schedule.pick": [
        {"English": "Schedule", "Español": "Programar"},
    ],
    "race.result.won": [
        {"English": "## ***Won!***", "Español": "## ***¡Ganaste!***"},
    ],
    "race.result.lost": [
        {"English": "## ***Lost!***", "Español": "## ***¡Perdiste!***"},
    ],
    "race.result.placement": [
        {"English": "— <0> Place", "Español": "— puesto <0>"},
    ],
    "race.result.reward.career": [
        {"English": "-# You gained **<0>** fans, **<1>** SP, and **<2>** carats!\n",
         "Español": "-# ¡Ganaste **<0>** fans, **<1>** SP y **<2>** carats!\n"},
    ],
    "race.result.reward.daily": [
        {"English": "-# You gained **<0>** carats and **<1>** exp!",
         "Español": "-# ¡Ganaste **<0>** carats y **<1>** exp!"},
    ],
    "race.result.club.title": [
        {"English": "Club Race has finished!", "Español": "¡La carrera del club ha terminado!"},
    ],
    "race.result.club.entry": [
        {"English": "<0> ***<1>***\n-# <2> <3>\n",
         "Español": "<0> ***<1>***\n-# <2> <3>\n"},
    ],
    "skills.none": [
        {"English": "No skills yet!", "Español": "¡Aún no tienes habilidades!"},
    ],

    "goal.ura": [
        {"English": "Win the <0>", "Español": "Gana el <0>"},
    ],
    "goal.debut": [
        {"English": "Participate in your debut race", "Español": "Participa en tu carrera de debut"},
    ],
    "goal.fans": [
        {"English": "Accumulate <0> fans", "Español": "Acumula <0> fans"},
    ],
    "goal.req.participate": [{"English": "Participate <0>", "Español": "Participa en <0>"}],
    "goal.req.top5": [{"English": "Finish top 5 <0>", "Español": "Termina entre los 5 primeros en <0>"}],
    "goal.req.top3": [{"English": "Finish top 3 <0>", "Español": "Termina entre los 3 primeros en <0>"}],
    "goal.req.win": [{"English": "Win <0>", "Español": "Gana <0>"}],

    "errors.career.no_uma": [
        {"English": "Can't Start Career", "Español": "No se puede iniciar la carrera"},
        {"English": "You don't have an Uma yet, roll first!", "Español": "¡Aún no tienes una Uma, tira primero!"},
    ],
    "errors.career.ended": [
        {"English": "Career Ended!", "Español": "¡La carrera ha terminado!"},
        {"English": "Your career is complete. Your fans have been saved.",
         "Español": "Tu carrera ha terminado. Tus fans se han guardado."},
    ],
    "errors.training.fail.low_energy": [
        {"English": "Training Failed! Mood worsened.", "Español": "¡Entrenamiento fallido! El ánimo empeoró."},
        {"English": "Not enough energy! Mood worsened.",
         "Español": "¡No tienes suficiente energía! El ánimo empeoró."},
    ],
    "errors.training.fail.random_failure": [
        {"English": "Training Failed", "Español": "Entrenamiento fallido"},
        {"English": "Training slipped up this time. Mood dropped.",
         "Español": "El entrenamiento falló esta vez. El ánimo bajó."},
    ],
    "errors.training.fail.skipped_by_condition": [
        {"English": "Training Skipped", "Español": "Entrenamiento omitido"},
        {"English": "A condition forced training to be skipped.",
         "Español": "Una condición obligó a omitir el entrenamiento."},
    ],
    "errors.training.fail.game_over": [
        {"English": "Career Over", "Español": "Carrera terminada"},
        {"English": "The career has ended.",
         "Español": "La carrera ha terminado."},
    ],
    "errors.race.none": [
        {"English": "No Races Available", "Español": "No hay carreras disponibles"},
        {"English": "No races match your current month or fan count.",
         "Español": "No hay carreras que coincidan con tu mes actual o tu número de fans."},
    ],
    "errors.skills.no_sp": [
        {"English": "Purchase Failed", "Español": "Compra fallida"},
        {"English": "Not enough skill points!", "Español": "¡No tienes suficientes puntos de habilidad!"},
    ],
    "errors.club.cant_leave": [
        {"English": "Unable to leave!"},
        {"English": "Please transfer you club first!"},
    ],
    "errors.club.cant_invite": [
        {"English": "Unable to invite!"},
        {"English": "Cannot DM target user!"},
    ],
    "condition.PracticePoor": [{"English": "Practice Poor", "Español": "Práctica deficiente"}],
    "condition.Migraine": [{"English": "Migraine", "Español": "Migraña"}],
    "condition.NightOwl": [{"English": "Night Owl", "Español": "Noctámbulo"}],
    "condition.DrySkin": [{"English": "Dry Skin", "Español": "Piel seca"}],
    "condition.SlowMetabolism": [{"English": "Slow Metabolism", "Español": "Metabolismo lento"}],
    "condition.Slacker": [{"English": "Slacker", "Español": "Holgazán"}],
    "condition.UnderTheWeather": [{"English": "Under the Weather", "Español": "Indispuesto"}],
    "condition.NotReady": [{"English": "Not Ready", "Español": "No preparado"}],
    "condition.LackOfFocus": [{"English": "Lack of Focus", "Español": "Falta de concentración"}],
    "condition.Overtired": [{"English": "Overtired", "Español": "Muy cansado"}],
    "condition.Charming": [{"English": "Charming", "Español": "Encantador"}],
    "condition.FastLearner": [{"English": "Fast Learner", "Español": "Aprendiz rápido"}],
    "condition.PracticePerfect_○": [{"English": "Practice Perfect", "Español": "Práctica perfecta"}],
    "condition.PracticePerfect_◎": [{"English": "Practice Perfect+", "Español": "Práctica perfecta+"}],
    "condition.HotTopic": [{"English": "Hot Topic", "Español": "Tema candente"}],
    "condition.ShiningBrightly": [{"English": "Shining Brightly", "Español": "Brillando intensamente"}],
    "condition.Sharpener": [{"English": "Sharpener", "Español": "En forma"}],
    "condition.NaturalTalent": [{"English": "Natural Talent", "Español": "Talento natural"}],

    "club.invite.accept": [{"English": "Accept", "Español": "Aceptar"}],
    "club.invite.decline": [{"English": "Decline", "Español": "Rechazar"}],
    "club.invite.invite_msg": [{"English": "You have been invited to **<0>**!", "Español": "¡Has sido invitado a **<0>**!"}],
    "club.msg.success": [{"English": "Successfully Responded.", "Español": "Respuesta enviada correctamente."}],

    "club.buttons.create": [{"English": "Create", "Español": "Crear"}],
    "club.buttons.view": [{"English": "View Club", "Español": "Ver club"}],
    "club.buttons.view_stats": [{"English": "View Statistics", "Español": "Ver estadísticas"}],
    "club.page.entrycount": [{"English": "<0> Entries", "Español": "<0> entradas"}],

    "club.buttons.join": [{"English": "Join Club", "Español": "Unirse al club"}],
    "club.buttons.leave": [{"English": "Leave Club", "Español": "Salir del club"}],
    "club.buttons.members": [{"English": "View Statistics", "Español": "Ver estadísticas"}],
    "club.page.titles":[
        {"English": "Info", "Español": "Información"},
        {"English": "Members", "Español": "Miembros"},
        {"English": "Statistics", "Español": "Estadísticas"}
    ],

    "club.create.title": [{"English": "Create a club", "Español": "Crear un club"}],
    "club.create.name": [{"English": "Club Name", "Español": "Nombre del club"}],
    "club.create.description": [{"English": "Club Description", "Español": "Descripción del club"}],
    "club.create.public": [{"English": "Public", "Español": "Público"}],
    "club.create.public_desc": [{"English": "Check this box to make it so your club is joinable without invites!",
                                 "Español": "Marca esta casilla para permitir que cualquiera se una sin invitación."}],
    "club.create.photo": [{"English": "Club Photo (512x512)", "Español": "Foto del club (512x512)"}],

    "global.buttons.next": [{"English": "Next", "Español": "Siguiente"}],

    "error.club.not_found": [{"English": "You don't have a club, Create one?",
                              "Español": "No tienes un club, ¿quieres crear uno?"}],

    "career.support.select": [{"English": "Select support cards to use.",
                               "Español": "Selecciona las cartas de apoyo que quieres usar."}],
    "career.support.none": [{"English": "Not Assigned.", "Español": "Sin asignar."}],

    "page.storage.upgrade": [
        {"English": "Upgrade"}
    ],
    "page.storage.show_umas": [
        {"English": "Your Umamusumes"}
    ],
    "page.storage.show_supports": [
        {"English": "Your Support Cards"}
    ]
}

class TranslationSection:
    def __init__(self, name: str, texts: list):
        self.name = name
        self.translations = list(texts)

    def translate(self, target: dict | str, index: int, *args, monospaced=False) -> str:
        lang = target["settings"]["lang"] if isinstance(target, dict) else target
        if index < 0 or index >= len(self.translations):
            return f"[index {index} out of range for section '{self.name}']"
        entry = self.translations[index]
        result = entry.get(lang)
        result = entry.get("English", "") if not result and result != False else result
        if not result and result != False:
            english_key = entry.get("English", "???")
            if english_key is None:
                return None
            return f"[no translation [{lang}] for {english_key!r}]"
        if args:
            result = _interpolate(result, args, lang)
        return result if not monospaced else typewriter(result)


def _interpolate(template: str, args: tuple, lang: str) -> str:
    """Replace <0>, <1>, ... positional placeholders with provided args."""
    def arg_replacer(match):
        idx_str = match.group(1)
        try:
            idx = int(idx_str)
            return str(args[idx]) if idx < len(args) else match.group(0)
        except ValueError:
            return match.group(0)

        
    return re.sub(r"\<(\w+)\>", arg_replacer, template)


def sectionify(parent: object, section_name: str, raw: list):
    parts = section_name.split(".")
    root = parent
    for i, part in enumerate(parts):
        is_leaf = i == len(parts) - 1
        if is_leaf:
            setattr(root, part, TranslationSection(part, raw))
        else:
            if not hasattr(root, part):
                setattr(root, part, _Namespace())
            root = getattr(root, part)


class _Namespace:
    pass


class Translator:
    def __init__(self, translations: dict):
        for section_name, value in translations.items():
            sectionify(self, section_name, value)

    def translate(self, identifier: str, target: dict | str, index: int, *args, monospaced=True) -> str:
        root = self
        for part in identifier.split("."):
            if not hasattr(root, part):
                return f"[MISSING SECTION: {identifier}]"
            root = getattr(root, part)
        if not isinstance(root, TranslationSection):
            return None
        return root.translate(target, index, *args, monospaced=monospaced)


translator = Translator(TRANSLATIONS)

def tr(identifier: str, index: int, prof_or_lang: dict | str = "English", *args, monospaced=False) -> str:
    return translator.translate(identifier, prof_or_lang, index, *args, monospaced=monospaced)
