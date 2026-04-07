from .goals import *
from ..data.uma_database import UMAS
from ..data.ranking import grade_score
from ..skills import SKILLS
from ..views.state import view_state

import random

stat_names = ['spd', 'stm', 'pwr', 'gut', 'wit', 'sp']

stat_to_index = {s: i for i, s in enumerate(stat_names[:-1])}

training_bonuses = {
    'spd': [('spd', 20), ('pwr', 10),          ('sp', 4), ('energy', -20)],
    'stm': [('stm', 20), ('gut', 10),          ('sp', 4), ('energy', -20)],
    'pwr': [('stm', 10), ('pwr', 20),          ('sp', 4), ('energy', -20)],
    'gut': [('spd', 5),  ('pwr', 5),           ('gut', 20),         ('sp', 4), ('energy', -35)],
    'wit': [('wit', 20), ('sp', 10), ('energy', 5)]
}

class Career:
    def __init__(
        self,
        owner: int,
        name: str,
        fans: int = 0,
        energy: int = 0,
        mood: int = 0,
        skill_points: int = 120,
        stats: list[int] = [0,0,0,0,0],
        skills: list[int] = [],
        conditions: set[int] = set(),
        races_scheduled: dict[int, RaceData] = {},
        support_cards: list[int] = [],
        goals_done: int = 0,
        turn: int = 0,
        seed: int = None,
        max_energy: int = 100,
        over: bool=False,
        has_bad: bool= False
    ):
        self.owner: int = owner
        self.name: str = name
        self.fans: int = fans
        self.energy: int = energy
        self.mood: int = mood
        self.stats: list[int] = stats
        self.conditions: set[int] = conditions
        self.races_scheduled: dict[int, RaceData] = races_scheduled
        self.turn: int = turn       
        self.support_cards: list[int] = support_cards
        self.goals_done: int = goals_done
        self.seed: int = seed

        self.skill_points: int = skill_points
        self.skills: list[int] = skills

        self.max_energy = max_energy

        self.goals: list[FanGoal|RaceGoal] = get_goals(name, UMAS[name])

        self.update_current_goal()
        self.update_aptitudes()

        self.over=over

        self.advance() if self.turn == 0 else self.calc_date()

        self.cache = {}
        self.has_bad=has_bad
    def __reduce__(self):
        return (self.__class__, (
            self.owner,
            self.name,
            self.fans,
            self.energy,
            self.mood,
            self.skill_points,
            self.stats,
            self.skills,
            self.conditions,
            self.races_scheduled,
            self.support_cards,
            self.goals_done,
            self.turn,
            self.seed,
            self.max_energy,
            self.over,
            self.has_bad
        ))
    def __repr__(self):
        return f"Career ({self.name})"

    def update_aptitudes(self):
        ud = UMAS[self.name]
        self.apts: dict[str, int] = ud.apts
    @staticmethod
    def create_new(name, uid, sps):
        uma_data = UMAS[name]
        return Career(uid, name, 1, 100, 2, 120, list(uma_data.stats), [], set(), {}, sps)
    def update_current_goal(self):
        for goal in self.goals[self.goals_done:]:
            if goal.deadline == self.turn:
                self.current_goal = goal
                return
        self.current_goal=None
    def stat_to_index(self, stat):
        return stat_to_index[stat]

    def rfc(self, id, current=0, offset=(0,1), fn=None):
        if id not in self.cache:
            deduction = random.randrange(*offset)
            new = current-deduction
            if fn is not None: new = fn(new)
            self.cache[id]=new
            return new
        else:
            return self.cache[id]

    def failed(self, deduct):
        new = self.energy+deduct
        r = new / self.max_energy

        if r >= 0.5: # base case
            return 0
        failure = -0.5 * (r**2) -1.5 * r + 1 # based on the wiki https://umamusu.me/failure_function.html
        return max(0, min(1, failure)) # clamp from 0-1

    def train(self, stat, is_preview=False):
        if stat is None:
            return

        base = {}
        for s, val in training_bonuses[stat]:
            base[s] = val

        result = {}

        acc_teff=0

        for s, value in base.items():
            if s == "energy":
                v = value
            elif s == "sp":
                v = value
            else:
                v = value

                for sc in self.support_cards:
                    if (sc._current_stat == stat\
                        and stat in sc.stats):
                        
                        v += sc.s_bonus
                        acc_teff+=sc.tr_eff
                        if sc.gauge > 80:
                            v *= (1 + sc.fr_bonus)

            if is_preview:
                if s != "sp":
                    v = self.rfc(stat + s, v, (-3, 4))
            else:
                v = self.rfc(stat + s, v, (-3, 4))

            result[s] = int(v)

        if is_preview:
            if "energy" in result:
                result["failure_rate"]  = self.failed(result["energy"])
                result["failure_rate"] -= acc_teff
            return result

        for s, v in result.items():
            if s in stat_to_index:
                self.stats[stat_to_index[s]] += v
            elif s == "energy":
                self.energy += v
                self.energy = min(self.max_energy, max(0, self.energy))
            elif s == "sp":
                self.skill_points += v

        self.advance()
    
    def advance(self):
        self.turn += 1

        self.calc_date()
        self.cache={}

        for sc in self.support_cards:
            sc.switch_lane()
    def calc_date(self):
        self.month = (self.turn//2 + 3)%12 # start in april
        self.half = (self.turn-1)%2
        self.year = (self.turn//2 + 3)//12
        
        self.update_current_goal()

    def is_summer(self):
        if not self.year: return False
        return 6 <= self.month <= 7

    def get_needed_goal(self):
        for goal in self.goals[self.goals_done:]:
            if goal.deadline >= self.turn:
                return goal

        self.over=True
    def get_avg(self):
        return sum(self.stats)//len(self.stats)
    def check_goal(self, goal_res):
        if self.current_goal is not None:
            gtype=goal_res["goal_type"]
            if gtype=="race":
                self.over=goal_res["placement"]>self.current_goal.placement
            elif gtype=="fans":
                self.over=self.fans<self.current_goal.requirement
        self.advance()
    def complete(self, prof):
        prof["career"]=None
        prof["stats"]["fans"]+=self.fans

        total_stats = sum(self.stats)
        skill_grades = sum(
            SKILLS[skid].value for skid in self.skills
        )
        grade = total_stats+skill_grades
        res = {
            "grade": grade,
            "stats": total_stats,
            "skills": self.skills,
            "name": self.name,
            "apts": self.apts,
            "rank": grade_score(grade)
        }
        return res
