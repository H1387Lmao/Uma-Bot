from ..data import SCHEDULES, races_by_turn_name, RaceData
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
    def __repr__(self):
        return f"Get atleast {self.placement}th in {self.race_data.name} before turn {_turn(self.deadline)}"

class FanGoal:
    def __init__(self, required_fans=0, by_turn=[0,0]):
        self.requirement = required_fans
        self.deadline = by_turn
    def __repr__(self):
        return f"Acquire {self.requirement} fans before turn {_turn(self.deadline)}"


GOAL_DB = {
	'Haru Urara': [
		FanGoal(5000, 31),
		FanGoal(9000, 39),
		FanGoal(12000, 42),
		RaceGoal(5, 'Negishi Stakes', 44),
		RaceGoal(5, 'February Stakes', 46),
		RaceGoal(5, 'Elm Stakes', 57),
		RaceGoal(5, 'JBC Sprint', 63),
		RaceGoal(99, 'Arima Kinen', 66)
	],
	'Agnes Tachyon': [
	    RaceGoal(5, 'Yayoi Sho', 23),
	    RaceGoal(5, 'Satsuki Sho', 25),
	    RaceGoal(5, 'Tokyo Yushun', 28),
	    RaceGoal(3, 'Kikuka Sho', 38),
	    RaceGoal(1, 'Osaka Hai', 48),
	    RaceGoal(3, 'Takarazuka Kinen', 54),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 62),
	    RaceGoal(1, 'Arima Kinen', 66)
	],
	'Vodka': [
	    RaceGoal(99, 'Hanshin Juvenile Fillies', 17),
	    RaceGoal(5, 'Oka Sho', 25),
	    RaceGoal(5, 'Tokyo Yushun', 28),
	    RaceGoal(5, 'Yasuda Kinen', 29),
	    RaceGoal(3, 'Takarazuka Kinen', 54),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 62)
	],
	'Special Week': [
	    RaceGoal(5, 'Kisaragi Sho', 21),
	    RaceGoal(5, 'Tokyo Yushun', 28),
	    RaceGoal(3, 'Kikuka Sho', 38),
	    RaceGoal(3, 'Tenno Sho (Spring)', 50),
	    RaceGoal(2, 'Japan Cup', 64),
	    RaceGoal(1, 'Arima Kinen', 66)
	],
	'Silence Suzuka': [
	    FanGoal(5000, 21),
	    RaceGoal(5, 'Yayoi Sho', 23),
	    RaceGoal(5, 'Kobe Shimbun Hai', 36),
	    RaceGoal(1, 'Kinko Sho', 47),
	    RaceGoal(3, 'Takarazuka Kinen', 54),
	    RaceGoal(1, 'Mainichi Okan', 61),
	    RaceGoal(1, 'Tenno Sho (Autumn)', 62)
	]
}

def make_debut(uma, data):
    Race = RaceData(None, "Junior Make Debut", data.best_dist, 0, data.get_turf_apt()>=6)
    return RaceGoal(3, Race, 4)

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
