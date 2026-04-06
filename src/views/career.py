from ..career import *
from uicord import *
from .translations import translator, tr, SUPPORTED_LANGS, TRANSLATIONS, typewriter
from .pages import pagination_buttons, error, _back_button
from .state import view_state
from ..data import grade_map, grade_stat, SCHEDULES
from ..race import *
from .race import *
from .skills import skill_shop
from ..utils import get_stat_graph

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
       args=[goal_info.requirement]
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
    c: Career = prof['career']
    d_ev = race.evaluate_distance(c.apts)
    g_ev = race.evaluate_ground(c.apts)

    d_stars = "⭐" if d_ev else ""
    g_stars = "⭐" if g_ev else ""

    schedule = Button(tr("race.schedule.pick", 0, prof))
    @interaction(schedule)
    async def _schedule(i):
        c.races_scheduled[race.turn] = race
        await i.response.edit_message(view=race_schedule(prof, uid, page))

    return View(
        Container(
            Text(f"# {race.name} {d_stars}{g_stars}"),
            ActionRow(
                schedule
            )
        ),
        Container(
            ActionRow(
                _back_button(prof, lambda: race_schedule(prof, uid, page))
            )
        ), owner=uid
    )

def career_select(prof, uid, page=0):
    if prof["career"]:
        return career(prof, uid)
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
    
    cols = 2
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

def get_abs_sign(numb):
    return (f"+{numb}" if numb > 0 else str(numb)) if numb != 0 else "0"

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
                val = typewriter(f"{base} **({get_abs_sign(bonus)})**")
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

def create_race_button(prof, uid, race, page, d_ev, g_ev):
    reccomended = "⭐" if d_ev and g_ev else ""

    btn = Button(f"{race.name}{reccomended}", emoji=race.get_emoji(view_state))

    @interaction(btn)
    async def _show_info(i, race=race):
        if page!=0:
            await i.response.edit_message(
                view=view_race_info(prof, uid, race, page)
            )
        else:
            r = Race(prof["career"], race, i.user)
            fn = show_race if not prof["settings"]["skip_race"] else show_skipped
            await fn(prof, uid, r, i, lambda: career(prof, uid))
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
    queued = ""
    if _displaying_turn in _career.races_scheduled:
        queued = f"\n-# **{tr("race.schedule.queued",0,prof,_career.races_scheduled[_displaying_turn].name)}**"
    if _displaying_turn == 4: # debut race
        race = _career.goals[0].race_data
        d_ev = race.evaluate_distance(_career.apts)
        g_ev = race.evaluate_ground(_career.apts)
        current_row.append(
            create_race_button(
                prof, uid, race, page, d_ev, g_ev
            )
        )
    if races_in_turn:
        for race in races_in_turn:
            d_ev = race.evaluate_distance(_career.apts)
            g_ev = race.evaluate_ground(_career.apts)
            btn = create_race_button(prof, uid, race, page, d_ev, g_ev)

            if _career.current_goal is not None:
                if _career.current_goal.race_data != race:
                    btn.disabled = True

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
                tr("race.schedule.title", 0, prof, em, year, month, half)+queued
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
def failed_training(prof, uid, stat):
    c = prof['career']

    failed_info = ""

    c.energy //= 2
    c.mood = max(0, c.mood-1)
    stat_index = c.stat_to_index(stat)
    c.stats[stat_index]-=5

    if random.random() <= 0.45:
        c.conditions.add(0)
        c.has_bad=True
        cond = tr('condition.PracticePoor', 0, prof)
        failed_info+=tr("career.attained_condition", 0, prof, cond)

    return View(
        Container(
            Section(
                Text(f'## **{tr("errors.training.fail.low_energy", 0, prof)}**'),
                *([Text(f"-# {failed_info}")] if failed_info else []),
                accessory=Thumbnail(url=view_state.bot.get_em("failed").url)
            ),
            ActionRow(_back_button(prof, lambda: career(prof, uid)))
        ), owner = uid
    )

def training(prof, uid, confirm_stat=None):
    _career = prof['career']
    if _career.current_goal is not None:
        goal = _career.current_goal
        if isinstance(goal, RaceGoal):
            return career(prof, uid)
    em = _uma_em(_career.name)
    
    mood = _mood_em(_career)

    stats_displayed = []
    training_btns = []

    preview = _career.train(confirm_stat, True) if confirm_stat else {}


    energy_display = f"{_career.energy}/{_career.max_energy}"
    if preview:
        energy_display += "**("+get_abs_sign(preview['energy'])+")**"
    training_header = tr("training.header", 0, prof, em, _career.name, energy_display)
    for stat, values in zip(stat_names, _career.stats):
        st = tr(f'stats.{stat}', 0, prof)
        if confirm_stat and stat in preview:
            stats_displayed.append((stat, st, (values, preview[stat])))
        else:
            stats_displayed.append((stat, st, values))
        if confirm_stat == stat:
            st+=f' {(preview['failure_rate']*100):.0f}%'
        btn = Button(tr('training.train_button', 0, prof, st), emoji=_stat_em(stat))
        training_btns.append(btn)
    
        @interaction(btn)
        async def _train(i, stat=stat):
            if confirm_stat == stat:
                res = lambda: training(prof, uid, None)
                if preview['failure_rate']>random.random():
                    res = lambda: failed_training(prof, uid, confirm_stat)
                else:
                    _career.train(stat)
                return await i.response.edit_message(view=res())
            else:
                return await i.response.edit_message(view=training(prof, uid, stat))
    if confirm_stat and 'sp' in preview:
        sp_val = (_career.skill_points, preview["sp"])
    else:
        sp_val = _career.skill_points

    stats_displayed.append(('sp', tr('training.skill_pts_label', 0, prof), sp_val))
    
    stat_line = get_statline(stats_displayed, compact=prof['settings']['mobile_mode'])

    return View(
        Container(
            Section(
                Text(f"## {training_header}"),
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
        ), owner=uid
    )

def completion_screen(prof, uid, result, fans, graph):
    bot = view_state.bot
    title = tr('errors.career.ended', 0, prof)
    skills = [SKILLS[skid].display(bot) for skid in result["skills"]] or [tr("skills.none", 0, prof)]
    return View(
        Container(
            Section(
                Text(f"# **{title}**{bot.get_uma(result["name"])}"),
                Text(f"-# **{tr("career.summary.fans",0,prof, fans)}**"),
                Text("-# "+("\n-# ".join(skills))),
                accessory=Thumbnail(
                    url=bot.get_em(result["rank"]).url
                )
            ),
            MediaGallery(MediaGalleryItem(
                url=graph
            )),
            ActionRow(
                _back_button(prof, lambda: view_state.views.home(prof, uid))
            )
        ),
        owner=uid
    )

def career_failure(prof, uid):
    _career = prof['career']
    skills = Button(tr('career.btn.skills', 0, prof), emoji=view_state.bot.get_em("ui_skills"))
    complete = Button(tr('career.btn.complete', 0, prof), emoji="🎉")
    @interaction(skills)
    async def _skills(i):
        await i.response.edit_message(view=skill_shop(prof, uid))

    stats_displayed = []

    for stat, values in zip(stat_names, _career.stats):
        st = tr(f'stats.{stat}', 0, prof)
        stats_displayed.append((stat, st, values))
    stats_displayed.append(('sp', tr('training.skill_pts_label', 0, prof), _career.skill_points))
    graph=get_stat_graph(
        [s[1:] for s in stats_displayed[:-1]]
    )
    
    @interaction(complete)
    async def _complete(i, graph=graph):
        res = _career.complete(prof)
        prof["old_careers"].append(
            res
        )
        await i.response.edit_message(
            view=completion_screen(prof, uid, res, _career.fans, graph)
        )

    return View(
        Container(
            Text(f"# **{tr("errors.career.ended", 0,prof)}**"),
            Text(get_statline(
                stats_displayed,
                prof["settings"]["mobile_mode"]
            )),
            MediaGallery(MediaGalleryItem(
                url=graph
            )),
            ActionRow(
                skills, complete
            )
        ), owner=uid
    )

def career_heal(prof, uid):
    _career = prof['career']
    cleared=set()
    for c in _career.conditions:
        cond = CONDITIONS[c]
        if cond.bad:
            cleared.add(c)
    _career.advance()
    _career.has_bad=False
    _career.conditions-=cleared
    _cleared = [CONDITIONS[c].get_name(prof)+\
                str(view_state.bot.get_em("mark_down"))\
                for c in cleared
            ] or ["nothing was cleared"]
    return View(
        Container(
            Text(f"# **{tr("career.removed_conditions", 0, prof)}**"+f"\n-# {"\n-# ".join(_cleared)}"),
            ActionRow(
                _back_button(prof, lambda: career(prof, uid))
            )
        )
    )
def career(prof, uid, goal_only=False):
    _career = prof['career']
    if not _career:
        return career_select(prof, uid)
    if _career.over:
        return career_failure(prof, uid)
    if _career.current_goal is not None and not goal_only:
        goal = _career.current_goal

        if isinstance(goal, RaceGoal):
            return career(prof, uid, True)
        elif isinstance(goal, FanGoal):
            _career.check_goal({"goal_type": "fans"})
            return career(prof, uid)

    em = _uma_em(_career.name)
    training_header = tr("training.header", 0, prof, '','', _career.energy)

    month = tr('career.months', _career.month%12, prof)
    early = "early" if _career.half == 0 else "late"
    half = tr(f'career.half.{early}', 0, prof)
    year = tr(f'career.year', _career.year, prof)
    mood = _mood_em(_career)

    train = Button(tr('career.btn.train', 0, prof), emoji=view_state.bot.get_em("ui_career"))
    race = Button(tr('career.btn.race', 0, prof), emoji=view_state.bot.get_em("ui_race"))
    sleep = Button(tr('career.btn.rest', 0, prof), emoji=view_state.bot.get_em("ui_rest"))
    recreation = Button(tr('career.btn.recreate', 0, prof), emoji=view_state.bot.get_em("ui_recreate"))
    infirmary = Button(tr('career.btn.infirmary', 0, prof), emoji=view_state.bot.get_em("ui_infirmary"), disabled=not _career.has_bad)
    restcreation = Button(tr('career.btn.restcreate', 0, prof), emoji=view_state.bot.get_em("ui_restcreate"))
    @interaction(train)
    async def _train(i):
        await i.response.edit_message(view=training(prof, uid))
    skills = Button(tr('career.btn.skills', 0, prof), emoji=view_state.bot.get_em("ui_skills"))
    @interaction(skills)
    async def _skills(i):
        await i.response.edit_message(view=skill_shop(prof, uid))
    @interaction(race)
    async def _race(i):
        await i.response.edit_message(view=race_schedule(prof, uid))
    @interaction(sleep)
    async def _sleep(i):
        _career.energy+=random.choice([30,50,70])
        _career.energy=min(_career.max_energy, _career.energy)

        _career.advance()
        await i.response.edit_message(view=career(prof, uid, goal_only))
    @interaction(recreation)
    async def _recreation(i):
        _career.mood=min(4, _career.mood+1)
        _career.advance()
        await i.response.edit_message(view=career(prof, uid, goal_only))

    @interaction(restcreation)
    async def _recreation(i):
        _career.mood=min(4, _career.mood+1)
        _career.energy+=random.choice([30,50,70])
        _career.energy=min(_career.max_energy, _career.energy)

        _career.advance()
        await i.response.edit_message(view=career(prof, uid, goal_only))
    @interaction(infirmary)
    async def _heal(i):
        await i.response.edit_message(view=career_heal(prof, uid))
    if not goal_only:
        slp = [sleep, recreation] if not _career.is_summer() else [restcreation]
        elements = ActionRow(
            train, race, *slp, infirmary
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
        ActionRow(
            skills,
            _back_button(prof, lambda: view_state.views.home(prof, uid)),
        )
    ),

    owner=uid)
    
view_state.views.career=career
