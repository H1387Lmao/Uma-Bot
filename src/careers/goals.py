from __future__ import annotations

from typing import Optional

def debut_goal() -> dict:
    return {
        "type":        "debut",
        "desc_key":    "goal.debut",
        "repeatable":  False,
        "completed":   False,
        "month":       6,
        "half":        "late",
        "year":        1,
    }

def fan_goal(target_fans: int, month: int, half: str, year: int) -> dict:
    return {
        "type":        "fans",
        "desc_key":    "goal.fans",
        "desc_args":   [target_fans],
        "repeatable":  False,
        "target_fans": target_fans,
        "month":       month,
        "half":        half,
        "year":        year,
        "completed":   False,
    }

def placement_goal(race_name: str, requirement: str, month: int, half: str, year: int) -> dict:
    valid = {"participate", "top5", "top3", "win"}
    if requirement not in valid:
        raise ValueError(f"requirement must be one of {valid}, got {requirement!r}")
    return {
        "type":        "placement",
        "desc_key":    f"goal.req.{requirement}",
        "desc_args":   [race_name],
        "repeatable":  False,
        "race_name":   race_name,
        "requirement": requirement,
        "month":       month,
        "half":        half,
        "year":        year,
        "completed":   False,
    }

def goal_description(goal: dict, prof_or_lang: dict | str = "English") -> str:
    from ..views.translations import tr
    key = goal.get("desc_key", "")
    args = goal.get("desc_args", [])
    return tr(key, 0, prof_or_lang, *args)

def get_turns_until_goal(goal: dict, current_month: int, current_half: str, current_year: int) -> int:
    """Calculate turns remaining until the goal's deadline."""
    target_month = goal.get("month", 12)
    target_half = goal.get("half", "late")
    target_year = goal.get("year", 3)
    
    current_total_half = (current_year - 1) * 24 + (current_month - 1) * 2 + (0 if current_half == "early" else 1)
    target_total_half = (target_year - 1) * 24 + (target_month - 1) * 2 + (0 if target_half == "early" else 1)
    
    return max(0, target_total_half - current_total_half)

_REQUIREMENT_THRESHOLD: dict[str, int] = {
    "participate": 99,   # any placement counts
    "top5":        5,
    "top3":        3,
    "win":         1,
}

def _is_debut_won(races_run: list[dict]) -> bool:
    """Return True if any Debut Race was won."""
    for record in races_run:
        if record.get("race_name") == "Debut Race":
            return record.get("placement", 99) == 1
    return False

def _check_single_goal(goal: dict, career_data: dict) -> bool:
    """Return True if *goal* is satisfied given *career_data*."""
    gtype = goal.get("type")

    if gtype == "debut":
        return _is_debut_won(career_data.get("races_run", []))

    if gtype == "fans":
        target = goal.get("target_fans", 0)
        return career_data.get("fans", 0) >= target

    if gtype == "placement":
        race_name   = goal.get("race_name", "")
        requirement = goal.get("requirement", "participate")
        threshold   = _REQUIREMENT_THRESHOLD.get(requirement, 99)

        for record in career_data.get("races_run", []):
            if record.get("race_name") == race_name:
                if record.get("placement", 99) <= threshold:
                    return True
        return False

    return False

def check_goals(career_data: dict) -> int:
    """Check all goals and mark newly completed ones.

    Mutates *career_data* in place:
    - Sets ``goal["completed"] = True`` for newly met goals.
    - Increments ``career_data["goals_completed"]``.

    Returns the number of goals newly completed this call.
    """
    newly_completed = 0

    for goal in career_data.get("goals", []):
        if goal.get("completed"):
            continue  # already done, skip

        if _check_single_goal(goal, career_data):
            goal["completed"] = True
            newly_completed  += 1

    career_data["goals_completed"] = (
        career_data.get("goals_completed", 0) + newly_completed
    )
    return newly_completed

def get_goal_progress(goal: dict, career_data: dict) -> float:
    """Return completion progress as a percentage (0–100).

    For display purposes only; does not mutate anything.
    """
    if goal.get("completed"):
        return 100.0

    gtype = goal.get("type")

    if gtype == "debut":
        return 100.0 if _is_debut_won(career_data.get("races_run", [])) else 0.0

    if gtype == "fans":
        target = goal.get("target_fans", 1)
        if target <= 0:
            return 100.0
        current = career_data.get("fans", 0)
        return min(100.0, (current / target) * 100.0)

    if gtype == "placement":
        race_name   = goal.get("race_name", "")
        requirement = goal.get("requirement", "participate")
        threshold   = _REQUIREMENT_THRESHOLD.get(requirement, 99)

        for record in career_data.get("races_run", []):
            if record.get("race_name") == race_name:
                if record.get("placement", 99) <= threshold:
                    return 100.0
                else:
                    return 50.0
        return 0.0

    return 0.0
