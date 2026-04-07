from uicord import *
from .translations import translator, tr
from .pages import pagination_buttons, error, _create_back_button, _back_button
from .state import view_state
from src.data import *
import asyncio
import random

TRAINEES = 0
SUPPORTS = 1

def add_uma_to_prof(prof, uma):
    prof["inventory"]["umas"][uma.name] = prof["inventory"]["umas"].get(uma.name, [0, 0])
    prof["inventory"]["umas"][uma.name][0] += 1

def add_sc_to_prof(prof, sc):
    prof["inventory"]["supports"][sc.id] = prof["inventory"]["supports"].get(sc.id, [0, 0])
    prof["inventory"]["supports"][sc.id][0] += 1

async def roll(prof, check=True, sc=False):
    if check and prof["stats"]["carats"] < 150:
        return None

    pool = UMA_RARITIES if not sc else SC_RARITIES

    rarity = random.choices(
        ["r", "sr", "ssr"], weights=[75, 20, 5], k=1
    )[0]

    while not pool[rarity]:
        rarity=rarity[1:]
    return random.choice(list(pool[rarity].values()))


async def roll_num(prof, amount, fn, sc=False):
    if prof["stats"]["carats"] < amount * 150:
        return None, None

    prof["stats"]["carats"] -= amount * 150
    objs = [await roll(prof, False, sc=sc) for _ in range(amount)]

    for obj in objs:
        fn(prof, obj)

    emojis = [obj.rarity.lower() for obj in objs]
    return emojis, objs


async def view_one(ctx, prof, obj, uid, sc=False):
    if obj is None:
        return await ctx.response.edit_message(
            view=error(
                prof, uid, "insufficient_currency",
                back_view_factory=lambda: gacha(prof, uid, page=SUPPORTS if sc else TRAINEES)
            )
        )

    back = _back_button(
        prof["settings"]["lang"],
        lambda: gacha(prof, uid, page=SUPPORTS if sc else TRAINEES)
    )

    prof["stats"]["carats"] -= 150

    if sc:
        add_sc_to_prof(prof, obj)

        stat_emoji = view_state.bot.get_em(obj.stats[0].upper()) if obj.stats else ""
        title = f"{stat_emoji} **{obj.name}**"

        container = Container(
            Section(
                Text(title),
                accessory=Thumbnail(url=obj.get_image())
            ),
            ActionRow(back)
        )

    else:
        add_uma_to_prof(prof, obj)

        uma_display = f"{obj.name}{view_state.bot.get_uma(obj.name)}"

        container = Container(
            Text(tr(
                "page.gacha.result_one", 0, prof,
                uma_display, prof["stats"]["carats"]
            )),
            Separator(),
            ActionRow(back)
        )

    rollx1 = Button(
        tr("page.gacha.spin_labels", 0, prof),
        emoji=view_state.emojis["carat"],
        disabled=prof["stats"]["carats"] < 150,
    )

    @interaction(rollx1)
    async def _roll(i):
        new_obj = await roll(prof, sc=sc)
        await view_one(i, prof, new_obj, uid, sc=sc)

    container.items[-1].add(rollx1)

    await ctx.response.edit_message(
        view=View(container, owner=uid)
    )


def format_emojis(prof, emojis, names=[]):
    if len(emojis) != 10:
        raise ValueError("Requires exactly 10 emojis")

    e = list(map(str, emojis))

    if prof["settings"].setdefault("triangle_gacha", True):
        rows = [
            f"",
            f"                {e[0]}                ",
            f"           {e[1]}   {e[2]}           ",
            f"      {e[3]}   {e[4]}   {e[5]}      ",
            f" {e[6]}   {e[7]}   {e[8]}   {e[9]}",
        ]
    else:
        print(e, names)
        rows = [
            "-# " + a + b for a, b in zip(e, names)
        ]

    return "\n".join(rows)


async def view_multi(ctx, prof, emojis, objs, uid, page, sc=False):
    if not (emojis or objs):
        return await ctx.response.edit_message(
            view=error(
                prof, uid, "insufficient_currency",
                back_view_factory=lambda: gacha(prof, uid, page=page)
            )
        )

    rollx10 = Button(
        tr("page.gacha.spin_labels", 1, prof),
        emoji=view_state.emojis["carat"],
        disabled=prof["stats"]["carats"] < 1500,
    )

    @interaction(rollx10)
    async def _roll10(i):
        new_emojis, new_objs = await roll_num(
            prof, 10,
            add_sc_to_prof if sc else add_uma_to_prof,
            sc=sc
        )
        await view_multi(i, prof, new_emojis, new_objs, uid, page, sc=sc)

    def decrease_rarity(n):
        if not n.startswith("r"):
            return n[1:]
        return n

    if not prof["settings"].setdefault("skip_gacha", False):
        fakes = []
        fake_index = []

        for i, em in enumerate(emojis):
            display_em = em
            if random.random() <= 0.15:
                if not em.startswith("r"):
                    fake_index.append(i)
                display_em = decrease_rarity(em)
            fakes.append(display_em)

        emojs = [view_state.emojis["shake_" + a] for a in fakes]
        names = ["???"] * 10

        rolling_text = tr(
            "page.gacha.result_multi_rolling", 0, prof,
            len(emojis), format_emojis(prof, emojs, names)
        )

        await ctx.response.edit_message(
            view=View(Container(Text(rolling_text)), owner=uid)
        )

        for i in range(len(emojis) + 1):
            await asyncio.sleep(1 if i - 1 in fake_index else 0.35)

            if i != 0:
                names[i - 1] = objs[i - 1].name if sc else objs[i - 1].name

            shown = (
                [
                    objs[j].get_emoji(view_state.bot) if sc
                    else view_state.bot.get_uma(objs[j].name)
                    for j in range(i)
                ] + list(emojs[i:])
            )

            rolling_text = tr(
                "page.gacha.result_multi_rolling", 0, prof,
                len(emojis), format_emojis(prof, shown, names)
            )

            await ctx.edit_original_response(
                view=View(Container(Text(rolling_text)), owner=uid)
            )

    if sc:
        shown = [obj.get_emoji(view_state.bot) for obj in objs]
        names = [obj.name for obj in objs]
    else:
        shown = [view_state.bot.get_uma(objs[j].name) for j in range(10)]
        names = list(map(lambda v: v.name, objs))

    done_text = tr(
        "page.gacha.result_multi_done", 0, prof,
        format_emojis(prof, shown, names)
    )

    back = _back_button(
        prof["settings"]["lang"],
        lambda: gacha(prof, uid, page=page)
    )

    r = ctx.edit_original_response if not prof["settings"]["skip_gacha"] else ctx.response.edit_message

    await r(
        view=View(
            Container(
                Text(done_text),
                ActionRow(back, rollx10),
            ),
            owner=uid,
        )
    )


def gacha(prof, uid, page=0, **kwargs):
    is_sc = page == SUPPORTS

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
        obj = await roll(prof, sc=is_sc)
        await view_one(i, prof, obj, uid, sc=is_sc)

    @interaction(rollx10)
    async def _roll10(i):
        new_emojis, new_objs = await roll_num(
            prof, 10,
            add_sc_to_prof if is_sc else add_uma_to_prof,
            sc=is_sc
        )
        await view_multi(i, prof, new_emojis, new_objs, uid, page, sc=is_sc)

    parent_factory = lambda page: gacha(prof, uid, page=page)
    back_factory = lambda: view_state.views.home(prof, uid)

    nav_buttons = pagination_buttons(
        parent_factory=parent_factory,
        max_pages=1,
        lang=prof["settings"]["lang"],
        current_page=page,
        back_factory=back_factory
    )

    return View(
        Container(
            page_title,
            Text(tr(
                "page.gacha.carat_label", 0, prof,
                prof["stats"]["carats"], view_state.emojis["carat"]
            )),
            ActionRow(rollx1, rollx10),
            *nav_buttons,
        ),
        owner=uid,
    )

view_state.views.gacha = gacha
