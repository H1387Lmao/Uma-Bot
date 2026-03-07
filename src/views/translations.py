import re

SUPPORTED_LANGS = ["English", "Español"]
TRANSLATIONS = {
    "settings.lang": [
        {"English": "Choose a language",  "Español": "Elige un idioma"},
        {"English": "Continue",           "Español": "Continuar"},
    ],
    "ui.label": [
        {"English": "Back", "Español": "Atrás"},
    ],
    "page.titles": [
        {"English": "Welcome Back Trainer!", "Español": "¡Bienvenido entrenador!"},
        {"English": "Club",                  "Español": "Clubes"},
        {"English": "Settings",              "Español": "Configuración"},
    ],
    "page.main.btns": [
        {"English": "Storage",      "Español": "Almacenaje"},
        {"English": "Career",       "Español": "Carrera"},
        {"English": "Scouting",     "Español": "Gacha",
            "_emoji": "ui_scouting"
        },
        {"English": "Daily Races",  "Español": "Carreras Diarias"},
    ],
    "page.club.btns": [
        {"English": "Your Club",    "Español": "Tu Club"},
        {"English": "Find Clubs",   "Español": "Buscar Club"},
    ],
    "page.gacha.titles": [
        {"English": "🏇 Pretty Derby Scout",    "Español": "🏇 Scout Pretty Derby"},
        {"English": "🃏 Support Card Scout",    "Español": "🃏 Scout de Cartas de Apoyo"},
    ],
    "page.gacha.spin_labels": [
        {"English": "150 | 1 Roll",     "Español": "150 | 1 Tirada"},
        {"English": "1500 | 10 Rolls",  "Español": "1500 | 10 Tiradas"},
    ],
    "page.gacha.result_one": [
        # {0} = uma name+emoji, {1} = carats remaining
        {"English": "🎉 You obtained **{0}**\n-# You have {1} carats left.",
         "Español": "🎉 ¡Obtuviste **{0}**!\n-# Te quedan {1} carats."},
    ],
    "page.gacha.result_multi_rolling": [
        # {0} = roll count, {1} = emoji string
        {"English": "-# Rolling {0} times!\n**{1}**",
         "Español": "-# ¡Tirando {0} veces!\n**{1}**"},
    ],
    "page.gacha.result_multi_done": [
        # {0} = emoji string
        {"English": "-# Finished rolling!\n**{0}**",
         "Español": "-# ¡Terminaste de tirar!\n**{0}**"},
    ],
    "cmd.start": [
        {"English": "start", "Español": "iniciar"},
    ],
    "cmd.music": [
        {"English": "music", "Español": "música"},
    ],
    "errors.insufficient_currency": [
        {"English": "Insufficient!",                    "Español": "¡Insuficiente!"},
        {"English": "You don't have enough carats!",    "Español": "¡No tienes suficientes carats!"},
    ],
}


class TranslationSection:
    def __init__(self, name: str, texts: list):
        self.name = name
        self.translations = list(texts)

    def translate(self, target: dict | str, index: int, *args) -> str:
        lang = target["lang"] if isinstance(target, dict) else target
        if index < 0 or index >= len(self.translations):
            return f"[index {index} out of range for section '{self.name}']"
        entry = self.translations[index]
        result = entry.get(lang) or entry.get("English", "")
        if not result:
            english_key = entry.get("English", "???")
            return f"[no translation [{lang}] for {english_key!r}]"
        # f-string-style interpolation: replace {0}, {1}, ... with positional args
        # and translate any nested tr("key") calls embedded as {key:index} if needed
        if args:
            result = _interpolate(result, args)
        return result


def _interpolate(template: str, args: tuple) -> str:
    """Replace {0}, {1}, ... positional placeholders with provided args."""
    def replacer(match):
        idx_str = match.group(1)
        try:
            idx = int(idx_str)
            return str(args[idx]) if idx < len(args) else match.group(0)
        except ValueError:
            return match.group(0)  # leave non-integer placeholders untouched
    return re.sub(r"\{(\w+)\}", replacer, template)


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

    def translate(self, identifier: str, target: dict | str, index: int, *args) -> str:
        root = self
        for part in identifier.split("."):
            if not hasattr(root, part):
                return f"[MISSING SECTION: {identifier}]"
            root = getattr(root, part)
        if not isinstance(root, TranslationSection):
            return f"[{identifier} is not a TranslationSection]"
        return root.translate(target, index, *args)


translator = Translator(TRANSLATIONS)

def tr(identifier: str, index: int, prof_or_lang: dict | str = "English", *args) -> str:
    return translator.translate(identifier, prof_or_lang, index, *args)
