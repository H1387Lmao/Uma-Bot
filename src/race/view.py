from uicord import *

class RaceView:
    def __init__(self, race, owner):
        self.race = race
        self.owner = owner

    def get_view(self):
        race_text = f"### **{self.race.track_name.name}**\n"
        
        # Determine viewport (centered on player or front of pack)
        player_uma = next((u for u in self.race.runners if u.is_player), self.race.runners[0])
        viewport_center = player_uma.pos
        viewport_size = 15 # units
        viewport_min = viewport_center - viewport_size / 2
        viewport_max = viewport_center + viewport_size / 2

        # Create tracks for each lane
        lane_tracks = [["─"] * 15 for _ in range(self.race.max_lanes)]
        
        for u in self.race.runners:
            if u.finished: continue
            # Relative position in viewport
            rel_pos = (u.pos - viewport_min) / viewport_size
            if 0 <= rel_pos < 1:
                idx = int(rel_pos * 15)
                # Overwrite track char with emoji or simple symbol
                lane_tracks[u.lane][idx] = str(u.emoji)

        for i, lane in enumerate(lane_tracks):
            lane_str = "".join(lane)
            race_text += f"Lane {i+1}: `{lane_str}`\n"

        # List all racers and their progress
        race_text += "\n**Standings:**\n"
        sorted_runners = sorted(self.race.runners, key=lambda u: u.pos, reverse=True)
        for i, u in enumerate(sorted_runners):
            progress = (u.pos / self.race.track_length) * 100
            status = "🏁" if u.finished else f"{progress:.1f}%"
            race_text += f"{i+1}. {u.emoji} {u.name} {u.display_effects()} - {status}\n"

        if self.race.event_queue:
            race_text += "\n" + "\n".join(list(self.race.event_queue)[-3:])

        return View(Container(Text(race_text)), owner=self.owner)
