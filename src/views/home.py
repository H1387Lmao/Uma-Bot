# main.py
from uicord import *
from .translations import translator, tr, SUPPORTED_LANGS, TRANSLATIONS
from .pages import page_buttons
from .gacha import gacha
from .state import view_state
import discord as dsc
import signal, sys, atexit

# Section identifiers
SEC_SETTINGS  = "settings.lang"
SEC_TITLES    = "page.titles"
SEC_MAIN_BTNS = "page.main.btns"
SEC_CLUB_BTNS = "page.club.btns"

# Index offsets within page.titles
TITLE_HOME  = 0   # "Welcome Back Trainer!"
TITLE_CLUB  = 1   # "Club"
TITLE_SETTINGS = 2  # "Settings"


def prof(data, uid, ulang="English"):
    tr_title  = tr("settings.lang", 0, ulang)
    tr_button = tr("settings.lang", 1, ulang)

    options = [
        dsc.SelectOption(label=lang, default=lang == ulang)
        for lang in SUPPORTED_LANGS
    ]

    lang_select = Choices(options=options)

    @interaction(lang_select)
    async def _switch(ctx):
        await ctx.response.edit_message(
            view=prof(data, uid, lang_select.picked)
        )

    start_btn = Button(tr_button)

    @interaction(start_btn)
    async def _ok(ctx):
        profile = data.setdefault(str(ctx.user.id), {
            "lang":         ulang,
            "name":         ctx.user.display_name,
            "inventory":    {
                "umas":     {},
                "items":    {},
                "supports": []
            },
            "badges":       [],
            "old_careers":  [],
            "career":       None,
            "club":         None,
            "stats":        {"fans": 0, "exp": 0, "tp": 100, "carats": 1500},
            "inboxes_read": [],
        })
        print(f"Created profile for {ctx.user}")
        await ctx.response.edit_message(
            view=home(profile, uid)
        )

    return View(
        Container(
            Text(f"## {tr_title}"),
            ActionRow(lang_select),
            ActionRow(start_btn),
        )
    )


def home(prof, uid, page=0):
    lang = prof["lang"]

    page_title = Text(f"## **{tr("page.titles", page, lang)}**")
    
    main_btns = [
        {
            "label": tr("page.main.btns", i, lang),
            "emoji": tr("page.main.btns", i, "_emoji")
        } for i in range(len(TRANSLATIONS["page.main.btns"]))
    ]
    club_btns = [
        {
            "label": tr("page.club.btns", i, lang),
            "emoji": tr("page.club.btns", i, "_emoji")
        } for i in range(len(TRANSLATIONS["page.club.btns"]))
    ]
    bot = view_state.bot
    match page:
        case 0:
            buttons = [Button(d['label'], emoji=bot.get_em(d['emoji'], "❔")) for d in main_btns]

            @interaction(buttons[2])
            async def _scout(ctx):
                await ctx.response.edit_message(
                    view=gacha(home, prof, uid)
                )
        case 1:
            buttons = [Button(d['label'], emoji=bot.get_em(d['emoji'], "❔")) for d in club_btns]
        case _:
            btn_info = []
    
    elements = []
    if buttons:
        elements.append(ActionRow(*buttons))

    return View(
        Container(
            page_title,
            *elements,
            *page_buttons(
                home,
                max_pages=2,
            ),
        ),
        owner=uid,
    )
