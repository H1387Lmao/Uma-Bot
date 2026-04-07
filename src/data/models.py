from .constants import DEFAULT_STATS
from ..skills import Skill
from enum import IntEnum
"""
all aptitude grades
"""

class Grade(IntEnum):
    G = 0
    F = 1
    E = 2
    D = 3
    C = 4
    B = 5
    A = 6
    S = 7

G = Grade.G
F = Grade.F
E = Grade.E
D = Grade.D
C = Grade.C
B = Grade.B
A = Grade.A
S = Grade.S

grade_map = {
    G: 'G',
    F: 'F',
    E: 'E',
    D: 'D',
    C: 'C',
    B: 'B',
    A: 'A',
    S: 'S'
}

PRE_OP = 0
OP = 1
G3 = 3
G2 = 4
G1 = 5

distances_apt = ["sprint", "mile", "medium", "long"]

distances = [
    ('sprint', 1400),
    ('mile', 1800),
    ('medium', 2400)
]

"""
every model
"""

class SCData:
    def __init__(
        self,
        name,
        id=1,
        rarity="R", 
        stats=["spd"],

        # benefits
        race_bonus=0,
        fan_bonus=0,
        training_effectiveness=0,
        specialty_priority=0
    ):
        self.name = name
        self.rarity = rarity.lower()
        self.stats = list(map(str.lower, stats))
        self.id = id

        self.r_bonus=race_bonus
        self.f_bonus=fan_bonus
        self.tr_eff =training_effectiveness
        self.s_prio =specialty_priority
        self.img_id = len(self.rarity) * 10000 + self.id

        self._emoji=f"sc_{self.img_id}"
    def display(self, bot):
        return f"{bot.get_em(self.stat.upper())}{self.name}"

    def get_emoji(self, bot):
        return bot.get_em(self._emoji)
        
    def get_id(self):
        return self.img_id
    
    def get_image(self):
        handle = "https://gametora.com/images/umamusume/supports/support_card_s_"
        return handle + f"{self.get_id()}.png"

class UmaData:
    def __init__(
        self, 
        name, 
        rarity, 
        stats, 
        aptitude=[
            G,
            G,
            G,
            G,
            G,
            G,
            G,
            G,
            G,
            G
        ], 
        skill=None
    ):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.ult = skill
        self.aptitude = aptitude

        self.best_distance_aptitude = distances_apt[sorted(enumerate(aptitude[6:10]), key=lambda d: d[1])[-1][0]]

        print(self.best_distance_aptitude, stats)
        for dist, threshold in distances:
            if dist == self.best_distance_aptitude:
                self.best_dist = threshold
                break
        else:
            self.best_dist = 2600

        self.apts: dict[str, int] = {
            "turf": self.get_turf_apt(),
            "dirt": self.get_dirt_apt(),
            "mile": self.get_mile_apt(),
            "medium": self.get_medium_apt(),
            "sprint": self.get_sprint_apt(),
            "long": self.get_long_apt(),
            "front": self.get_front_apt(),
            "pace": self.get_pace_apt(),
            "end": self.get_end_apt(),
            "late": self.get_late_apt()
        }
                
    def get_turf_apt(self):
        return self.aptitude[0]
    def get_dirt_apt(self):
        return self.aptitude[1]
    def get_front_apt(self):
        return self.aptitude[2]
    def get_pace_apt(self):
        return self.aptitude[3]
    def get_late_apt(self):
        return self.aptitude[4]
    def get_end_apt(self):
        return self.aptitude[5]
    def get_sprint_apt(self):
        return self.aptitude[6]
    def get_mile_apt(self):
        return self.aptitude[7]
    def get_medium_apt(self):
        return self.aptitude[8]
    def get_long_apt(self):
        return self.aptitude[9]

def GRADE_ICON(grade):
    match grade:
        case 0:
            return "grade_debut"
        case 1:
            return "grade_maiden"
        case 3:
            return "grade_g3"
        case 4:
            return "grade_g2"
        case 5:
            return "grade_g1"


class RaceData:
    def __init__(self, race_name, name, distance=2000, grade=0, turf=True):
        self.distance_meters = distance

        for dist, threshold in distances:
            if threshold <= distance:
                self.distance = dist
                break
        else:
            self.distance = 'long'
        
        self.name = name
        self.race_name = race_name or name

        self.grade = grade
        self.turf = turf

        self.turn = 0

    def get_emoji(self, view_state):
        return view_state.bot.get_em(GRADE_ICON(self.grade))

    def evaluate_distance(self, aptitudes):
        return aptitudes[self.distance]>=A
    def evaluate_ground(self, aptitudes):
        return aptitudes['turf' if self.turf else 'dirt']>=A

    def display(self, separator='\n'):
        return f"{self.get_emoji() or ''} {self.name}{separator}{self.race_name} {self.distance}m"

class SupportCard:
    def __init__(self, data, cs=None, gauge=0):
        self.name = data.name
        self.rarity = data.rarity
        self.stats = data.stats
        self.id = data.id

        self.r_bonus=data.r_bonus
        self.f_bonus=data.f_bonus
        self.tr_eff =data.tr_eff
        self.s_prio =data.s_prio
        self.img_id =data.img_id
        self.data=data

        self._current_stat=cs or self.switch_lane()
        self.gauge=gauge
    def switch_lane(self):
        if self.s_prio>random.random():
            self._current_stat = random.choices(
                self.stats
            )
        else:
            self._current_stat = random.choices(
                ["spd", "stm", "pwr", "gut", "wit"]
            )
    def __reduce__(self):
        return (self.__class__, (
            self.data,
            self._current_stat,
            self.gauge
        ))

