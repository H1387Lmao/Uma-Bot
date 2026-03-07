from enum import IntEnum
import random

class TRACK_TYPE(IntEnum):
    Turf = 0
    Dirt = 1

class TRACK_WEATHER(IntEnum):
    Sunny = 0
    Snowy = 1
    Rainy = 2
    Cloudy = 3

class TRACK_SEASON(IntEnum):
    Summer = 0
    Winter = 1
    Fall = 2
    Spring = 3

class TRACK_LENGTH(IntEnum):
    Short = 1200
    Mile = 1600
    Medium = 1800
    Long = 2200

class TRACK_TIME(IntEnum):
    Day = 0
    Night = 1
    Sunset = 2

class TRACK_NAME(IntEnum):
    Sapporo = 0
    Hakodate = 1
    Niigata = 2
    Fukushima = 4
    Nakayama = 5
    Tokyo = 6
    Chukyo = 7
    Kyoto = 8
    Hanshin = 9
    Kokura = 10
    Oi = 11
    Kawasaki = 12
    Funabashi = 13
    Morioka = 14
    Longchamp = 15

def random_enum(Enums):
    return random.choice([priority for priority in Enums])

class Skill:
    def __init__(
        self,
        name,
        desc,
        skillprice, 
        effects=[], 
        uses=1, 
        condition=None, 
        type="Buffed", 
        icon="green_speed", 
        rarity="normal",
        duration="inf",
        freq=0.1
    ):
        self.name      = name
        self.price     = skillprice
        self.desc      = desc
        self.effects   = effects
        self.uses      = uses
        self.condition = condition
        self.duration  = duration
        self.type      = type
        self.icon      = icon
        self.rarity    = rarity
        self.freq      = freq

    def activate(self, owner, race):
        if self.uses != "passive":
            race.push_event(f"{owner} used {self.display(race.bot)}!")

        for t, effect in self.effects:
            match t:
                case "self":
                    self.affect(owner, effect)
                case "ahead":
                    targets = race.get_ahead(owner.placement)
                    self.affect_targets(targets, owner, effect, t)
                case "behind":
                    targets = race.get_behind(owner.placement)

                    self.affect_targets(targets, owner, effect, t)
                case "radius":
                    targets = race.get_near(owner.placement, 2)

                    self.affect_targets(targets, owner, effect, t)
                case "all":
                    targets = race.get_others(owner)

                    self.affect_targets(targets, owner, effect, t)
        if self.uses!="passive":
            owner.skilluses[self.name]-=1
    def affect_targets(self, targets, owner, effect, type):
        for target in targets:
            self.affect(target, effect, type)
    def color(self):
        match self.rarity:
            case "normal":
                return ""
            case "gold":
                return "🟡"
    @property
    def value(self):
        return 500 if self.rarity!="gold" else 1200
        
    def can_trigger(self, owner, race):
        if self.uses == "passive": return False
        if owner.skilluses[self.name]<=0:
            return False 
        if random.random()>self.freq:
            return False
        if self.condition:
            return self.condition(owner, race)
        return True
    def display(self, bot):
        return f"{bot.em.get(self.icon, self.icon)} **{self.name}**{self.color()}"
    def __repr__(self):
        return f"{self.name} {self.price}"
    def affect(self, target, e, type="self"):
        stam = e.get("stm", 0)
        spd = e.get("spd", 0)
        vel = e.get("vel", 0)
        accel=e.get("accel", 0)
        late = e.get("late_start_chance", 0)

        target.spd+=spd
        target.stm+=stam
        target.vel+=vel
        target.ACCEL_RATE+=accel
        target.late_chance-=late
        if isinstance(self.type, dict):
            target.effects.append(self.type[type])
        else:
            target.effects.append(self.type)

# =========================
# SKILL DEFINITIONS
# =========================

EFFECTS = {
    "Late Start": "😰",
    "Debuffed": "😔",
    "Buffed": "🙃",
    "Better": "✨",
    "Rushed": "😡",
    "Ult": "🔥"
}

def GetIndex(*skills):
    for i, skill in enumerate(skills):
        skill.id=i
    return skills

SKILLS = GetIndex(
    Skill(
        "Opening Gambit",
        "Slightly dull movement for runners ahead when positioned toward the back early-race.",
        160,
        (
            ("ahead", {
                "vel": -30
            })
        ,),
        1,
        lambda owner, race: 35<=owner.order_rate<=50,
        "Rushed",
        "red_rush"
    ),
    Skill(
        "Intimidate",
        "If you're in the first half of the pack during the Opening Leg, girls in the back become slightly slower",
        170,
        (
            ("behind", {
                "vel":-20
            })
        ,),
        1,
        lambda owner, race: 35<=owner.order_rate<=50,
        "Debuffed",
        "red_tire"
    ),
    Skill(
        "Intense Gaze",
        "Slightly unnerve girls you set your sights on in the Final Leg",
        180,
        (
            ("ahead",{
                "vel": -10
            })
        ,),
        1,
        lambda owner, race: 75<=owner.order_rate<=100,
        "Late Start",
        "red_tire"
    ),
    Skill(
        "Stamina Eater",
        "If you're in the back at a random point during the Middle Leg, you will drain stamina from enemy girls ahead of you, and your own stamina will slightly recover",
        160,
        (
            ("ahead",{
                "stm": -30
            }),
            ("self",{
                "stm": 20
            })
        ,),
        1,
        lambda owner, race: 35<=owner.order_rate<=75 and 35<=owner.group_rate<=50,
        {
            "self": "Better",
            "ahead": "Rushed"
        },
        "red_tire"
    ),
    Skill(
        "Go with the Flow",
        "Become a little better at positioning during the Final Leg of the race",
        120,
        (
            ("self",{
                "pwr": 250,
                "vel": 20
            })
        ,),
        1,
        lambda owner, race: 75<=owner.order_rate<=100,
        "Better",
        "yellow_measure"
    ),
    Skill(
        "Meticulous Measures",
        "At a random point during the Middle Leg, your acceleration and lane movement speed will slightly increase",
        140,
        (
            ("self",{
                "accel": 20
            })
        ,),
        1,
        lambda owner, race: 35<=owner.order_rate<=50,
        "Buffed",
        "yellow_measure"
    ),
    Skill(
        "Center Stage",
        "At a random point in the Opening Leg, your lane movement speed will increase",
        120,
        (
            ("self",{
                "accel": 10
            })
        ,),
        1,
        lambda owner, race: 15<=owner.order_rate<=35,
        "Better",
        "yellow_measure",
    ),
    Skill(
        "Early Lead",
        "At the start of the race, your acceleration will slightly increase",
        120,
        (
            ("self",{
                "accel": 20
            })
        ,),
        1,
        None, #instant,
        "Buffed",
        "yellow_velocity"
    ),
    Skill(
        "Final Push",
        "At a random point during the Final Corner, if you're in the lead, your acceleration will slightly increase",
        180,
        (
            ("self",{
                "vel": 50
            })
        ,),
        1,
        lambda owner, race: 75<=owner.order_rate<=100,
        "Ult",
        "yellow_velocity"
    ),
    Skill(
        "Prepared To Pass",
        "At a random point on the Final Corner, if you're in the first half of the pack, your speed will slightly increase",
        180,
        (
            ("self",{
                "vel": 50
            })
        ,),
        1,
        lambda owner, race: 75<=owner.order_rate<=100 and 50<=owner.group_rate,
        "Ult",
        "yellow_gold",
        "gold"
    ),
    Skill(
        "Deep Breaths",
        "At a random point during the Middle Leg, your stamina will slightly recover",
        160,
        (
            ("self",{
                "stm": 60
            })
        ,),
        1,
        lambda owner, race: 35<=owner.order_rate<=75,
        "Better",
        "blue_replenish"
    ),
    Skill(
        "Quiet Breathing",
        "During the second half of the Opening Leg, if you're not in the front, your stamina will slightly recover",
        180,
        (
            ("self",{
                "stm": 70
            })
        ,),
        1,
        lambda owner, race: 25<=owner.order_rate<=35,
        "Better",
        "blue_replenish"
    ),
    Skill(
        "Ready, Steady, Go!",
        "If you're in the second half of the pack during the Final Corner and there's at least one other girl nearby, your stamina will recover",
        330,
        (
            ("self",{
                "stm":130
            })
        ,),
        1,
        lambda owner, race: 50<=owner.group_rate,
        "Ult",
        "blue_ult"
    ),
    Skill(
        "Scenery of Dreams",
        "Frantically chasing after the scenery, your Speed stat is increased by 40",
        90,
        (
            ("self", {
                "spd": 40
            })
        ,),
        "passive",
        None,
        "Better",
        "green_speed"
    ),
    Skill(
        "Running Passion",
        "Your Stamina stat is increased by 60",
        100,
        (
            ("self",{
                "stm":60
            })
        ,),
        "passive",
        None,
        "Better",
        "green_stamina"
    ),
    Skill(
        "Disorientate",
        "Decrease WIT and Speed of everyone ahead of you",
        130,
        (
            ("ahead",{
                "wit": -30,
                "vel": -50
            })
        ,),
        1,
        lambda owner, race: owner.order_rate > 30,
        "Late Start",
        "red_confuse"
    )
)

PEERLESS_HEROINE=Skill(
    "Peerless Heroine (Turf)",
    "If she is in front in the middle corner, she will move very far ahead for a short time. If she is in the middle distance, he will move extremely far ahead for a short time, and then if he is in third place or somewhere during a full-throttle sprint, she will show a short burst of speed.",
    0,
    (
        ("self",{
            "vel":250,
        }),
    ),
    1,
    lambda owner, race: owner.order_rate<=50 and race.track_type==1,
    "Ult",
    "yellow_ult"
)

MC_ULT=Skill(
    "Chasing After You",
    "Chase after an unseen friend when in midpack in the second half of the race, moderately increasing velocity steadily and very slightly intimidating runners ahead.",
    0,
    (
        ("self",{
            "vel": 130
        }),
        ("ahead", {
            "vel": -50
        })
    ),
    1,
    lambda owner, race: owner.order_rate>=75,
    {
        "self": "Ult",
        "ahead": "Late Start"
    },
    "Ult",
    "yellow_ult"
)

MOST_EXPENSIVE_SKILLS=sorted(SKILLS, key=lambda skill: skill.price, reverse=True)

print(MOST_EXPENSIVE_SKILLS, len(SKILLS))
