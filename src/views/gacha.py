# gacha.py
from uicord import *
from .translations import translator, tr
from .pages import pagination_buttons, error
from .state import view_state
from src.data import *
import asyncio
import random

TRAINEES = 0
SUPPORTS = 1

def _back_button(lang, view_factory):
    emoji = view_state.bot.get_em("ui_back")
    btn = Button(emoji=emoji, text=tr("ui.label", 0, lang))
    @interaction(btn)
    async def _back(ctx):
        await ctx.response.edit_message(view=view_factory())
    return btn

def add_uma_to_prof(prof, uma):
    prof["inventory"]["umas"][uma.name] = prof["inventory"]["umas"].get(uma.name, [0, 0])
    prof["inventory"]["umas"][uma.name][0] += 1

async def roll():
    RARITY = random.choices(
        ["r", "sr", "ssr"], weights=[75, 20, 5], k=1)[0]
    return random.choice(list(UMA_RARITIES[RARITY].values()))

async def roll_num(prof, amount):
    if prof["stats"]["carats"] < amount * 150:
        return None, None
    prof["stats"]["carats"] -= amount * 150
    umas = [await roll() for _ in range(amount)]
    for uma in umas:
        add_uma_to_prof(prof, uma)
    umasemojis = [uma.name for uma in umas]
    emojis = [uma.rarity for uma in umas]
    return emojis, umasemojis

def view_one(prof, uma, uid):
    back = _back_button(prof["lang"], lambda: gacha(prof, uid))

    rollx1 = Button(
        tr("page.gacha.spin_labels", 0, prof),
        emoji=view_state.emojis["carat"],
        disabled=prof["stats"]["carats"] < 150,
    )

    @interaction(rollx1)
    async def _roll(i):
        if prof["stats"]["carats"] < 150:
            return
        prof["stats"]["carats"] -= 150
        new_uma = await roll()
        add_uma_to_prof(prof, new_uma)
        uma_display = f"{new_uma.name}{view_state.bot.get_uma(new_uma.name)}"
        await i.response.edit_message(
            view=view_one(prof, new_uma, uid)
        )

    uma_display = f"{uma.name}{view_state.bot.get_uma(uma.name)}"
    return View(
        Container(
            Text(tr("page.gacha.result_one", 0, prof,
                    uma_display, prof["stats"]["carats"])),
            Separator(),
            ActionRow(back, rollx1),
        ),
        owner=uid,
    )

async def view_multi(ctx, prof, emojis, umas, uid, page):
    if not (emojis or umas):
        return error(prof, uid, "insufficient_currency",
                     back_view_factory=lambda: gacha(prof, uid))

    rollx10 = Button(
        tr("page.gacha.spin_labels", 1, prof),
        emoji=view_state.emojis["carat"],
        disabled=prof["stats"]["carats"] < 1500,
    )

    @interaction(rollx10)
    async def _roll10(i):
        new_emojis, new_umas = await roll_num(prof, 10)
        await i.edit_original_response(
            view=await view_multi(i, prof, new_emojis, new_umas, uid, page)
        )

    # Build fake/reveal animation list
    def decrease_rarity(n):
        if not n.startswith("r"):
            return n[1:]
        return n

    fakes = []
    fake_index = []
    for i, em in enumerate(emojis):
        display_em = em
        if random.random() <= 0.15:
            if not em.startswith("r"):
                fake_index.append(i)
            display_em = decrease_rarity(em)
        fakes.append(display_em)

    emojs = [view_state.emojis[a + "pull"] for a in fakes]

    rolling_text = tr("page.gacha.result_multi_rolling", 0, prof,
                      len(emojis), " ".join(map(str, emojs)))
    await ctx.response.edit_message(
        view=View(
            Container(Text(rolling_text)),
            owner=uid,
        )
    )

    shown = list(emojs)
    for i in range(len(emojis) + 1):
        await asyncio.sleep(0.35)
        if i in fake_index:
            shown[i] = view_state.emojis["s" + emojs[i].name]
        shown = (
            [view_state.bot.get_uma(umas[j]) for j in range(i)]
            + list(emojs[i:])
        )
        rolling_text = tr("page.gacha.result_multi_rolling", 0, prof,
                          len(emojis), " ".join(map(str, shown)))
        await ctx.edit_original_response(
            view=View(Container(Text(rolling_text)), owner=uid)
        )
        if i in fake_index:
            await asyncio.sleep(1)

    done_text = tr("page.gacha.result_multi_done", 0, prof,
                   " ".join(map(str, shown)))
    back = _back_button(prof["lang"], lambda: gacha(prof, uid))
    return View(
        Container(
            Text(done_text),
            ActionRow(back, rollx10),
        ),
        owner=uid,
    )

def gacha(prof, uid, page=0, **kwargs):
    page_title = Text(f"## **{tr('page.gacha.titles', page, prof)}**")

    rollx1 = Button(
        emoji=view_state.emojis["carat"],
        text=tr("page.gacha.spin_labels", 0, prof),
    )
    rollx10 = Button(
        emoji=view_state.emojis["carat"],
        text=tr("page.gacha.spin_labels", 1, prof),
    )

    @interaction(rollx1)
    async def _roll(i):
        if prof["stats"]["carats"] < 150:
            return
        prof["stats"]["carats"] -= 150
        uma = await roll()
        add_uma_to_prof(prof, uma)
        await i.response.edit_message(view=view_one(prof, uma, uid))

    @interaction(rollx10)
    async def _roll10(i):
        new_emojis, new_umas = await roll_num(prof, 10)
        await i.edit_original_response(
            view=await view_multi(i, prof, new_emojis, new_umas, uid, page)
        )

    parent_factory = lambda page: gacha(prof, uid, page=page)
    back_factory = lambda: view_state.views.home(prof, uid)
    nav_buttons = pagination_buttons(
        parent_factory=parent_factory,
        max_pages=1,
        lang=prof["lang"],
        current_page=page,
        back_factory=back_factory
    )

    return View(
        Container(
            page_title,
            ActionRow(rollx1, rollx10),
            *nav_buttons,
        ),
        owner=uid,
    )

view_state.views.gacha = gacha
