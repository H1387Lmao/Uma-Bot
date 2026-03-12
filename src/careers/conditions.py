from __future__ import annotations

from enum import Enum
from typing import Optional

# Enum

class ConditionType(Enum):
    GOOD = "good"
    BAD  = "bad"

class Condition:
    """Base class for all conditions.

    Subclasses override ``apply_effect`` to mutate the context dict that is
    passed into ``Career.train``.

    Context dict keys currently in use:
        training_failure_bonus (int)  – added to the base failure chance (%).
        skip_training          (bool) – if True the entire training is skipped.
        block_speed            (bool) – if True speed primary gain is forced to 0.
        bond_boost             (int)  – friendship / bond point bonus (future).
        skill_discount         (float)– multiplier applied to skill costs (future).
        stat_gain_multiplier   (float)– multiplies primary stat gain.
        skill_point_bonus      (int)  – flat bonus to skill points earned.
    """

    def __init__(self, name: str, cond_type: ConditionType, description: str):
        self.name        = name
        self.cond_type   = cond_type
        self.description = description

    def apply_effect(self, data: dict) -> dict:
        """Modify training context *in place* and return it."""
        return data

    def can_remove(self, method: str) -> bool:
        """Return True if this condition can be removed by *method*."""
        return True  # default: removable by any method

    def __repr__(self) -> str:
        return f"Condition({self.name!r}, {self.cond_type})"

class PracticePoor(Condition):
    """Training failure chance +10 %."""

    def __init__(self):
        super().__init__(
            "PracticePoor",
            ConditionType.BAD,
            "Poor practice form — training fails more often.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["training_failure_bonus"] = data.get("training_failure_bonus", 0) + 10
        return data

class Migraine(Condition):
    """Wit-training is skipped; all other training has +5 % failure chance."""

    def __init__(self):
        super().__init__(
            "Migraine",
            ConditionType.BAD,
            "Splitting headache — wit training is skipped, others fail more.",
        )

    def apply_effect(self, data: dict) -> dict:
        if data.get("stat") == "wit":
            data["skip_training"] = True
        else:
            data["training_failure_bonus"] = data.get("training_failure_bonus", 0) + 5
        return data

class NightOwl(Condition):
    """Stat gains reduced by 20 % (stat_gain_multiplier)."""

    def __init__(self):
        super().__init__(
            "NightOwl",
            ConditionType.BAD,
            "Stayed up too late — gains are reduced.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["stat_gain_multiplier"] = data.get("stat_gain_multiplier", 1.0) * 0.80
        return data

class DrySkin(Condition):
    """Power training is skipped; speed training has +5 % failure."""

    def __init__(self):
        super().__init__(
            "DrySkin",
            ConditionType.BAD,
            "Skin trouble from dry weather — power training skipped.",
        )

    def apply_effect(self, data: dict) -> dict:
        if data.get("stat") == "power":
            data["skip_training"] = True
        elif data.get("stat") == "speed":
            data["training_failure_bonus"] = data.get("training_failure_bonus", 0) + 5
        return data

class SlowMetabolism(Condition):
    """Stamina training gains are halved."""

    def __init__(self):
        super().__init__(
            "SlowMetabolism",
            ConditionType.BAD,
            "Sluggish body — stamina gains are halved.",
        )

    def apply_effect(self, data: dict) -> dict:
        if data.get("stat") == "stamina":
            data["stat_gain_multiplier"] = data.get("stat_gain_multiplier", 1.0) * 0.50
        return data

class Slacker(Condition):
    """All training has a 15 % chance to be skipped regardless of failure roll."""

    def __init__(self):
        super().__init__(
            "Slacker",
            ConditionType.BAD,
            "Feeling unmotivated — may skip training entirely.",
        )

    def apply_effect(self, data: dict) -> dict:
        import random
        if random.random() < 0.15:
            data["skip_training"] = True
        return data

class UnderTheWeather(Condition):
    """Training failure chance +15 %."""

    def __init__(self):
        super().__init__(
            "UnderTheWeather",
            ConditionType.BAD,
            "Coming down with something — training fails more often.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["training_failure_bonus"] = data.get("training_failure_bonus", 0) + 15
        return data

class NotReady(Condition):
    """First training each turn is always skipped."""

    def __init__(self):
        super().__init__(
            "NotReady",
            ConditionType.BAD,
            "Not mentally prepared — the first training of the turn is skipped.",
        )

    def apply_effect(self, data: dict) -> dict:
        if not data.get("has_trained_this_turn", False):
            data["skip_training"] = True
        return data

class LackOfFocus(Condition):
    """Skill points earned from training are halved."""

    def __init__(self):
        super().__init__(
            "LackOfFocus",
            ConditionType.BAD,
            "Mind is wandering — skill points gained are halved.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["skill_point_multiplier"] = data.get("skill_point_multiplier", 1.0) * 0.50
        return data

class Overtired(Condition):
    """Speed training is blocked (gain = 0) and failure chance +10 %."""

    def __init__(self):
        super().__init__(
            "Overtired",
            ConditionType.BAD,
            "Pushed too hard — speed training is blocked and failure chance rises.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["block_speed"] = True
        data["training_failure_bonus"] = data.get("training_failure_bonus", 0) + 10
        return data

class Charming(Condition):
    """Bond / friendship gains +3."""

    def __init__(self):
        super().__init__(
            "Charming",
            ConditionType.GOOD,
            "Full of charm — bond gains are increased.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["bond_boost"] = data.get("bond_boost", 0) + 3
        return data

class FastLearner(Condition):
    """Skill points gained +3."""

    def __init__(self):
        super().__init__(
            "FastLearner",
            ConditionType.GOOD,
            "Quick on the uptake — bonus skill points every session.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["skill_point_bonus"] = data.get("skill_point_bonus", 0) + 3
        return data

class PracticePerfect(Condition):
    """Reduces training failure chance.

    Level "○" → -5 %; level "◎" → -10 %.
    """

    def __init__(self, level: str = "○"):
        if level not in ("○", "◎"):
            raise ValueError(f"PracticePerfect level must be '○' or '◎', got {level!r}")
        self.level = level
        reduction = 5 if level == "○" else 10
        name = f"PracticePerfect_{level}"
        super().__init__(
            name,
            ConditionType.GOOD,
            f"Perfect practice form ({level}) — failure chance reduced by {reduction} %.",
        )
        self._reduction = reduction

    def apply_effect(self, data: dict) -> dict:
        data["training_failure_bonus"] = data.get("training_failure_bonus", 0) - self._reduction
        return data

class HotTopic(Condition):
    """Fan gains from races are increased by 20 %."""

    def __init__(self):
        super().__init__(
            "HotTopic",
            ConditionType.GOOD,
            "Everyone is talking about you — fan gains from races are boosted.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["fan_gain_multiplier"] = data.get("fan_gain_multiplier", 1.0) * 1.20
        return data

class ShiningBrightly(Condition):
    """Stat gains +15 % across all training."""

    def __init__(self):
        super().__init__(
            "ShiningBrightly",
            ConditionType.GOOD,
            "Shining at peak form — all stat gains increased.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["stat_gain_multiplier"] = data.get("stat_gain_multiplier", 1.0) * 1.15
        return data

class Sharpener(Condition):
    """Skill discount: skills cost 10 % fewer skill points."""

    def __init__(self):
        super().__init__(
            "Sharpener",
            ConditionType.GOOD,
            "Sharp as a tack — skill costs are reduced.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["skill_discount"] = data.get("skill_discount", 1.0) * 0.90
        return data

class NaturalTalent(Condition):
    """Primary stat gains +20 % and skill points +2."""

    def __init__(self):
        super().__init__(
            "NaturalTalent",
            ConditionType.GOOD,
            "Born for this — exceptional gains from every training session.",
        )

    def apply_effect(self, data: dict) -> dict:
        data["stat_gain_multiplier"] = data.get("stat_gain_multiplier", 1.0) * 1.20
        data["skill_point_bonus"]    = data.get("skill_point_bonus", 0) + 2
        return data

_CONDITION_REGISTRY: dict[str, Condition] = {
    # Bad
    "PracticePoor":       PracticePoor(),
    "Migraine":           Migraine(),
    "NightOwl":           NightOwl(),
    "DrySkin":            DrySkin(),
    "SlowMetabolism":     SlowMetabolism(),
    "Slacker":            Slacker(),
    "UnderTheWeather":    UnderTheWeather(),
    "NotReady":           NotReady(),
    "LackOfFocus":        LackOfFocus(),
    "Overtired":          Overtired(),
    # Good
    "Charming":           Charming(),
    "FastLearner":        FastLearner(),
    "PracticePerfect_○":  PracticePerfect("○"),
    "PracticePerfect_◎":  PracticePerfect("◎"),
    "HotTopic":           HotTopic(),
    "ShiningBrightly":    ShiningBrightly(),
    "Sharpener":          Sharpener(),
    "NaturalTalent":      NaturalTalent(),
}

def get_condition_by_name(name: str) -> Optional[Condition]:
    """Return the Condition instance for *name*, or None if unknown."""
    return _CONDITION_REGISTRY.get(name)

def apply_all_conditions(conditions: list[str], career_data: dict) -> dict:
    """Apply every active condition to *career_data* in order.

    Unknown condition names are silently skipped so old saves don't break.
    """
    for name in conditions:
        condition = _CONDITION_REGISTRY.get(name)
        if condition is not None:
            condition.apply_effect(career_data)
    return career_data
