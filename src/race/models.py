import random
from collections import deque
from ..data import *
from ..skills import *
from ..views.state import view_state

NUM_LANES           = 3
GUTS_OVERTAKE_COST  = 25
GUTS_DEFEND_COST    = 15
GUTS_BLOCK_COST     = 20
GUTS_RESIST_COST    = 10
GUTS_FAIL_PENALTY   = 0.92
POWER_FAIL_PENALTY  = 0.95
BLOCK_PENALTY       = 0.60
BLOCK_RANGE         = 40
RANKING_EMOJIS      = [":first_place:", ":second_place:", ":third_place:", ":medal:"]

WEATHER_OPTIONS = ["Sunny", "Cloudy", "Rainy", "Snow"]
SEASON_OPTIONS  = ["Spring", "Summer", "Fall", "Winter"]
TIME_OPTIONS    = ["Morning", "Noon", "Evening", "Night"]

GRADE_BONUS = {0: 0.0, 1: 0.05, 3: 0.15, 4: 0.25, 5: 0.40}
ORDINAL     = {1: "st", 2: "nd", 3: "rd"}


def get_tick(speed: float) -> float:
    if speed <= 800:
        return 22 - (22 - 14) * (speed / 800)
    return 14 - (14 - 7) * ((speed - 800) / 800)


def random_skills(atleast: int = 3) -> list:
    return random.sample(SKILLS, k=min(atleast, len(SKILLS)))


def _distance_apt_key(meters: int) -> str:
    if meters <= 1400:
        return "sprint"
    if meters <= 1800:
        return "mile"
    if meters <= 2200:
        return "medium"
    return "long"


def _apt_factor(value: int) -> float:
    if value >= 6:
        return 1.0
    if value >= 4:
        return 0.9
    if value >= 2:
        return 0.75
    return 0.60


class RaceUma:
    def __init__(
        self,
        name:      str,
        stats:     tuple,
        emoji,
        is_player: bool = False,
        owner           = None,
        career          = None,
        club_uma:  bool = False,
        skills:    list = [],
        race            = None,
    ):
        self.name        = name
        self.stats       = stats
        self.emoji       = emoji
        self.is_player   = is_player
        self.owner       = owner
        self.career      = career
        self.club_uma    = club_uma
        self.race        = race

        self.ACCEL_RATE  = 12
        self.pos         = 0.0
        self.finished    = False
        self.gain        = 0.0
        self.late_start  = False
        self.placement   = 67
        self.vel         = 0.0
        self.lane        = 0
        self.effects     = deque(maxlen=5)
        self.late_chance = 1

        ult = UMAS[name].ult

        self.skills    = list(skills)
        if ult:
            self.skills.insert(0, ult)
        
        self.skilluses = {a.name: a.uses for a in self.skills if a}

        self.spd, self.stm, self.pwr, self.guts, self.wit = self.stats

        for skill in self.skills:
            if skill.uses == "passive":
                skill.activate(self, None)

        self.vel = self._init_vel()

    def __repr__(self) -> str:
        if self.club_uma:
            return f"{self.owner.mention}'s {self.name}"
        return self.name

    def _aptitude_multiplier(self) -> float:
        apts        = UMAS[self.name].apts
        race_data   = self.race.race_data
        dist_f      = _apt_factor(apts.get(_distance_apt_key(race_data.distance_meters), 7))
        surface_f   = _apt_factor(apts.get("turf" if race_data.turf else "dirt", 7))
        return dist_f * surface_f

    def _init_vel(self) -> float:
        ticks  = get_tick(self.spd)
        norm   = min(max(self.wit / 1600, 0), 1)
        chance = 0.35 * (1 - norm) ** 1.2 * self.late_chance
        self.late_start = True
        if random.random() < chance:
            ticks += 2 * (1 - norm) ** 0.8
            self.effects.append("Late Start")
        return (self.race.race_data.distance_meters / ticks) * self._aptitude_multiplier()

    def display_effects(self) -> str:
        return "".join(EFFECTS[a] for a in self.effects)

    def activate_skills(self, race) -> None:
        self.race = race
        for skill in self.skills:
            if skill.can_trigger(self, race):
                skill.activate(self, race)

    @property
    def order_rate(self) -> int:
        return round(self.race.race_data.distance_meters / max(self.pos, 1) * 100)

    @property
    def group_rate(self) -> int:
        runners = len(self.race.runners)
        return round(runners / max(1, runners - self.placement) * 100)


class Race:
    def __init__(
        self,
        career,
        race_data,
        owner       = None,
        club_race:  bool = False,
        racers:     list = [],
        IS_DAILY:   bool = False,
    ):
        self.bot       = view_state.bot
        self.career    = career
        self.race_data = race_data
        self.owner     = owner
        self.club_race = club_race
        self.IS_DAILY  = IS_DAILY
        self.turn      = 0
        self.finished  = False
        self.runners:  list[RaceUma] = []
        self.winners:  list[RaceUma] = []
        self.event_queue             = deque(maxlen=10)

        self.weather = random.choice(WEATHER_OPTIONS)
        self.season  = random.choice(SEASON_OPTIONS)
        self.time    = random.choice(TIME_OPTIONS)

        self._init_runners(racers)
        self._assign_lanes()

    def _opponent_difficulty(self) -> float:
        turn_factor = 0.2 + (self.career.turn / 66) * 0.6
        return turn_factor + GRADE_BONUS.get(self.race_data.grade, 0.15)

    def _init_runners(self, racers: list) -> None:
        if not self.club_race:
            size        = random.randint(6, 10)
            pool        = [u for u in UMA_DB if u.name != self.career.name]
            random.shuffle(pool)
            difficulty  = self._opponent_difficulty()
            skill_count = int(self.career.get_avg() / 1600 * 12)
            for u in pool[:size - 1]:
                scaled = tuple(int(s * difficulty) for s in u.stats)
                self.runners.append(
                    RaceUma(u.name, scaled, self.bot.get_uma(u.name),
                            False, None, None, None,
                            skills=random_skills(skill_count), race=self)
                )
        else:
            for c_owner, ccareer in racers:
                self.runners.append(RaceUma(
                    ccareer.name,
                    ccareer.stats,
                    self.bot.get_uma(ccareer.name),
                    True, c_owner, ccareer, True,
                    [self._resolve_skill(s) for s in ccareer.skills],
                    race=self,
                ))

        self.runners.append(RaceUma(
            self.career.name,
            self.career.stats,
            self.bot.get_uma(self.career.name),
            True, self.owner, self.career, self.club_race,
            [self._resolve_skill(s) for s in self.career.skills],
            race=self,
        ))

        for i, u in enumerate(self.runners):
            u.gate_placement = i

    def _assign_lanes(self) -> None:
        for i, u in enumerate(self.runners):
            u.lane = i % NUM_LANES

    @staticmethod
    def _resolve_skill(skill):
        return SKILLS[skill] if isinstance(skill, int) else skill

    def push_event(self, text: str) -> None:
        self.event_queue.append({"text": text, "ttl": len(self.event_queue) + 3})

    def tick_events(self) -> None:
        for ev in list(self.event_queue):
            ev["ttl"] -= 1
            if ev["ttl"] <= 0:
                self.event_queue.remove(ev)

    def standings(self) -> list[RaceUma]:
        return sorted(self.runners, key=lambda u: u.pos, reverse=True)

    def get_ahead(self,  placement: int) -> list[RaceUma]: return self.standings()[placement + 1:]
    def get_behind(self, placement: int) -> list[RaceUma]: return self.standings()[:placement]
    def get_near(self, placement: int, radius: int) -> list[RaceUma]:
        s = self.standings()
        return s[max(0, placement - radius): min(len(self.runners), placement + radius)]
    def get_others(self, racer: RaceUma) -> list[RaceUma]:
        return [r for r in self.runners if r is not racer]

    @property
    def career_placement(self) -> int:
        player = next((u for u in self.runners if u.is_player), None)
        if not player:
            return -1
        return self.standings().index(player) + 1

    @property
    def race_em(self) -> str:
        em = self.bot.em
        return (
            str(em.get("time_"     + self.time.lower(),    ""))
            + str(em.get("weather_" + self.weather.lower(), ""))
            + str(em.get(self.season.lower(),               ""))
        )
