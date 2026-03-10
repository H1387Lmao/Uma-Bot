from .constants import MAX_STATS
from ..skills import SKILLS

def get_rank_score(d):
    SKILL_PTS = sum([SKILLS[i].value for i in d.get("skills", [])])
    FANS = d.get("fans", 0)
    GRADE = sum(d["stats"])
    
    return GRADE + SKILL_PTS + FANS


def grade_stat(stat: int):
    stat = max(0, stat)
    
    # 0–499 (50-step)
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
    
    # 500–599
    if stat <= 600:
        return "rankB"
    
    # 600–649
    if stat <= 650:
        return "rankB"
    
    # 650–699
    if stat <= 700:
        return "rankBP"
    
    # 700–799
    if stat < 800:
        return "rankA"
    
    # 800–899
    if stat <= 900:
        return "rankAP"
    
    # 900–999
    if stat <= 1000:
        return "rankS"
    
    # 1000–1099
    if stat <= 1100:
        return "rankSP"
    
    # 1100–1149
    if stat <= 1150:
        return "rankSS"
    
    # 1150–1199
    if stat <= 1200:
        return "rankSSP"
    
    # 1200+ → Ultra
    step = (stat - 1200) // 100
    
    if step == 0:
        return "rankUG"
    if step <= 9:
        return f"rankUG{step}"
    return f"rankUF{min(step - 9, 7)}"


def grade_score(score: int):
    score = max(0, score)
    
    # 0–2999 (500)
    if score < 3000:
        step = score // 500
        ranks = ["G", "G", "F", "F", "E", "E"]
        suf = "P" if step % 2 else ""
        return f"rank{ranks[step]}{suf}"
    
    # 3000–6999 (1000)
    if score < 7000:
        step = (score - 3000) // 1000
        ranks = ["D", "D", "C", "C"]
        suf = "P" if step % 2 else ""
        return f"rank{ranks[step]}{suf}"
    
    # 7000–8199
    if score < 8200:
        return "rankB"
    
    # 8200–9999
    if score < 10000:
        return "rankBP"
    
    # 10000–11999 (A / AP)
    if score < 12000:
        return "rankAP" if score >= 11000 else "rankA"
    
    # 12000–14500 (A+)
    if score < 14500:
        return "rankAP"  # or "rankA+" if you want it explicit
    
    # 14501–17499 (S / SP)
    if score < 17500:
        return "rankSP" if score >= 16000 else "rankS"
    
    # 17500–20499 (SS / SSP)
    if score < 20500:
        return "rankSSP" if score >= 19000 else "rankSS"
    
    # 20500+ Ultra
    step = (score - 20500) // 2000
    if step == 0:
        return "rankUG"
    if step <= 9:
        return f"rankUG{step}"
    return f"rankUF{min(step - 9, 7)}"
