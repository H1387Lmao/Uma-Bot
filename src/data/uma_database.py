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
    UmaData("Mejiro McQueen", "ssr", (71, 111, 71, 103, 94), [
        A, E, B, A, D, F, G, F, A, A
    ]),
    UmaData("Curren Chan", "ssr", (97, 58, 107, 91, 97),[
        A, F, B, A, E, G, A, D, G, G
    ]),
    UmaData("Sakura Bakushin O", "r", (87, 54, 93, 85, 81), [
        A, G, A, A, F, G, A, B, G, G
    ]),
    UmaData("King Halo", "r", (87, 60, 93, 83, 87), [
        A, G, G, B, A, D, A, B, B, C
    ]),
    UmaData("Grass Wonder", "sr", (91, 70, 99, 74, 91), [
        A, G, F, A, A, F, G, A, B, A
    ]),
    UmaData("TM Opera O", "ssr", (75, 108, 75, 102, 90), [
        A, E, C, A, A, G, G, E, A, A
    ]),
    UmaData("Rice Shower", "ssr", (71, 117, 70, 102, 90), [
        A, G, B, A, C, G, E, C, A, A
    ]),
    UmaData("Winning Ticket", "r", (87, 68, 91, 74, 80), [
        A, G, G, B, A, G, G, F, A, B
    ]),
    UmaData("Manhattan Cafe", "ssr", (83, 98, 94, 86, 89), [
        A, G, G, C, A, C, G, F, B, A
    ]),
    UmaData("Agnes Digital", "ssr", (85, 91, 83, 100, 91), [
        A, A, G, A, A, B, F, A, A, G
    ]),
    UmaData("Smart Falcon", "ssr", (94, 85, 85, 100, 86), [
        E, A, A, D, G, G, B, A, A, E
    ]),
    UmaData("Nice Nature", "r", (86, 72, 89, 69, 84), [
        A, G, F, B, A, D, G, C, A, A
    ]),
    UmaData("Matikane Tannhauser", "sr", (79, 91, 82, 88, 85), [
        A, G, F, A, A, E, G, D, A, A
    ]),
    UmaData("Matikane Fukukitaru", "r", (77, 81, 88, 81, 73), [
        A, F, G, B, A, F, F, C, A, A
    ]),
    UmaData("Daiwa Scarlet", "sr", (84, 77, 79, 95, 90), [
        A, G, A, A, E, G, F, A, A, B
    ])
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

