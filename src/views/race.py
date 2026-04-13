import asyncio
from collections import deque

from uicord      import View, Container, Text, Separator, ActionRow, Button, interaction
from .translations import tr
from .pages import _create_back_button
from src.race.models  import Race, RaceUma, RANKING_EMOJIS, ORDINAL
from src.race.engine  import step
from src.race.rewards import give_career_rewards, give_daily_rewards, give_club_rewards

_BAR_STEPS  = 29
_LANE_ICONS = ["▸1", "▸2", "▸3"]

def _progress_bar(u: RaceUma, dist: float) -> str:
    pct   = min(u.pos, dist) / dist
    steps = round(pct * _BAR_STEPS)
    if steps <= 1:
        return ""
    return "**" + ("─" * (steps - 1)) + "**➔"


def _lane_badge(lane: int) -> str:
    try:
        return f"`{_LANE_ICONS[lane]}`"
    except IndexError:
        return f"`L{lane + 1}`"


def _placement_label(place: int) -> str:
    suf = ORDINAL.get(place, "th")
    return f"**{place}{suf}**"


def build_race_view(prof, uid, race: Race, back=None) -> View:
    lang = prof["settings"]["lang"]
    dist       = race.race_data.distance_meters
    sorted_r   = race.standings()

    body = f"### **{race.race_data.name}** {race.race_em} ***{dist}m***\n\n"

    for idx, u in enumerate(sorted_r, start=1):
        finish_badge = RANKING_EMOJIS[min(idx - 1, 3)] if u.finished else ""
        bar          = _progress_bar(u, dist)
        lane         = _lane_badge(u.lane)
        u.placement  = idx + 1

        body += f"{chr(idx + 10101)} {u.emoji} **{u.name}** {u.display_effects()} {lane}\n"
        body += f"{bar}{finish_badge}\n"

        if u.effects:
            u.effects.pop()
        u.activate_skills(race)

    events = list(race.event_queue)[-10:]
    for i, ev in enumerate(events):
        body += ("-# " if i == 0 else "") + ev["text"] + "\n"

    back_btn = _create_back_button(prof, back)

    if back:
        @interaction(back_btn)
        async def _go_back(i):
            await i.response.edit_message(view=back())
        components = [Text(body), Separator(), ActionRow(back_btn)]
    else:
        components = [Text(body)]

    return View(Container(*components), owner=uid)


async def show_race(prof, uid, race: Race, ctx, back_function) -> None:
    race.winners = []
    await ctx.response.edit_message(view=View(Text("Racing…")))

    while not race.finished:
        step(race)
        await ctx.edit_original_response(view=build_race_view(prof, uid, race))
        await asyncio.sleep(1)

    race.event_queue = deque()
    await show_results(prof, uid, race, ctx, back_function)


async def show_skipped(prof, uid, race: Race, ctx, back_function) -> None:
    race.winners = []
    await ctx.response.edit_message(view=View(Text("Skipping through the race!")))
    while not race.finished:
        step(race)
    await show_results(prof, uid, race, ctx, back_function)


async def show_results(prof, uid, race: Race, ctx, back_function) -> None:
    lang = prof["settings"]["lang"]
    if race.club_race:
        _push_club_result(race, lang)
    elif race.IS_DAILY:
        _push_daily_result(race, lang)
    else:
        _push_career_result(race, lang)
    prof["career"].check_goal(
        {"goal_type": "race", "placement": race.career_placement}
    )

    await ctx.edit_original_response(view=build_race_view(prof, uid, race, back=back_function))


def _placement_line(race: Race, lang) -> str:
    place = race.career_placement
    label = _placement_label(place)
    return tr("race.result.placement", 0, lang, label)


def _push_career_result(race: Race, lang) -> None:
    won, rewards = give_career_rewards(race, race.bot, race.career, race.owner, race.winners)
    place_line   = _placement_line(race, lang)
    detail=""
    for item, am in rewards.get("items", ()):
        detail+=f"-# {race.bot.get_item_em(item)} × {am}\n"
    if won:
        title  = tr("race.result.won",           0, lang)
        detail += tr("race.result.reward.career",  0, lang,
                    rewards.get("fans", 0), rewards.get("sp", 0), rewards.get("carats", 0))
    else:
        title  = tr("race.result.lost", 0, lang)
        detail += str(race.bot.em["Tazuna"])
    race.push_event(f"{title} {place_line}\n{detail}")


def _push_daily_result(race: Race, lang) -> None:
    won, rewards = give_daily_rewards(race, race.bot, race.owner, race.winners)
    place_line   = _placement_line(race, lang)
    if won:
        title  = tr("race.result.won",          0, lang)
        detail = tr("race.result.reward.daily",  0, lang,
                    rewards.get("carats", 0), rewards.get("exp", 0))
    else:
        title  = tr("race.result.lost", 0, lang)
        detail = str(race.bot.em["Tazuna"])
    race.push_event(f"{title} {place_line}\n{detail}")


def _push_club_result(race: Race, lang) -> None:
    placements = give_club_rewards(race.winners)
    msg        = tr("race.result.club.title", 0, lang) + "\n"
    for entry in placements:
        place = entry["place"]
        uma   = entry["uma"]
        msg  += tr("race.result.club.entry", 0, lang,
                   _placement_label(place), str(uma.owner),
                   uma.career.uma.name, str(uma.emoji))
    race.push_event(msg)
