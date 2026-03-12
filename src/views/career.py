from __future__ import annotations
import random
import asyncio
from typing import Optional
from uicord import *
from .translations import tr
from .pages import pagination_buttons, error
from .state import view_state

from src.careers.career import Career, STAT_NAMES, MOOD_LEVELS, TRAINING_COST_RANGES, PRIMARY_GAIN_RANGES, MOOD_MULTIPLIER
from src.careers.races import ALL_RACES, RACE_BY_NAME

_STAT_KEYS = {"spd": "stats.speed", "stm": "stats.stamina", "pwr": "stats.power", "gut": "stats.guts", "wit": "stats.wit"}

def _lang(prof): return prof["settings"]["lang"]
def _stat_label(stat, prof): return tr(_STAT_KEYS[stat], 0, prof)
def _uma_em(name): return view_state.bot.get_em(name.replace(" ", "_").lower()) or "🐴"
def _mood_em(career): return view_state.bot.get_em(f"mood_{MOOD_LEVELS[career.mood].lower()}")

def _back_button(lang, view_factory):
    btn = Button(emoji=view_state.bot.get_em("ui_back"), text=tr("ui.label", 0, lang))
    @interaction(btn)
    async def _back(ctx): await ctx.response.edit_message(view=view_factory())
    return btn

def career_select(prof, uid, page=0):
    umas = prof.get("inventory", {}).get("umas", {})
    if not umas: return error(prof, uid, "career.no_uma", back_view_factory=lambda: view_state.views.home(prof, uid))
    names = list(umas.keys())
    max_p = max(0, (len(names)-1)//4)
    page_names = names[page*4:page*4+4]
    btns = []
    for name in page_names:
        btn = Button(f"{name} {'⭐'*umas[name][1]}", emoji=_uma_em(name), color=Colors.Grey)
        @interaction(btn)
        async def _pick(i, n=name): await i.response.edit_message(view=view_career_select_confirm(prof, uid, n))
        btns.append(btn)
    pagination = pagination_buttons(lambda p: career_select(prof, uid, p), max_p, _lang(prof), page, back_factory=lambda: view_state.views.home(prof, uid))
    return View(Container(Text(tr("career.select.title", 0, prof)), ActionRow(*btns), *pagination), owner=uid)

def view_career_select_confirm(prof, uid, name):
    start = Button(tr("career.select.start", 0, prof), emoji="🏁", color=Colors.Green)
    @interaction(start)
    async def _start(ctx):
        prof["career"] = Career.create_new(name, str(uid))
        await ctx.response.edit_message(view=career(prof, uid))
    return View(Container(Section(Text(f"## {name} {_uma_em(name)}"), accessory=Thumbnail(url=getattr(_uma_em(name), "url", ""))), Separator(), ActionRow(start, _back_button(_lang(prof), lambda: career_select(prof, uid)))), owner=uid)

def career(prof, uid):
    c: Career = prof["career"]
    if c.game_over: return view_career_over(prof, uid)
    
    thumb = getattr(_mood_em(c), "url", "")
    btn_train = Button(tr("career.btn.train", 0, prof), emoji="💪")
    btn_rest = Button(tr("career.btn.rest", 0, prof), emoji="🛏️")
    btn_recreate = Button(tr("career.btn.recreate", 0, prof), emoji="🎡")
    btn_infirm = Button(tr("career.btn.infirmary", 0, prof), emoji="🏥")
    btn_race = Button(tr("career.btn.race", 0, prof), emoji="🏁")
    btn_skills = Button(tr("career.btn.skills", 0, prof), emoji=view_state.bot.get_em("yellow_gold") or "⭐")
    
    @interaction(btn_train)
    async def _train(i): await i.response.edit_message(view=view_training(prof, uid))
    @interaction(btn_rest)
    async def _rest(i): c.rest(); await i.response.edit_message(view=career(prof, uid))
    @interaction(btn_recreate)
    async def _recreate(i): c.recreation(); await i.response.edit_message(view=career(prof, uid))
    @interaction(btn_infirm)
    async def _on_infirm(i): c.infirmary(); await i.response.edit_message(view=career(prof, uid))
    @interaction(btn_race)
    async def _on_race(i): await i.response.edit_message(view=view_race_calendar(prof, uid))
    @interaction(btn_skills)
    async def _on_skills(i): await i.response.edit_message(view=view_skills(prof, uid))

    bad_conds = [cn for cn in c.conditions if (gc := get_condition_by_name(cn)) and gc.cond_type == ConditionType.BAD]
    cond_str = f"\n-# **{tr('career.conditions', 0, prof)}**: {', '.join([tr(f'condition.{cn}', 0, prof) for cn in c.conditions])}" if c.conditions else ""
    header = tr("career.header", 0, prof, _uma_em(c.name), c.name, f"{c.energy}/100", c.year, c.current_month, tr(f"career.half.{c.current_half.lower()}", 0, prof))

    rows = [ActionRow(btn_train, btn_rest, btn_recreate)]
    if bad_conds: rows[0].components.append(btn_infirm)
    rows.append(ActionRow(btn_race, btn_skills))
    rows.append(ActionRow(_back_button(_lang(prof), lambda: view_state.views.home(prof, uid))))

    return View(Container(Section(Text(header + cond_str), accessory=Thumbnail(url=thumb)), *rows), owner=uid)

def view_training(prof, uid, confirm_stat=None):
    c: Career = prof["career"]
    stat_lines = [f"-# {view_state.bot.get_em(s.upper()) or ''} **{_stat_label(s, prof)}** {v:>5}" for s, v in c.get_stat_info()]
    stat_lines.append(f"-# 💡 **{tr('career.skillpoints.label', 0, prof)}** {c.skill_points}")
    
    async def _do_train(i, s):
        res = c.train(s)
        if res["success"]: await i.response.edit_message(view=view_training(prof, uid))
        else: await i.response.edit_message(view=career(prof, uid) if res.get("failure_reason")=="low_energy" else error(prof, uid, f"training.fail.{res.get('failure_reason')}", back_view_factory=lambda: view_training(prof, uid)))

    btns = []
    for s in STAT_NAMES:
        btn = Button(_stat_label(s, prof), color=Colors.Grey, emoji=view_state.bot.get_em(s.upper()))
        @interaction(btn)
        async def _click(i, target=s):
            if confirm_stat != target: await i.response.edit_message(view=view_training(prof, uid, target))
            else: await _do_train(i, target)
        btns.append(btn)
    
    header = tr("career.header", 0, prof, _uma_em(c.name), c.name, f"{c.energy}/100", c.year, c.current_month, tr(f"career.half.{c.current_half.lower()}", 0, prof))
    if confirm_stat: header += f" | 💪 **{_stat_label(confirm_stat, prof)}**"
    
    return View(Container(Section(Text(header + "\n" + "\n".join(stat_lines)), accessory=Thumbnail(url=getattr(_mood_em(c), "url", ""))), ActionRow(*btns[:3]), ActionRow(*btns[3:]), Separator(), ActionRow(_back_button(_lang(prof), lambda: career(prof, uid)))), owner=uid)

def view_skills(prof, uid, page=0, back_factory=None):
    c: Career = prof["career"]
    owned, sp = c.skills, c.skill_points
    back_factory = back_factory or (lambda: career(prof, uid))
    from src.skills import MOST_EXPENSIVE_SKILLS, SKILLS_BY_NAME
    max_p = max(0, (len(MOST_EXPENSIVE_SKILLS)-1)//5)
    subset = MOST_EXPENSIVE_SKILLS[page*5:page*5+5]
    lines, btns = [], []
    for sk in subset:
        lines.append(f"{sk.display(view_state.bot)}\n-# {sk.desc}")
        btn = Button(f"{sk.name} {sk.price}", emoji=view_state.bot.get_em(sk.icon) or "⭐", color=Colors.Grey, disabled=sk.id in owned)
        @interaction(btn)
        async def _buy(i, s=sk):
            if sp >= s.price: c.skills.append(s.id); c.skill_points -= s.price; await i.response.edit_message(view=view_skills(prof, uid, page, back_factory))
            else: await i.response.edit_message(view=error(prof, uid, "skills.no_sp", back_view_factory=lambda: view_skills(prof, uid, page, back_factory)))
        btns.append(btn)
    lines.append(f"\n### {tr('training.skill_info', 0, prof, sp, len(owned))}")
    pagination = pagination_buttons(lambda p: view_skills(prof, uid, p, back_factory), max_p, _lang(prof), page, back_factory=back_factory)
    return View(Container(Text("\n".join(lines)), ActionRow(*btns), *pagination), owner=uid)

def view_race_calendar(prof, uid, page=0):
    c: Career = prof["career"]
    m, h = (page % 24 // 2) + 1, ("early" if page % 2 == 0 else "late")
    y = (page // 24) + 1
    races = [r for r in ALL_RACES if r.month == m and r.half == h]
    is_today = (y == c.year and m == c.current_month and h == c.current_half)
    btns = []
    for r in races[:5]:
        btn = Button(r.name, emoji=view_state.bot.get_em(f"grade_{r.grade.lower()}"), color=Colors.Green if is_today else Colors.Grey, disabled=(is_today and getattr(c, "_raced_this_turn", False)))
        @interaction(btn)
        async def _run_or_sched(i, race=r):
            if is_today:
                from src.race.race import Race
                from src.race.uma import RaceUma
                from src.race.view import RaceView
                from src.skills import SKILLS_BY_NAME, SKILLS
                from src.data.uma_database import UMA_DB
                p_skills = [SKILLS_BY_NAME[sn] for sn in c.skills if sn in SKILLS_BY_NAME]
                p_uma = RaceUma(c.name, c.stats, _uma_em(c.name), is_player=True, owner=uid, career=c, skills=p_skills)
                runners = [p_uma]
                for o_data in random.sample([u for u in UMA_DB if u.name != c.name], 5):
                    diff = 0.8 + random.random() * 0.4
                    o_skills = ([o_data.ult] if o_data.ult else []) + random.sample(list(SKILLS), random.randint(1, 2))
                    runners.append(RaceUma(o_data.name, [int(s*diff) for s in o_data.stats], _uma_em(o_data.name), skills=o_skills))
                new_race = Race(view_state.bot, c, runners, race.distance, race)
                view = RaceView(new_race, uid)
                await i.response.edit_message(view=view.get_view())
                while not new_race.finished:
                    await asyncio.sleep(1); new_race.step(); await i.edit_original_response(view=view.get_view())
                c.run_race(race.name, p_uma.placement)
                await i.edit_original_response(view=View(Container(Text(f"## Race Finished!\nPlacement: **{p_uma.placement}**"), ActionRow(_back_button(_lang(prof), lambda: career(prof, uid))))))
            else: pass # Sched removed
        btns.append(ActionRow(btn))
    pagination = pagination_buttons(lambda p: view_race_calendar(prof, uid, p), 71, _lang(prof), page, back_factory=lambda: career(prof, uid))
    return View(Container(Text(f"### {y}Y {m}M {h.upper()}"), *btns, *pagination), owner=uid)

def view_career_over(prof, uid):
    c: Career = prof["career"]
    stats = [f"-# {view_state.bot.get_em(s.upper()) or ''} **{_stat_label(s, prof)}** {v:>5}" for s, v in c.get_stat_info()]
    end_btn = Button(tr("career.btn.end", 0, prof), color=Colors.Red)
    @interaction(end_btn)
    async def _on_end(i):
        prof.setdefault("fans", 0); prof["fans"] += c.fans
        prof.setdefault("old_careers", []).append({"stats": list(c.stats), "skills": list(c.skills), "name": c.name, "fans": c.fans, "mood": c.mood})
        prof["career"] = None; await i.response.edit_message(view=view_state.views.home(prof, uid))
    return View(Container(Section(Text(f"## {tr('career.over.title', 0, prof)}\n" + "\n".join(stats))), ActionRow(end_btn)), owner=uid)

view_state.views.career = career
view_state.views.career_select = career_select
