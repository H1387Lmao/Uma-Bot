from .models import UmaData, A, B, C, D, E, F, G
from .constants import DEFAULT_STATS
from .skill_database import *
from ..views.state import view_state

UMA_DB = [
    UmaData("Haru Urara", "r", (75, 47, 62, 115, 52), [
        G, A, G, G, A, B, A, B, G, G
    ]),
    UmaData("Agnes Tachyon", "r", (93, 132, 83, 79, 134), [
        A, G, E, A, B, F, G, D, A, B
    ]),
    
    UmaData("Vodka", "sr", (96, 61, 105, 75, 88), [
        A, G, C, B, A, F, F, A, A, F
    ]),
    
    UmaData("Silence Suzuka", "ssr", (101, 84, 77, 100, 88), [
        A, G, A, C, E, G, D, A, A, E
    ]),
    UmaData("Special Week", "ssr", (83, 88, 98, 90, 91), [
        A, G, G, A, A, C, F, C, A, A
    ]),
]

UMAS = {u.name: u for u in UMA_DB}
UMA_RARITIES = {"r": {}, "sr": {}, "ssr": {}}
SAFE_TO_REAL = {
    u.name.replace(" ", "_").lower(): u.name
    for u in UMA_DB
}

# Populate uma rarities (excluding unobtainable)
for k, v in UMAS.items():
    if not v._u:
        UMA_RARITIES[v.rarity].setdefault(k, v)

