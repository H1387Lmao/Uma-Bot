from ..data import SCHEDULES, races_by_turn_name, RaceData
from .goal_parser import parse_goals
import random

_turn = lambda deadline: deadline[0]*2+deadline[1] if isinstance(deadline, list) else deadline

class RaceGoal:
    def __init__(self, placement=0, data=None, by_turn=[0,0]):
        self.placement = placement
        self.turn = _turn(by_turn)
        if not isinstance(data, str):
            self.race_data = data
        else:
            turn_data = races_by_turn_name[self.turn]
            if data.strip() not in turn_data:
                raise ValueError(f"Thats not in this turn??\n{self.turn}, {repr(data)}")
            self.race_data = turn_data[data.strip()]
        self.deadline = by_turn
        self.goal_type = "race"
    def __repr__(self):
        return f"Get atleast place {self.placement} in {self.race_data.name} before turn {_turn(self.deadline)}"

class GradeGoal:
    def __init__(self, race_grade=1, placement=99, count=1, by_turn):
        self.placement  = placement
        self.count      = count
        self.race_grade = race_grade
        self.deadline   = by_turn
        self.goal_type  = "grade"
    def __repr__(self):
        return f"Place {self.placement}th in {self.count} Race Grade {self.race_grade}"

class FanGoal:
    def __init__(self, required_fans=0, by_turn=[0,0]):
        self.requirement = required_fans
        self.deadline = by_turn
        self.goal_type = "fans"
    def __repr__(self):
        return f"Acquire {self.requirement} fans before turn {_turn(self.deadline)}"


GOAL_DB = {
	'Haru Urara': [
		FanGoal(5000, 36),
		FanGoal(9000, 44),
		FanGoal(12000, 47),
		RaceGoal(5, 'Negishi Stakes', 49),
		RaceGoal(5, 'February Stakes', 51),
		RaceGoal(5, 'Elm Stakes', 62),
		RaceGoal(5, 'JBC Sprint', 68),
		RaceGoal(99, 'Arima Kinen', 71)
	],
	'Agnes Tachyon': [
	    RaceGoal(5, 'Yayoi Sho', 28),
	    RaceGoal(5, 'Satsuki Sho', 30),
	    RaceGoal(5, 'Tokyo Yushun', 33),
	    RaceGoal(3, 'Kikuka Sho', 43),
	    RaceGoal(1, 'Osaka Hai', 53),
	    RaceGoal(3, 'Takarazuka Kinen', 59),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 67),
	    RaceGoal(1, 'Arima Kinen', 71)
	],
	'Vodka': [
	    RaceGoal(99, 'Hanshin Juvenile Fillies', 22),
	    RaceGoal(5, 'Tulip Sho', 28),
	    RaceGoal(5, 'Oka Sho', 30),
	    RaceGoal(5, 'Tokyo Yushun', 33),
	    RaceGoal(3, 'Shuka Sho', 43),
	    RaceGoal(1, 'Arima Kinen', 47),
	    RaceGoal(3, 'Victoria Mile', 56),
	    RaceGoal(2, 'Yasuda Kinen', 58),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 67)
	],
	'Special Week': [
	    RaceGoal(5, 'Kisaragi Sho', 26),
	    RaceGoal(5, 'Tokyo Yushun', 33),
	    RaceGoal(3, 'Kikuka Sho', 43),
	    RaceGoal(3, 'Tenno Sho (Spring)', 55),
	    RaceGoal(2, 'Japan Cup', 69),
	    RaceGoal(1, 'Arima Kinen', 71)
	],
	'Silence Suzuka': [
	    FanGoal(5000, 26),
	    RaceGoal(5, 'Yayoi Sho', 28),
	    RaceGoal(5, 'Kobe Shimbun Hai', 41),
	    RaceGoal(1, 'Kinko Sho', 52),
	    RaceGoal(3, 'Takarazuka Kinen', 59),
	    RaceGoal(1, 'Mainichi Okan', 66),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 67)
	]
}

GOAL_DB.update(parse_goals(RaceGoal,FanGoal))

def make_debut(uma, data):
    Race = RaceData(None, "Junior Make Debut", data.best_dist, 0, data.get_turf_apt()>=6)
    return RaceGoal(99, Race, 4)

def get_goals(uma, data):
    if uma in GOAL_DB:
        debut = make_debut(uma, data)

        goals = [debut, *GOAL_DB[uma]]
        return goals
    raise ValueError(f"That uma doesnt have a goal, {uma}")

def turns_till_next(goal, month, half):
    turn = _turn(goal.deadline)
    return turn - month * 2 - half

def check_goal(goal, career):
    if isinstance(goal, RaceGoal):
        if goal.placement == 99:
            return True
        return career.last_race.placement <= goal.placement
    elif isinstance(goal, FanGoal):
        return career.fans >= goal.requirement
