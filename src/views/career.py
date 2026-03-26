from ..career import *
from uicord import *
from .translations import translator, tr, SUPPORTED_LANGS, TRANSLATIONS, typewriter
from .pages import pagination_buttons, error, _back_button
from .state import view_state
from ..data import grade_map, grade_stat, SCHEDULES
import random

MOOD_LEVELS = ['awful', 'bad', 'normal', 'good', 'great']

def _lang(prof): return prof["settings"]["lang"]
def _uma_em(name): return view_state.bot.get_em(name.replace(" ", "_").lower()) or "🐴"
def _mood_em(c): return view_state.bot.get_em(f"mood_{MOOD_LEVELS[c.mood].lower()}")
def _stat_em(stat): return view_state.bot.get_em(stat.upper()) or ":bulb:"

def _get_umas(prof) -> dict[str, list]:
    return prof.get("inventory", {}).get("umas", {})

def get_goal_header(prof, uid):
    career = prof['career']
    goal_info = career.get_needed_goal()

    args = []
    
    if isinstance(goal_info, FanGoal):
       tr_identif = "goal.fans"
    elif isinstance(goal_info, RaceGoal):
        if goal_info.race_data.name=="Junior Make Debut":
            tr_identif = "goal.debut"
        else:
            match goal_info.placement:
                case 1:
                    tr_identif = "goal.req.win"
                case 3:
                    tr_identif = "goal.req.top3"
                case 5:
                    tr_identif = "goal.req.top5"
                case 99:
                    tr_identif = "goal.req.participate"
        args.append(goal_info.race_data.name)
    elif goal_info is None:
        return tr("career.goal.completed", 0, prof)
    title = tr(tr_identif, 0, prof, *args)
    needed_turn = goal_info.deadline-career.turn
    index = 0 if needed_turn != 1 else 1
    turn = tr("career.turns", index, prof, needed_turn) if needed_turn>0 else ""
    return tr("career.goal.header", 0, prof, title, turn)


def view_race_info(prof, uid, race, page):
    print(race)
    return View(
        Container(
            Text(f"# {race.name}"),
            ActionRow(
                _back_button(prof, lambda: race_schedule(prof, uid, page))
            )
        )
    )

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
    data_uma = UMAS[name]
    start = Button(tr("career.select.start", 0, prof), emoji="🏁", color=Colors.Green)

    @interaction(start)
    async def _start(ctx):
        prof["career"] = Career.create_new(name, str(uid), [])
        await ctx.response.edit_message(view=career(prof, uid))
    
    cols = 3
    rows = []

    aptitudes = []

    for apt in ['turf','dirt','front', 'mile', 'medium', 'long']:
        grade = grade_map[getattr(data_uma, f"get_{apt}_apt")()]
        aptitudes.append((apt.title(), grade))

    longest_length = max(len(stat) for stat, _ in aptitudes)
    
    for i in range(0, len(aptitudes), cols):
        chunk = aptitudes[i:i+cols]
    
        label_row = []
    
        for actual, value in chunk:
            _label = typewriter(' '+actual)
            label = f"{view_state.bot.get_em('rank'+value)}{_label:{"\u2007"}<{longest_length + 2}}"
            label_row.append(label)

        rows.append(" ".join(label_row))
        rows.append("")
    
    aptitude_lines = "\n".join(rows)
    return View(
        Container(
            Section(
                Text(f"## {_uma_em(name)} {name}\n{aptitude_lines}"),
                accessory=Thumbnail(url=getattr(_uma_em(name), "url", ""))
            ),
            ActionRow(start, _back_button(_lang(prof), lambda: career_select(prof, uid))),
        ),
        owner=uid
    )

def get_statline(stats_displayed, compact=False):
    longest_length = max(len(stat) for _, stat, _ in stats_displayed)
    
    cols = 3 if not compact else 2
    rows = []
    
    for i in range(0, len(stats_displayed), cols):
        chunk = stats_displayed[i:i+cols]
    
        label_row = []
        value_row = []
    
        for actual, stat, value in chunk:
            if isinstance(value, tuple):
                base, bonus = value
                val = typewriter(f"{base} **(+{bonus})**")
            else:
                base = value
                val = typewriter(str(value))

            em = str(_stat_em(actual))
            label = em+typewriter(stat.ljust(longest_length))
            em = str(view_state.bot.get_em(grade_stat(base))) if actual != 'sp' else ""

            label_row.append(label)
            
            value_row.append(em+val.ljust(longest_length, '\u2007'))
    
        rows.append("\u2007".join(label_row))
        rows.append("\u2007".join(value_row))
        rows.append("")
    
    stat_line = "\n".join(rows)
    return stat_line

def create_race_button(race, page):
    btn = Button(race.name, emoji=race.get_emoji(view_state))
    @interaction(btn)
    async def _show_info(i, race=race):
        await i.response.edit_message(
            view=view_race_info(prof, uid, race, page)
        )
    return btn

def race_schedule(prof, uid, page=0):
    _career: Career = prof['career']

    _displaying_turn = _career.turn+page

    _month = _displaying_turn//2
    _half = (_displaying_turn-1)%2
    _year = _month//12
    month = tr('career.months', (_month+3)%12, prof)
    early = "late" if _half == 0 else "early"
    half = tr(f'career.half.{early}', 0, prof)
    year = tr(f'career.year', _year, prof)
    em = _uma_em(_career.name)

    elements = []

    current_row = []

    races_in_turn: list[RaceData] = SCHEDULES.get(_displaying_turn, [])
    if _displaying_turn == 4: # debut race
        current_row.append(
            create_race_button(
                _career.goals[0].race_data
            )
        )
    if races_in_turn:
        for race in races_in_turn:
            btn = create_race_button(race, page)

            current_row.append(btn)

            if len(current_row) == 5:
                elements.append(ActionRow(*current_row))
                current_row = []
    if current_row:
        elements.append(ActionRow(*current_row))
    if not elements:
        elements.append(Text(
            tr("errors.race.none", 0, prof)
        ))


    return View(
        Container(
            Text(
                tr("race.schedule.title", 0, prof, em, year, month, half)
            ),
            *elements,
            *pagination_buttons(
                lambda p: race_schedule(prof, uid, p),
                max_pages=len(SCHEDULES)-_career.turn,
                lang=prof,
                current_page=page,
                far_buttons=True,
                back_factory=lambda: career(prof, uid)
            )
        ),
        owner = uid
    )


def training(prof, uid, confirm_stat=None):
    _career = prof['career']
    if _career.current_goal is not None:
        goal = _career.current_goal
        if isinstance(goal, RaceGoal):
            return career(prof, uid)
    em = _uma_em(_career.name)
    training_header = tr("training.header", 0, prof, em, _career.name, _career.energy)
    mood = _mood_em(_career)

    stats_displayed = []
    training_btns = []

    preview = _career.train(confirm_stat, True) if confirm_stat else {}
    
    for stat, values in zip(stat_names, _career.stats):
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
                _career.train(stat)
                return await i.response.edit_message(view=training(prof, uid, None))
            else:
                return await i.response.edit_message(view=training(prof, uid, stat))
    
    stats_displayed.append(('sp', tr('training.skill_pts_label', 0, prof), _career.skill_points))
    
    stat_line = get_statline(stats_displayed, compact=prof['settings']['mobile_mode'])

    return View(
        Container(
            Section(
                Text(f"## **{training_header}**"),
                Text(f"-# **{get_goal_header(prof, uid)}**"),
                Text(stat_line),
                accessory=Thumbnail(
                    url=mood.url
                )
            )
        ),
        Container(
            ActionRow(*training_btns)
        ),
        Container(
            ActionRow(_back_button(
                prof,
                lambda: career(prof, uid)
            ))
        )
    )

def career_failure(prof, uid):
    return View(Text("Your shit is cooked dumbass"))

def career(prof, uid, goal_only=False):
    _career = prof['career']
    if not _career:
        return career_select(prof, uid)
    if _career.current_goal is not None and not goal_only:
        goal = _career.current_goal

        if isinstance(goal, RaceGoal):
            return career(prof, uid, True)
        elif isinstance(goal, FanGoal):
            if goal.requirement > _career.fans:
                return career_failure(prof, uid)

    em = _uma_em(_career.name)
    training_header = tr("training.header", 0, prof, '','', _career.energy)

    month = tr('career.months', _career.month%12, prof)
    early = "early" if _career.half == 0 else "late"
    half = tr(f'career.half.{early}', 0, prof)
    year = tr(f'career.year', _career.year, prof)
    mood = _mood_em(_career)

    train = Button(tr('career.btn.train', 0, prof), emoji=view_state.bot.get_em("ui_career"))
    race = Button(tr('career.btn.race', 0, prof), emoji="🏁")
    sleep = Button(tr('career.btn.rest', 0, prof))

    @interaction(train)
    async def _train(i):
        await i.response.edit_message(view=training(prof, uid))
    @interaction(race)
    async def _race(i):
        await i.response.edit_message(view=race_schedule(prof, uid))
    @interaction(sleep)
    async def _sleep(i):
        _career.energy+=random.choice([30,50,70])
        _career.energy=min(_career.max_energy, _career.energy)

        _career.advance()
        await i.response.edit_message(view=career(prof, uid, goal_only))
    if not goal_only:
        elements = ActionRow(
            train, race, sleep
        )
    else:
        elements = ActionRow(
            race
        )
    
    return View(Container(
        Section(
            Text(
                tr("career.header", 0, prof, em, _career.name, training_header, year, month, half)
            ),
            Text(f"-# **{get_goal_header(prof, uid)}**"),
            accessory=Thumbnail(
                url=mood.url
            )
        ),
        elements,
    ),
    Container(
        ActionRow(_back_button(prof, career))
    ),

    owner=uid)
