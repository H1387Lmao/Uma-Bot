from .skills import *
from .views.state import view_state
MAX_STATS=1600

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

DEFAULT_ULT = Skill(
    "Ultimate Pass",
    "Gain insane velocity at the second half of the race, when in second place",
    0,
    (
        (
            "self",
            {
                "vel": 16
            }
        )
    ,),
    1,
    lambda v, race: v.order_rate>=50 and v.placement==2,
    type="Ult",
    icon="yellow_ult"
)

class SCData:
    def __init__(self, name, rarity, description, label=None, stat="SPD", id=1):
        self.name=name
        self.rarity=rarity
        self.description=description
        self.label=f"({label})" if label else ""
        self.stat = stat.lower()

        self.id=id
        self.img_id = len(self.rarity)*10000+self.id
    def display(self,bot):
        return f"{bot.em[self.stat.upper()]}{self.name} {self.label}"
    def get_id(self):
        return self.img_id
    def get_image(self):
        handle="https://gametora.com/images/umamusume/supports/support_card_s_"
        return handle+f"{self.get_id()}.png"

class UmaData:
    def __init__(self, name, rarity, stats, ult=DEFAULT_ULT, unobtainable=False):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.ult = ult
        self.unobtainable = unobtainable

        view_state.logger.print(f"[light cyan]Unreleased: [gold]{self.name}[reset]" ) if self.unobtainable else 0

DEF_STATS = (87,98,85,89,80)

SCALING={
    "r":(75,125,150,180,200),
    "sr":(35,50,75,90,125),
    "ssr":(6,7,13,20,25)
}

def GET_SCALER(level):
    return (level*0.35)+1

SC_DB = [
    SCData(
        "Special Week",
        "r",
        "Test Description",
        "Tracen Academy",
        "GUT",
        1
    )
]

UMA_DB = [
    UmaData("Haru Urara", "r", (75,47,62,115,52)),
    UmaData("Matikane Tannhauser", "r", (79,91,82,88,85), unobtainable=True),
    UmaData("Agnes Tachyon", "r", (93,132,83,79,134)),
    UmaData("Sakura Bakushin O", "r", DEF_STATS),
    UmaData("King Halo", "r", (93,63,89,77,94)),

    UmaData("Daiwa Scarlet", "sr", (84,77,79,95,90)),
    UmaData("Gold Ship", "sr", (82,96,100,77,70)),
    UmaData("Vodka", "sr", (96,61,105,75,88)),

    UmaData("Silence Suzuka", "ssr", (101,84,77,100,88)),
    UmaData("Kitasan Black", "ssr", (97,100,79,86,88), unobtainable=True),
    UmaData("Special Week", "ssr", (83,88,98,90,91)),
    UmaData("Curren Chan", "ssr", (97,58,109,91,97)),
    UmaData("Daitaku Helios", "ssr", (100,89,97,87,77), unobtainable=True),
    UmaData("Still In Love", "ssr", (91,89,97,90,83), unobtainable=True),
    UmaData("Oguri Cap", "ssr", (101, 66, 106, 84, 93)),
    UmaData("Tokai Teio", "ssr", (90, 89, 83, 92, 96)),
    UmaData("TM Opera O", "ssr", DEF_STATS),
    UmaData("Air Groove", "ssr", DEF_STATS),
    UmaData("Mejiro McQueen", "ssr", (71,111,71,103,94)),
    UmaData("Loves Only You", "ssr",(88,82,103,80,97), Skill(
        "Our Love Language",
        "Loves Only You gains increased stats at the start",
        0,
        (
            (
                "self",
                {
                    "spd": 150,
                    "stm": 350,
                    "gut": 145
                }
            ),
        ),
        1,
        None,
        type="Ult",
        icon="yellow_ult"
    ), unobtainable=True), 
    UmaData("Tamamo Cross", "ssr", (83,95,105,83,84), Skill(
        "Fast as Lightning!",
        "Tamamo Cross gains velocity at the start",
        0,
        (
            (
                "self",
                {
                    "vel":20
                }
            ),
        ),
        1,
        None,
        type="Ult",
        icon="yellow_ult"
    )),
    UmaData("Sweep Tosho", "ssr", (101, 85, 110, 65, 89), Skill(
        "Victory belongs to me — Strelitzia! ☆",
        "If positioned toward the back until the start of the final corner, when there are 300m remaining, cast a magic spell to increase velocity continuously.",
        0,
        (
            (
                "self",
                {
                    "vel": 20
                }
            ),
        ),
        1,
        lambda owner, race: (race.track_length-owner.pos)<=300,
        type="Ult",
        icon="yellow_ult"
    )),
    UmaData("Almond Eye", "ssr", (
        104, 83, 83, 91, 89
    ), PEERLESS_HEROINE, unobtainable=True),
    UmaData("Manhattan Cafe", "ssr", (
        83, 98, 94, 86, 89
    ), MC_ULT, unobtainable=True),
    UmaData("Aston Machan", "ssr", (
        99, 73, 97, 98, 83
    ),
        Skill(
            "Silent Letter",
            "With less than 400 meters remaining, if you're in the front and someone is about to overtake you, your speed and acceleration will increase",
            0,
            (
                (
                    "self", {
                        "vel": 50,
                        "accel": 250
                    }
                ),
            ),
            1,
            lambda owner, race: race.track_length - owner.pos <= 400,
            "Ult",
            "yellow_ult"
    ), unobtainable=True)
]

UMAS = {u.name: u for u in UMA_DB}
SUPPORTS = {u.name: u for u in SC_DB}

UMA_RARITIES = {"r":{},"sr":{},"ssr":{}}
SC_RARITIES = {"r":{},"sr":{},"ssr":{}}

SUPPORT_IDS = {u.img_id: u for u in SC_DB}

SAFE_TO_REAL = {
    u.name.replace(" ", "_").lower(): u.name
    for u in UMA_DB
}

[UMA_RARITIES[v.rarity].setdefault(k, v) for k,v in UMAS.items() if not v.unobtainable]
[SC_RARITIES[v.rarity].setdefault(k, v) for k,v in SUPPORTS.items()]

