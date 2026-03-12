from __future__ import annotations

import random
from typing import Optional

from .conditions import apply_all_conditions, get_condition_by_name, ConditionType
from src.careers.races import ALL_RACES, RACE_BY_NAME, Race as RaceTemplate

STAT_NAMES: list[str] = ["spd", "stm", "pwr", "gut", "wit"]
MOOD_LEVELS: list[str] = ["Awful", "Bad", "Normal", "Good", "Great"]

PRIMARY_GAIN_RANGES: dict[str, tuple[int, int]] = {
    "spd": (4, 10), "stm": (4, 10), "pwr": (4, 10), "gut": (3, 8), "wit": (3, 8),
}

SECONDARY_GAIN_RATIO: dict[str, list[tuple[str, float]]] = {
    "spd": [("pwr", 0.30)], "stm": [("gut", 0.30)], "pwr": [("spd", 0.30)],
    "gut": [("stm", 0.30)], "wit": [],
}

SKILL_POINTS_PER_TRAINING: dict[str, int | tuple[int, int]] = {
    "spd": 2, "stm": 2, "pwr": 2, "gut": 2, "wit": (8, 12),
}

TRAINING_COST_RANGES: dict[str, tuple[int, int]] = {
    "spd": (15, 25), "stm": (15, 25), "pwr": (15, 25), "gut": (20, 30), "wit": (-5, -5),
}

MOOD_MULTIPLIER: list[float] = [0.5, 0.8, 1.0, 1.2, 1.5]

_BASE_FANS_BY_GRADE: dict[str, int] = {
    "Debut": 500, "Maiden": 300, "G3": 2000, "G2": 3000, "G1": 5000, "URA": 10000,
}

_PLACEMENT_FAN_MULT: dict[int, float] = {
    1: 2.0, 2: 1.5, 3: 1.2, 4: 1.0, 5: 0.8,
}

_STAT_INDEX: dict[str, int] = {name: i for i, name in enumerate(STAT_NAMES)}

class Career:
    def __init__(
        self,
        name: str,
        owner: str,
        stats: Optional[list[int]] = None,
        energy: int = 100,
        fans: int = 1,
        conditions: Optional[list[str]] = None,
        skills: Optional[list[str]] = None,
        skill_points: int = 0,
        mood: int = 2,
        current_month: int = 1,
        current_half: str = "early",
        year: int = 1,
        game_over: bool = False,
        race_history: Optional[list[dict]] = None,
        seed: Optional[int] = None,
    ):
        self.name             = name
        self.owner            = owner
        self.stats            = list(stats) if stats else [100] * len(STAT_NAMES)
        self.energy           = energy
        self.fans             = fans
        self.conditions       = list(conditions) if conditions else []
        self.skills           = list(skills)     if skills     else []
        self.skill_points     = skill_points
        self.mood             = max(0, min(4, mood))
        self.current_month    = current_month
        self.current_half     = current_half
        self.year             = year
        self.game_over        = game_over
        self.race_history     = list(race_history) if race_history else []
        self.seed             = seed or random.randint(0, 1000000)
        self.rng              = random.Random(self.seed)

    @classmethod
    def create_new(cls, name: str, owner: str) -> "Career":
        return cls(name=name, owner=owner)

    @classmethod
    def from_save_list(cls, owner: str, data: list) -> "Career":
        name, stats, raw = data[0], data[1], data[2]
        def _get(idx, default): return raw[idx] if idx < len(raw) else default
        return cls(
            name=name, owner=owner, stats=stats,
            energy=_get(0, 100), fans=_get(1, 1), conditions=_get(2, []),
            skills=_get(6, []), skill_points=_get(7, 0), mood=_get(8, 2),
            current_month=_get(9, 1), current_half=_get(10, "early"),
            year=_get(11, 1), game_over=_get(12, False), race_history=_get(13, [])
        )

    def to_save_list(self) -> list:
        return [self.name, self.stats, [
            self.energy, self.fans, self.conditions, [], [], 0, # Placeholders for removed goals/scheduled
            self.skills, self.skill_points, self.mood, self.current_month,
            self.current_half, self.year, self.game_over, self.race_history
        ]]

    def get_stat_info(self) -> list[tuple[str, int]]:
        return [(name, self.stats[i]) for i, name in enumerate(STAT_NAMES)]

    def train(self, stat: str) -> dict:
        if self.game_over: return {"success": False, "failure_reason": "game_over"}
        energy_cost = random.randint(*TRAINING_COST_RANGES.get(stat, (15, 25)))
        if self.energy < energy_cost:
            self.energy = max(0, self.energy - int(self.energy * 0.3))
            if random.random() < 0.5: self.conditions.append("PracticePoor")
            return {"success": False, "failure_reason": "low_energy"}

        ctx = {"stat": stat, "stat_gain_multiplier": 1.0, "skill_point_multiplier": 1.0}
        apply_all_conditions(self.conditions, ctx)

        raw_primary = random.randint(*PRIMARY_GAIN_RANGES.get(stat, (3, 8)))
        primary_gain = int(raw_primary * MOOD_MULTIPLIER[self.mood] * ctx["stat_gain_multiplier"])
        
        gains = {stat: primary_gain}
        for sec, ratio in SECONDARY_GAIN_RATIO.get(stat, []):
            val = int(primary_gain * ratio)
            if val > 0: gains[sec] = val

        for s, g in gains.items(): self.stats[_STAT_INDEX[s]] += g

        sp = int((random.randint(8, 12) if stat == "wit" else 2) * ctx["skill_point_multiplier"])
        self.skill_points += sp
        self.energy = max(0, self.energy - energy_cost)
        self.advance_turn()
        return {"success": True, "gains": gains, "sp_gained": sp}

    def rest(self):
        self.energy = min(100, self.energy + random.randint(30, 70))
        self.advance_turn()

    def recreation(self):
        self.mood = min(4, self.mood + 1)
        self.energy = min(100, self.energy + 5)
        self.advance_turn()

    def infirmary(self):
        bad = [c for c in self.conditions if (gc := get_condition_by_name(c)) and gc.cond_type == ConditionType.BAD]
        if bad and random.random() < 0.6: self.conditions.remove(random.choice(bad))
        self.advance_turn()

    def run_race(self, race_name: str, placement: int):
        race = RACE_BY_NAME.get(race_name)
        if not race: return
        self.fans += int(_BASE_FANS_BY_GRADE.get(race.grade, 1000) * _PLACEMENT_FAN_MULT.get(placement, 0.5))
        self.energy = max(0, self.energy - max(10, race.distance // 200))
        self.race_history.append({"name": race_name, "placement": placement, "year": self.year})
        self.advance_turn()

    def advance_turn(self):
        if self.current_half == "early": self.current_half = "late"
        else:
            self.current_half = "early"
            self.current_month += 1
            if self.current_month > 12:
                self.current_month = 1
                self.year += 1
