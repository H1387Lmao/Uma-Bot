import random
import asyncio
from collections import deque
from .uma import RaceUma

class Race:
    def __init__(self, bot, career, runners, track_length, track_name, max_lanes=3):
        self.bot = bot
        self.career = career
        self.runners = runners
        self.track_length = track_length
        self.track_name = track_name
        self.max_lanes = max_lanes
        
        self.turn = 0
        self.finished = False
        self.winners = []
        self.event_queue = deque(maxlen=10)

        # Initialize lanes for runners
        for i, runner in enumerate(self.runners):
            runner.lane = i % self.max_lanes
            runner.target_lane = runner.lane
            runner.race = self

    def step(self):
        self.turn += 1
        
        # Sort by position to handle logic based on order
        sorted_runners = sorted(self.runners, key=lambda u: u.pos, reverse=True)
        
        total_runners = len(self.runners)
        for i, runner in enumerate(sorted_runners):
            if runner.finished:
                continue

            runner.placement = i + 1
            # group_rate: 100 is 1st, 0 is last
            if total_runners > 1:
                runner.group_rate = (total_runners - runner.placement) / (total_runners - 1) * 100
            else:
                runner.group_rate = 100.0
            
            # order_rate: Progress percentage (0 to 100)
            runner.order_rate = (runner.pos / self.track_length) * 100
            
            runner.update_physics()
            
            # Trigger skills
            for skill in runner.skills:
                # Skill.can_trigger should handle uses check and freq
                if skill.can_trigger(runner, self):
                    skill.activate(runner, self)

            if runner.finished and runner not in self.winners:
                self.winners.append(runner)
                # placement is fixed once they finish
                runner.placement = len(self.winners)

        # Check for duels (nearby runners in same or adjacent lanes)
        self.check_for_duels()

        if all(u.finished for u in self.runners):
            self.finished = True

    def check_for_duels(self):
        for i, u1 in enumerate(self.runners):
            if u1.finished or u1.is_dueling: continue
            for u2 in self.runners[i+1:]:
                if u2.finished or u2.is_dueling: continue
                
                # If they are very close and side-by-side
                if abs(u1.pos - u2.pos) < 1.0 and abs(u1.lane - u2.lane) <= 1:
                    if random.random() < 0.1: # 10% chance per tick to start a duel
                        u1.is_dueling = True
                        u1.duel_target = u2
                        u1.duel_timer = 0
                        u2.is_dueling = True
                        u2.duel_target = u1
                        u2.duel_timer = 0
                        self.push_event(f"**{u1.name}** and **{u2.name}** are dueling!")

    def get_uma_immediately_ahead(self, racer):
        ahead = [u for u in self.runners if u.pos > racer.pos and u.lane == racer.lane]
        if not ahead: return None
        return min(ahead, key=lambda u: u.pos - racer.pos)

    def is_lane_occupied(self, lane, pos, buffer=2.0):
        for u in self.runners:
            if u.lane == lane and abs(u.pos - pos) < buffer:
                return True
        return False

    def get_ahead(self, placement):
        return [u for u in self.runners if u.placement < placement]

    def get_behind(self, placement):
        return [u for u in self.runners if u.placement > placement]

    def get_near(self, placement, range_val=2):
        return [u for u in self.runners if 0 < abs(u.placement - placement) <= range_val]

    def get_others(self, racer):
        return [u for u in self.runners if u != racer]

    def push_event(self, text):
        self.event_queue.append(text)

    def standings(self):
        return sorted(self.runners, key=lambda u: u.pos, reverse=True)
