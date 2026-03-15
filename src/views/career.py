from ..career import *
from uicord import *
from .translations import translator, tr, SUPPORTED_LANGS, TRANSLATIONS
from .pages import pagination_buttons, error, _back_button
from .state import view_state

MOOD_LEVELS = ['awful', 'bad', 'normal', 'good', 'great']

def _lang(prof): return prof["settings"]["lang"]
def _uma_em(name): return view_state.bot.get_em(name.replace(" ", "_").lower()) or "🐴"
def _mood_em(c): return view_state.bot.get_em(f"mood_{MOOD_LEVELS[c.mood].lower()}")
def _stat_em(stat): return view_state.bot.get_em(stat.upper()) or ":bulb:"

def _get_umas(prof) -> dict[str, list]:
    return prof.get("inventory", {}).get("umas", {})
 

def career_select(prof, uid, page=0):
    umas = _get_umas(prof)
    if not umas:
        return error(prof, uid, "career.no_uma", back_view_factory=lambda: view_state.views.home(prof, uid))
    names = list(umas.keys())
    max_p = max(0, (len(names) - 1) // 4)
    page_names = names[page * 4: page * 4 + 4]
    btns = []
    for name in page_names:
        btn = Button(name, emoji=_uma_em(name), color=Colors.Grey)
        @interaction(btn)
        async def _pick(i, n=name):
            await i.response.edit_message(view=career_select_confirm(prof, uid, n))
        btns.append(btn)
    pagination = pagination_buttons(lambda p: career_select(prof, uid, p), max_p, _lang(prof), page, back_factory=lambda: view_state.views.home(prof, uid))
    return View(Container(Text(tr("career.select.title", 0, prof)), ActionRow(*btns), *pagination), owner=uid)
 
def career_select_confirm(prof, uid, name):
    count, level = _get_umas(prof).get(name, [0, 0])
    start = Button(tr("career.select.start", 0, prof), emoji="🏁", color=Colors.Green)
    @interaction(start)
    async def _start(ctx):
        prof["career"] = Career.create_new(name, str(uid), [])
        await ctx.response.edit_message(view=career(prof, uid))
    return View(
        Container(
            Section(
                Text(f"## {_uma_em(name)} {name}"),
                accessory=Thumbnail(url=getattr(_uma_em(name), "url", ""))
            ),
            ActionRow(start, _back_button(_lang(prof), lambda: career_select(prof, uid))),
        ),
        owner=uid
    )

def training(prof, uid, confirm_stat=None):
    career = prof['career']
    em = _uma_em(career.name)
    training_header = tr("training.header", 0, prof, em, career.name, career.energy)
    mood = _mood_em(career)

    stats_displayed = []
    training_btns = []

    preview = career.train(confirm_stat, True) if confirm_stat else {}
    
    for stat, values in zip(stat_names, career.stats):
        st = tr(f'stats.{stat}', 0, prof)
        if confirm_stat and stat in preview:
            stats_displayed.append((stat, st, (values, preview[stat])))
        else:
            stats_displayed.append((stat, st, values))
    
        btn = Button(tr('training.train_button', 0, prof, st), emoji=_stat_em(stat))
        training_btns.append(btn)
    
        @interaction(btn)
        async def _train(i, stat=stat):
            if confirm_stat == stat:
                career.train(stat)
                return await i.response.edit_message(view=training(prof, uid, None))
            else:
                return await i.response.edit_message(view=training(prof, uid, stat))
    
    stats_displayed.append(('skill_points', tr('training.skill_pts_label', 0, prof), career.skill_points))
    
    longest_length = max(len(stat) for _, stat, _ in stats_displayed)
    
    cols = 3
    rows = []
    
    for i in range(0, len(stats_displayed), cols):
        chunk = stats_displayed[i:i+cols]
    
        label_row = []
        value_row = []
    
        for actual, stat, value in chunk:
            label = f"{_stat_em(actual)} {stat}"
            label_row.append(label.ljust(longest_length + 6))
    
            if isinstance(value, tuple):
                base, bonus = value
                val = f"{base} **(+{bonus})**"
            else:
                val = str(value)
    
            value_row.append(val.ljust(longest_length + 6))
    
        rows.append(" ".join(label_row))
        rows.append(" ".join(value_row))
        rows.append("")  # spacing row
    
    stat_line = "\n".join(rows)

    return View(
        Container(
            Section(
                Text(f"## **{training_header}**"),
                Text(stat_line),
                accessory=Thumbnail(
                    url=mood.url
                )
            )
        ),
        Container(
            ActionRow(*training_btns)
        )
    )

def career(prof, uid):
    career = prof['career']
    if not career:
        return career_select(prof, uid)
    em = _uma_em(career.name)
    training_header = tr("training.header", 0, prof, '','', career.energy)

    month = tr('career.months', career.month, prof)
    early = "early" if career.half == 0 else "late"
    half = tr(f'career.half.{early}', 0, prof)
    mood = _mood_em(career)

    train = Button(tr('career.btn.train', 0, prof))

    @interaction(train)
    async def _train(i):
        await i.response.edit_message(view=training(prof, uid))
    
    return View(Container(
        Section(
            Text(
                tr("career.header", 0, prof, em, career.name, training_header, career.year, month, half)
            ),
            accessory=Thumbnail(
                url=mood.url
            )
        ),
        ActionRow(
            train
        )
       
    ), owner=uid)
