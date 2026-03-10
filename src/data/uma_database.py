from .models import UmaData
from .constants import DEFAULT_STATS
from .skill_database import *
from ..views.state import view_state

UMA_DB = [
    UmaData("Haru Urara", "r", (75, 47, 62, 115, 52), False),
    UmaData("Matikane Tannhauser", "r", (79, 91, 82, 88, 85)),
    UmaData("Agnes Tachyon", "r", (93, 132, 83, 79, 134), False),
    UmaData("Sakura Bakushin O", "r", DEFAULT_STATS),
    UmaData("King Halo", "r", (93, 63, 89, 77, 94)),
    
    UmaData("Daiwa Scarlet", "sr", (84, 77, 79, 95, 90)),
    UmaData("Gold Ship", "sr", (82, 96, 100, 77, 70)),
    UmaData("Vodka", "sr", (96, 61, 105, 75, 88), False),
    
    UmaData("Silence Suzuka", "ssr", (101, 84, 77, 100, 88), False),
    UmaData("Kitasan Black", "ssr", (97, 100, 79, 86, 88)),
    UmaData("Special Week", "ssr", (83, 88, 98, 90, 91), False),
    UmaData("Curren Chan", "ssr", (97, 58, 109, 91, 97)),
    UmaData("Daitaku Helios", "ssr", (100, 89, 97, 87, 77)),
    UmaData("Still In Love", "ssr", (91, 89, 97, 90, 83)),
    UmaData("Oguri Cap", "ssr", (101, 66, 106, 84, 93)),
    UmaData("Tokai Teio", "ssr", (90, 89, 83, 92, 96)),
    UmaData("TM Opera O", "ssr", DEFAULT_STATS),
    UmaData("Air Groove", "ssr", DEFAULT_STATS),
    UmaData("Mejiro McQueen", "ssr", (71, 111, 71, 103, 94)),
    UmaData("Loves Only You", "ssr", (88, 82, 103, 80, 97), skill=Skill(
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
    )),
    UmaData("Tamamo Cross", "ssr", (83, 95, 105, 83, 84), skill=Skill(
        "Fast as Lightning!",
        "Tamamo Cross gains velocity at the start",
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
        None,
        type="Ult",
        icon="yellow_ult"
    )),
    UmaData("Sweep Tosho", "ssr", (101, 85, 110, 65, 89), skill=Skill(
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
        lambda owner, race: (race.track_length - owner.pos) <= 300,
        type="Ult",
        icon="yellow_ult"
    )),
    UmaData("Almond Eye", "ssr", (104, 83, 83, 91, 89), skill=PEERLESS_HEROINE),
    UmaData("Manhattan Cafe", "ssr", (83, 98, 94, 86, 89), skill=MC_ULT),
    UmaData("Aston Machan", "ssr", (99, 73, 97, 98, 83),
            skill=Skill(
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
            ))
]

UMAS = {u.name: u for u in UMA_DB}
UMA_RARITIES = {"r": {}, "sr": {}, "ssr": {}}
SAFE_TO_REAL = {
    u.name.replace(" ", "_").lower(): u.name
    for u in UMA_DB
}

# Populate uma rarities (excluding unobtainable)
for k, v in UMAS.items():
    if not v.unobtainable:
        UMA_RARITIES[v.rarity].setdefault(k, v)

# Log unreleased uma
for uma in UMA_DB:
    if uma.unobtainable:
        view_state.logger.print(f"[light cyan]Unreleased: [gold]{uma.name}[reset]")
