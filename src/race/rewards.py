import random
import traceback


def give_career_rewards(bot, career, owner, winners: list) -> tuple[bool, dict]:
    won = bool(winners) and winners[0].is_player
    if not won:
        return False, {}
    try:
        fans   = random.randrange(50,  1000)
        sp     = random.randrange(30,  70)
        carats = random.randrange(50,  100)

        f_bonus = 1
        r_bonus = 1

        for sc in career.support_cards:
            f_bonus*=(1+sc.f_bonus)
            r_bonus*=(1+sc.r_bonus)
        
        career.fans        += int(fans*f_bonus)
        career.skill_points += sp

        race_bonus=5 if not won else 15

        for i in range(5):
            career.stats[i]+=int(race_bonus*r_bonus)
        
        bot.database[str(owner.id)]["stats"]["carats"] += carats
        return True, {"fans": fans, "sp": sp, "carats": carats}
    except Exception:
        traceback.print_exc()
        return True, {}


def give_daily_rewards(bot, owner, winners: list) -> tuple[bool, dict]:
    won = bool(winners) and winners[0].is_player
    if not won:
        return False, {}
    try:
        carats = random.randrange(400, 1000)
        exp    = random.randrange(500, 1000)
        prof            = bot.database[str(owner.id)]["stats"]
        prof["carats"] += carats
        prof["exp"]    += exp
        prof["level"]   = prof["exp"] // 10000
        return True, {"carats": carats, "exp": exp}
    except Exception:
        traceback.print_exc()
        return True, {}


def give_club_rewards(winners: list) -> list[dict]:
    return [
        {"uma": w, "place": w.placement - 1, "career": w.career}
        for w in winners
    ]
