from .constants import MAX_STATS
from ..skills import SKILLS

def get_rank_score(d):
    SKILL_PTS = sum([SKILLS[i].value for i in d.get("skills", [])])
    FANS = d.get("fans", 0)
    GRADE = sum(d["stats"])
    
    return GRADE + SKILL_PTS + FANS


def grade_stat(stat: int):
    stat = max(0, stat)

    if stat < 500:
        step = stat // 50
        ranks = [
            "G", "GP",
            "F", "FP",
            "E", "EP",
            "D", "DP",
            "C", "CP",
        ]
        return f"rank{ranks[step]}"

    if stat <= 600:
        return "rankB"

    if stat <= 650:
        return "rankB"

    if stat <= 700:
        return "rankBP"

    if stat < 800:
        return "rankA"

    if stat <= 900:
        return "rankAP"

    if stat <= 1000:
        return "rankS"

    if stat <= 1100:
        return "rankSP"

    if stat <= 1150:
        return "rankSS"

    if stat <= 1200:
        return "rankSSP"

    step = (stat - 1200) // 100
    
    if step == 0:
        return "rankUG"
    if step <= 9:
        return f"rankUG{step}"
    return f"rankUF{min(step - 9, 7)}"


def grade_score(score: int):
    score = max(0, score)

    if score < 3000:
        step = score // 500
        ranks = ["G", "G", "F", "F", "E", "E"]
        suf = "P" if step % 2 else ""
        return f"rank{ranks[step]}{suf}"

    if score < 7000:
        step = (score - 3000) // 1000
        ranks = ["D", "D", "C", "C"]
        suf = "P" if step % 2 else ""
        return f"rank{ranks[step]}{suf}"

    if score < 8200:
        return "rankB"

    if score < 10000:
        return "rankBP"

    if score < 12000:
        return "rankAP" if score >= 11000 else "rankA"

    if score < 14500:
        return "rankAP"
        
    if score < 17500:
        return "rankSP" if score >= 16000 else "rankS"

    if score < 20500:
        return "rankSSP" if score >= 19000 else "rankSS"

    step = (score - 20500) // 2000
    if step == 0:
        return "rankUG"
    if step <= 9:
        return f"rankUG{step}"
    return f"rankUF{min(step - 9, 7)}"
