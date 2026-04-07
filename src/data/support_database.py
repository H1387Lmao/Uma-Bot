from .models import SCData
from .constants import SCALING, GET_SCALER

SC_DB = [
    SCData(
      name="Fine Motion",
      id=28,
      rarity="R",
      stats=["wit"],
      race_bonus=0.05,
      fan_bonus=0.1,
      training_effectiveness=0.6,
      specialty_priority=0.2,
      stat_bonus=5,
      friendship_bonus=0.1
    ),
    SCData(
      name="El Condor Pasa",
      id=11,
      rarity="R",
      stats=["pwr"],
      race_bonus=0.05,
      fan_bonus=0.1,
      training_effectiveness=0,
      specialty_priority=0.20,
      stat_bonus=5,
      friendship_bonus=0.1,
      initial_gauge=15
    ),
    SCData(
      name="Tokai Teio",
      id=3,
      rarity="R",
      stats=["spd"],
      race_bonus=0,
      fan_bonus=0,
      training_effectiveness=0,
      specialty_priority=0.20,
      stat_bonus=5,
      friendship_bonus=0.1,
      initial_gauge=15
    ),
    SCData(
      name="T.M. Opera O",
      id=12,
      rarity="R",
      stats=["stm"],
      race_bonus=0,
      fan_bonus=0.10,
      training_effectiveness=0,
      specialty_priority=0.20,
      stat_bonus=5,
      friendship_bonus=0.1,
      initial_gauge=15
    ),
    SCData(
      name="Grass Wonder",
      id=9,
      rarity="R",
      stats=["gut"],
      race_bonus=0.01,
      fan_bonus=0.05,
      training_effectiveness=0,
      specialty_priority=0.20,
      stat_bonus=5,
      friendship_bonus=0.15,
      initial_gauge=15
    )
]

SUPPORTS = {u.name: u for u in SC_DB}
SC_RARITIES = {"r": {}, "sr": {}, "ssr": {}}
SUPPORT_IDS = {u.img_id: u for u in SC_DB}
SC_BY_STAT = {"spd":[], "stm":[], "pwr":[], "gut":[], "wit":[]}


[SC_RARITIES[v.rarity].setdefault(k, v) for k, v in SUPPORTS.items()]

for sc in SC_DB:
  for stat in sc.stats:
    SC_BY_STAT[stat].append(sc)
