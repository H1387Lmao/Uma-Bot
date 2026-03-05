from uicord import *
from .translations import *
from .pages import page_buttons
import discord as dsc

def prof(data, uid, ulang="English"):
    TR_TITLE  = tr(ulang, 5)
    TR_BUTTON = tr(ulang, 6)
    options = []
    for lang in SUPPORTED_LANGS:
        options.append(
            dsc.SelectOption(
                label=lang, default=lang==ulang
            )
        )
    
    lang_select = Choices(
        options=options
    )
    @interaction(lang_select)
    async def _switch(ctx):
        await ctx.response.edit_message(
            view=prof(
                data, uid, lang_select.picked
            )
        )
    START_BTN = Button(TR_BUTTON)
    @interaction(START_BTN)
    async def _ok(ctx):
        profile = data.setdefault(str(ctx.user.id),
        {
            "lang": ulang,
            "name": ctx.user.display_name,
            "items": {
                
            },
            "umas": {
                
            },
            "badges": [],
            "old_careers": [],
            "career": None,
            "club": None,
            "stats": {
                "fans": 0,
                "exp": 0,
                "tp": 100
            },
            "inboxes_read": []
        })
        print(f"Created Profile for {ctx.user}")
        await ctx.response.edit_message(
            view=home(profile, uid)
        )
    return View(
        Container(
            Text(f"## {TR_TITLE}"),
            ActionRow(lang_select),
            ActionRow(
                START_BTN
            )
        )
    )

def home(prof, uid, page=2, **kwargs):
    page_title = Text(f"## **{tr(prof["lang"], page)}**!\n-# Under construction")
    return View(
        Container(
            page_title,
            *page_buttons(home, MAXPAGES=4)
        ),
        owner=uid
    )
