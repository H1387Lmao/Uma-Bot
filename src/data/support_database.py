from .models import SCData
from .constants import SCALING, GET_SCALER

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

SUPPORTS = {u.name: u for u in SC_DB}
SC_RARITIES = {"r": {}, "sr": {}, "ssr": {}}
SUPPORT_IDS = {u.img_id: u for u in SC_DB}

# Populate support rarities
[SC_RARITIES[v.rarity].setdefault(k, v) for k, v in SUPPORTS.items()]
