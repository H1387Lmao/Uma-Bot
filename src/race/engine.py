import random

from .models import (
    NUM_LANES,
    GUTS_OVERTAKE_COST, GUTS_DEFEND_COST,
    GUTS_BLOCK_COST,    GUTS_RESIST_COST,
    GUTS_FAIL_PENALTY,  POWER_FAIL_PENALTY,
    BLOCK_PENALTY,      BLOCK_RANGE,
)


def _lane_leader_pairs(sorted_runners):
    seen: dict[int, object] = {}
    for u in sorted_runners:
        if u.finished:
            continue
        if u.lane in seen:
            yield (seen[u.lane], u)
        else:
            seen[u.lane] = u


def run_lanes(race) -> None:
    sorted_runners = sorted(race.runners, key=lambda u: u.pos, reverse=True)
    being_blocked: set[int] = set()
    for ahead, behind in _lane_leader_pairs(sorted_runners):
        if ahead.pos - behind.pos <= BLOCK_RANGE:
            being_blocked.add(id(behind))
    for u in race.runners:
        if u.finished:
            continue
        chance   = 0.55 if id(u) in being_blocked else 0.15
        if random.random() < chance:
            new_lane = u.lane + random.choice((-1, 1))
            if 0 <= new_lane < NUM_LANES:
                u.lane = new_lane


def run_blocking(race) -> None:
    sorted_runners = sorted(race.runners, key=lambda u: u.pos, reverse=True)
    for ahead, behind in _lane_leader_pairs(sorted_runners):
        gap = ahead.pos - behind.pos
        if gap <= BLOCK_RANGE:
            if ahead.guts >= GUTS_BLOCK_COST:
                ahead.guts  -= GUTS_BLOCK_COST
                behind.gain *= BLOCK_PENALTY
                if behind.guts >= GUTS_RESIST_COST:
                    behind.guts -= GUTS_RESIST_COST
                    behind.gain *= (1 / BLOCK_PENALTY) * 0.85
            else:
                ahead.vel *= GUTS_FAIL_PENALTY

        if gap <= behind.gain:
            if behind.guts >= GUTS_OVERTAKE_COST:
                behind.guts -= GUTS_OVERTAKE_COST
                behind.gain += behind.stm * 0.03
            else:
                behind.vel *= GUTS_FAIL_PENALTY
                behind.pwr *= POWER_FAIL_PENALTY
            if ahead.guts >= GUTS_DEFEND_COST:
                ahead.guts -= GUTS_DEFEND_COST
            else:
                ahead.vel *= GUTS_FAIL_PENALTY


def step(race) -> None:
    race.turn += 1

    for u in race.runners:
        if not u.finished:
            u.gain = min(120, u.vel)

    run_lanes(race)
    run_blocking(race)

    spread = len(race.runners) - len(race.winners)
    dist   = race.race_data.distance_meters

    for u in race.runners:
        if u.finished:
            continue
        u.pos = min(dist, u.pos + u.gain) + spread
        if u.pos >= dist:
            u.finished = True
            race.winners.append(u)
            u.pos += spread + 1
        elif u.stm > (1600 - u.pwr) // 2:
            u.vel  += u.ACCEL_RATE
            u.stm  -= u.ACCEL_RATE * 40

    if not race.club_race and any(u.finished for u in race.runners):
        race.finished = True
        for u in race.runners:
            u.finished = True
        race.event_queue.clear()
        return

    if all(u.finished for u in race.runners):
        race.finished = True
        race.event_queue.clear()
        return

    race.tick_events()
