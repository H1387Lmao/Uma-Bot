from .goals import *
from ..data.uma_database import UMAS
import random

stat_names = ['spd', 'stm', 'pwr', 'gut', 'wit', 'sp']

stat_to_index = {s: i for i, s in enumerate(stat_names)}

training_bonuses = {
	'spd': [('spd', 20), ('pwr', 10),          ('sp', 4), ('energy', -20)],
	'stm': [('stm', 20), ('gut', 10),          ('sp', 4), ('energy', -20)],
	'pwr': [('stm', 10), ('pwr', 20),          ('sp', 4), ('energy', -20)],
	'gut': [('spd', 5),  ('pwr', 5),           ('gut', 20),         ('sp', 4), ('energy', 35)],
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
		conditions: list[int] = [],
		races_scheduled: list[int] = [],
		support_cards: list[int] = [],
		goals_done: int = 0,
		turn: int = 0,
		seed: int = None,
		max_energy: int = 100
	):
		self.owner: int = owner
		self.name: str = name
		self.fans: int = fans
		self.energy: int = energy
		self.mood: int = mood
		self.stats: list[int] = stats
		self.conditions: list[int] = conditions
		self.races_scheduled: list[int] = races_scheduled
		self.turn: int = turn		
		self.support_cards: list[int] = support_cards
		self.goals_done: int = goals_done
		self.seed: int = seed

		self.skill_points: int = skill_points
		self.skills: list[int] = skills

		self.max_energy = max_energy

		self.goals: list[FanGoal|RaceGoal] = get_goals(name, UMAS[name])

		self.update_current_goal()

		self.advance()


	@staticmethod
	def create_new(name, uid, sps):
		uma_data = UMAS[name]
		return Career(uid, name, 1, 100, 2, 120, list(uma_data.stats), [], [], sps)
	def update_current_goal(self):
		for goal in self.goals[self.goals_done:]:
			if goal.deadline == self.turn:
				self.current_goal = goal
				return
		self.current_goal=None

	def train(self, stat, is_preview=False):
		if stat is None:
			return
		if not is_preview:
			self.advance()
		bonuses = {}
		for effect in training_bonuses[stat]:
			if is_preview:
				bonuses[effect[0]] = effect[1]
				continue
			if len(effect[0])==3:
				index = stat_to_index[effect[0]]
				self.stats[index]+=effect[1]
			elif effect[0] == 'energy':
				self.energy+=effect[1]
				self.energy = min(self.max_energy, self.energy)
				self.energy = max(0, self.energy)
			elif effect[0] == 'sp':
				self.skill_points+=effect[1]

		return bonuses

	def advance(self):
		self.turn += 1
		self.month = self.turn//2 + 3 # start in april
		self.half = (self.turn-1)%2
		self.year = (self.month//12+1)
		
		self.update_current_goal()

	def get_needed_goal(self):
		for goal in self.goals[self.goals_done:]:
			if goal.deadline >= self.turn:
				return goal
