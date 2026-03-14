from .goals import *
from ..data.uma_database import UMAS
import random

stats = ['spd', 'stm', 'pwr', 'gut', 'wit', 'skill_points']

stat_to_index = {s: i for i, s in enumerate(stats)}

training_bonuses = {
	'spd': [('spd', 20), ('pwr', 10),          ('skill_points', 4), ('energy', -20)],
	'stm': [('stm', 20), ('gut', 10),          ('skill_points', 4), ('energy', -20)],
	'pwr': [('stm', 10), ('pwr', 20),          ('skill_points', 4), ('energy', -20)],
	'gut': [('spd', 5),  ('pwr', 5),           ('gut', 20),         ('skill_points', 4), ('energy', 35)],
	'wit': [('wit', 20), ('skill_points', 10), ('energy', 5)]
}

class Career:
	def __init__(
		self,
		owner,
		name,
		fans = 0,
		energy = 0,
		mood = 0,
		skill_points = 120,
		stats = [0,0,0,0,0],
		skills = [],
		conditions = [],
		races_scheduled = [],
		support_cards = [],
		goals_done = 0,
		turn = 0,
		seed = None
	):
		self.owner = owner
		self.name = name
		self.fans = fans
		self.energy = energy
		self.mood = mood
		self.stats = stats
		self.conditions = conditions
		self.races_scheduled = races_scheduled
		self.turn = turn
		
		self.advance()
		
		self.support_cards = support_cards

		self.skill_points = skill_points
		self.skills = skills

		self.goals = get_goals(name, UMAS[name])
	@staticmethod
	def create_new(name, uid, sps):
		uma_data = UMAS[name]
		return Career(uid, name, 1, 100, 2, uma_data.stats, [], [], sps)

	def train(self, stat):
		if stat is not None:
			self.advance()
		bonuses = {}
		for effect in training_bonuses[stat]:
			if len(effect[0])==3:
				index = stat_to_index[effect[0]]
				self.stats[index]+=effect[1]
			elif effect[0] == 'energy':
				self.energy+=effect[1]
			elif effect[0] == 'skill_points':
				self.skill_points+=effect[1]
			if stat is None:
				bonuses[effect[0]] = effect[1]

		return bonuses

	def advance(self):
		self.turn += 1
		self.month = self.turn//2
		self.half = self.turn%2
		self.year = (self.month//12+1)
