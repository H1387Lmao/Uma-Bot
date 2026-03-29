# home.py
from uicord import *
from .translations import translator, tr, SUPPORTED_LANGS, TRANSLATIONS
from .pages import pagination_buttons
from .gacha import gacha
from .storage import storage
from .career import career_select, career
from .state import view_state
import discord as dsc
import signal, sys, atexit
import asyncio

SEC_SETTINGS  = "settings.lang"
SEC_TITLES    = "page.titles"
SEC_MAIN_BTNS = "page.main.btns"
SEC_CLUB_BTNS = "page.club.btns"

TITLE_HOME  = 0
TITLE_CLUB  = 1
TITLE_SETTINGS = 2

async def create_loading(ctx, function, *args, respond=False):
    em = "<a:loading:1482569743679361225>"
    
    res = ctx.response.edit_message if not respond else ctx.reply

    if view_state.emojis:
        return await res(
            view=function(*args)
        )

    msg = await res(
        view=View(
            Container(
                Section(
                    Text(f"### **{tr("ui.loading", 0, prof, em)}**\n-# {tr("ui.loading", 1, prof)}"),
                    accessory=Thumbnail(
                        url="https://raw.githubusercontent.com/H1387Lmao/H1387Lmao/refs/heads/main/resources/umabot-logo.png"
                    )
                )
            )
        )
    )
    while not view_state.emojis:
        await asyncio.sleep(1)

    res = ctx.edit_original_response if not respond else msg.edit
    try:
        await res(
            view=function(*args)
        )
    except:
        return

async def prof(ctx, data, uid: int, ulang="English", respond=True):
    if str(uid) in data:
        return await create_loading(ctx, home, data[str(uid)], uid, respond=respond)
    tr_title  = tr("settings.lang", 0, ulang)
    tr_button = tr("settings.lang", 1, ulang)

    options = [
        dsc.SelectOption(label=lang, default=lang == ulang)
        for lang in SUPPORTED_LANGS
    ]

    lang_select = Choices(options=options)

    @interaction(lang_select)
    async def _switch(ctx):
        await prof(ctx, data, uid, lang_select.picked, False)

    start_btn = Button(tr_button)

    @interaction(start_btn)
    async def _ok(ctx):
        prof = data.setdefault(str(ctx.user.id), {
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
            "settings": {
                "lang":         ulang,
            }
        })

        options = [
            {
                "name": tr("page.settings.options", i, ulang),
                "id": tr("page.settings.options", i, "_id"),
                "default": tr("page.settings.options", i, "_default"),
                "value": tr("page.settings.options", i, "_values"),
                "type": tr("page.settings.options", i, "_type")

            } for i in range(len(TRANSLATIONS["page.settings.options"]))
        ]

        for element in options:
            name     = element["name"]
            id       = element["id"]
            values   = element["value"]
            default  = prof["settings"].setdefault(
                id, element["default"]
            )
        print(f"Created profile for {ctx.user}")
        await create_loading(
            ctx, home, prof, uid
        )
    res = ctx.respond if respond else ctx.response.edit_message
    await res(
        view=View(
            Container(
                Text(f"## {tr_title}"),
                ActionRow(lang_select),
                ActionRow(start_btn),
            )
        )
    )

def credits_page(prof, uid):
    bot = view_state.bot
    prog_id = 735679718506102881
    eng_id = 1252175358741057586
    esp_id = 696002196205994024

    prog_user = bot.get_user(prog_id)
    eng_user = bot.get_user(eng_id)
    esp_user = bot.get_user(esp_id)

    prog_name = prog_user.display_name if prog_user else "Unknown"
    eng_name = eng_user.display_name if eng_user else "Unknown"
    esp_name = esp_user.display_name if esp_user else "Unknown"

    title = tr("page.credits", 0, prof, monospaced=True)
    assets = tr("page.credits", 1, prof)
    sprites = tr("page.credits", 2, prof)
    dev = tr("page.credits", 3, prof)
    prog = tr("page.credits", 4, prof)
    comm = tr("page.credits", 5, prof)
    eng = tr("page.credits", 6, prof)
    esp = tr("page.credits", 7, prof)

    text = (
        f"# **{title}**{bot.get_em("ui_profile")}\n"

        f"## 🖼️ {assets}\n"
        f"-# © CyGames — {sprites}\n\n"

        f"## 🖱️ {dev}\n"
        f"-# ***{prog_name}***\n**({prog})**\n\n"

        f"## 🌐 {comm}\n"
        f"-# ***{eng_name}***\n**({eng})**\n"
        f"-# ***{esp_name}***\n**({esp})**"
    )

    return Text(text)

def home(prof, uid, page=0):
    lang = prof["settings"]["lang"]

    title = f"{tr('page.titles', page, lang)}"
    emoji = tr('page.titles', page, '_emoji')

    bot = view_state.bot

    page_title = Text(f"## **{title}**")
    
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
    options = [
        {
            "name": tr("page.settings.options", i, lang),
            "id": tr("page.settings.options", i, "_id"),
            "default": tr("page.settings.options", i, "_default"),
            "value": tr("page.settings.options", i, "_values"),
            "type": tr("page.settings.options", i, "_type")

        } for i in range(len(TRANSLATIONS["page.settings.options"]))
    ]
    elements = []
    buttons = []
    
    match page:
        case 0:
            buttons = [Button(d['label'], emoji=bot.get_em(d['emoji'], "❔")) for d in main_btns]

            @interaction(buttons[2])
            async def _scout(ctx):
                await ctx.response.edit_message(
                    view=gacha(prof, uid)
                )

            @interaction(buttons[0])
            async def _storage(ctx):
                await ctx.response.edit_message(
                    view=storage(home, prof, uid)
                )
            @interaction(buttons[1])
            async def _career(ctx):
                await ctx.response.edit_message(
                    view=career_select(prof, uid)
                )
        case 1:
            buttons = [Button(d['label'], emoji=bot.get_em(d['emoji'], "❔")) for d in club_btns]
        case 2:
            current_row=[]
            for element in options:
                name     = element["name"]
                id       = element["id"]
                values   = element["value"]
                default  = prof["settings"].setdefault(
                    id, element["default"]
                )
                if len(current_row)==5:
                    elements.append(ActionRow(
                        *current_row
                    ))
                match element["type"]:
                    case "toggle":
                        tg = Toggle(
                            name, default=default,
                            custom_off=view_state.emojis["toggle_off"],
                            custom_on=view_state.emojis["toggle_on"]
                        )
                        @interaction(tg)
                        async def _int(ctx, id=id, tg=tg, name=name):
                            prof["settings"][id] = tg.active
                            await ctx.response.edit_message(
                                view=home(prof, uid, page)
                            )
                        current_row.append(
                            tg
                        )
                    case "choices":
                        choices_options = [
                            dsc.SelectOption(label=value, default=default==value)
                            for value in values
                        ]
                        choices = Choices(
                            options=choices_options
                        )
                        @interaction(choices)
                        async def _int(ctx,
                            id=id,
                            choices=choices
                        ):
                            prof["settings"][id]=choices.picked
                            await ctx.response.edit_message(
                                view=home(prof, uid, page)
                            )
                        elements.extend([
                            Text(f"## **{name}**"),
                            ActionRow(choices)
                        ])
            if current_row:
                elements.append(ActionRow(
                    *current_row
                ))
        case 3:
            page_title=credits_page(prof, uid)

    if buttons:
        elements.append(ActionRow(*buttons))

    parent_factory = lambda page: home(prof, uid, page=page)
    nav_buttons = pagination_buttons(
        parent_factory=parent_factory,
        max_pages=3,
        lang=lang,
        current_page=page,
        loop=True
    )

    thumb_url = "https://raw.githubusercontent.com/H1387Lmao/H1387Lmao/refs/heads/main/resources/umabot-logo.png" if page%3==0 else bot.get_em(emoji).url
    return View(
        Container(
            Section(
                page_title,
                accessory=Thumbnail(
                    url=thumb_url
                )
            ),
            *elements,
            *nav_buttons,
        ),
        owner=uid,
    )

view_state.views.home = home
