from .constants import DEFAULT_STATS
from ..skills import Skill

class SCData:
    def __init__(self, name, rarity, description, label=None, stat="SPD", id=1):
        self.name = name
        self.rarity = rarity
        self.description = description
        self.label = f"({label})" if label else ""
        self.stat = stat.lower()
        self.id = id
        self.img_id = len(self.rarity) * 10000 + self.id
    
    def display(self, bot):
        return f"{bot.em[self.stat.upper()]}{self.name} {self.label}"
    
    def get_id(self):
        return self.img_id
    
    def get_image(self):
        handle = "https://gametora.com/images/umamusume/supports/support_card_s_"
        return handle + f"{self.get_id()}.png"


class UmaData:
    def __init__(self, name, rarity, stats, unobtainable=True, skill=None):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.ult = skill
        self.unobtainable = unobtainable
