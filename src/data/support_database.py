from .models import SCData
from .constants import SCALING, GET_SCALER

SC_DB = [
    SCData(
      name="Fine Motion",
      id=28,
      rarity="R",
      stats=["wit"],
      race_bonus=0.15,
      fan_bonus=0.15,
      training_effectiveness=0.6,
      specialty_priority=0.2 
    ),
    SCData(
      name="El Condor Pasa",
      id=11,
      rarity="R",
      stats=["pwr"],
      race_bonus=0.5,
      fan_bonus=0.15,
      training_effectiveness=0,
      specialty_priority=0.35
    ),
    SCData(
      name="Tokai Teio",
      id=3,
      rarity="R",
      stats=["spd"],
      race_bonus=0,
      fan_bonus=0,
      training_effectiveness=0,
      specialty_priority=0.35
    ),
    SCData(
      name="T.M. Opera O",
      id=12,
      rarity="R",
      stats=["stm"],
      race_bonus=0.5,
      fan_bonus=0.15,
      training_effectiveness=0,
      specialty_priority=0.5
    ),
    SCData(
      name="Grass Wonder",
      id=9,
      rarity="R",
      stats=["gut"],
      race_bonus=0.15,
      fan_bonus=0.10,
      training_effectiveness=0,
      specialty_priority=0.5
    )
]

SUPPORTS = {u.name: u for u in SC_DB}
SC_RARITIES = {"r": {}, "sr": {}, "ssr": {}}
SUPPORT_IDS = {u.img_id: u for u in SC_DB}
SC_BY_STAT = {"spd":{}, "stm":{}, "pwr":{}, "gut":{}, "wit":{}}

[SC_RARITIES[v.rarity].setdefault(k, v) for k, v in SUPPORTS.items()]
[(SC_BY_STAT[stat].append(v) for stat in v.stats) for _, v in SUPPORTS.items()]
