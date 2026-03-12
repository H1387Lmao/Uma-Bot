import random
from collections import deque

class RaceUma:
    def __init__(self, name, stats, emoji, is_player=False, owner=None, career=None, club_uma=False, skills=[], race=None):
        self.name = name
        self.stats = stats  # spd, stm, pwr, gut, wit
        self.emoji = emoji
        self.is_player = is_player
        self.owner = owner
        self.career = career
        self.club_uma = club_uma
        self.race = race

        self.spd, self.stm, self.pwr, self.gut, self.wit = self.stats
        
        self.pos = 0.0
        self.lane = 0 # 0 is inside, higher is outside
        self.target_lane = 0
        self.lane_progress = 1.0 # 1.0 means fully in lane
        
        self.vel = 0.0
        self.accel = 0.0
        self.finished = False
        self.placement = 0
        
        self.effects = deque(maxlen=5)
        self.skills = skills
        self.skilluses = {a.name: a.uses for a in skills if hasattr(a, 'uses')}
        
        self.blocked_by = None
        self.is_dueling = False
        self.duel_target = None
        self.duel_timer = 0

        # Missing attributes needed by skills
        self.order_rate = 0.0
        self.group_rate = 0.0
        self.late_chance = 0.0
        self.ACCEL_RATE = 1.0

    @property
    def maneuverability(self):
        # Derived from Power (60%) and Speed (40%).
        return (self.spd * 0.4 + self.pwr * 0.6)

    def __repr__(self):
        if self.club_uma:
            return f"{self.owner}'s {self.name}"
        return self.name

    def update_physics(self):
        if self.finished:
            return

        # Acceleration logic (simplified from old project)
        # In a real implementation, this would be more complex based on distance/phase
        target_vel = self.race.track_length / 15 # Placeholder base speed
        # Adjust target_vel by speed stat
        target_vel *= (1 + (self.spd - 800) / 2000)
        
        if self.vel < target_vel:
            self.vel += (self.pwr / 100) * 0.1 * self.ACCEL_RATE
        elif self.vel > target_vel:
            # Gradually slow down to target speed if exceeding it (e.g. after a boost)
            self.vel = max(target_vel, self.vel - 0.5)
        
        # Blocking logic
        self.blocked_by = None
        uma_ahead = self.race.get_uma_immediately_ahead(self)
        if uma_ahead:
            dist = uma_ahead.pos - self.pos
            if dist < 2.0 and uma_ahead.lane == self.lane:
                self.blocked_by = uma_ahead
                # Match speed of the one in front if blocked
                self.vel = min(self.vel, uma_ahead.vel)
                
        # Lane changing logic
        if self.target_lane != self.lane:
            change_speed = (self.maneuverability / 1000) * 0.2
            self.lane_progress -= change_speed
            if self.lane_progress <= 0:
                self.lane = self.target_lane
                self.lane_progress = 1.0
        elif self.blocked_by and self.lane_progress >= 1.0:
            # Try to change lanes if blocked
            self.decide_lane_change()

        # Dueling logic
        if self.is_dueling:
            self.duel_timer += 1
            if self.duel_target:
                # In a duel, stay close in lanes
                # Winner pulls forward after some time
                if self.duel_timer > 20:
                    if self.vel > self.duel_target.vel:
                        self.pos += 0.5
                    else:
                        self.pos -= 0.1
            if self.duel_timer > 50:
                self.is_dueling = False
                self.duel_target = None

        self.pos += self.vel * (1.0 + random.uniform(-0.02, 0.02))
        
        if self.pos >= self.race.track_length:
            self.pos = self.race.track_length
            self.finished = True

    def decide_lane_change(self):
        # Maneuverability check: higher means more likely to find a gap or push through
        possible_lanes = []
        if self.lane > 0: possible_lanes.append(self.lane - 1)
        if self.lane < self.race.max_lanes - 1: possible_lanes.append(self.lane + 1)
        
        for l in possible_lanes:
            if not self.race.is_lane_occupied(l, self.pos):
                self.target_lane = l
                return

    def display_effects(self):
        from src.skills import EFFECTS
        return "".join([EFFECTS.get(a, a) for a in self.effects])
