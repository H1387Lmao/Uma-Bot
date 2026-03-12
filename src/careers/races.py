from __future__ import annotations

class Race:
    __slots__ = ('name', 'grade', 'fans_required', 'month', 'half',
                 'location', 'surface', 'distance')

    def __init__(
        self,
        name: str,
        grade: str,
        fans_required: int,
        month: int,
        half: str,
        location: str,
        surface: str,
        distance: int,
    ):
        self.name = name
        self.grade = grade
        self.fans_required = fans_required
        self.month = month
        self.half = half
        self.location = location
        self.surface = surface
        self.distance = distance

    def to_dict(self) -> dict:
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __repr__(self) -> str:
        return (f"Race({self.name!r}, grade={self.grade!r}, "
                f"month={self.month}, half={self.half!r})")

ALL_RACES: list[Race] = [
    Race("Debut Race",          "Debut",  0,    4,  "early",  "Sapporo",   "Turf",  1200),
    Race("Maiden Race",         "Maiden", 0,    4,  "late",   "Sapporo",   "Turf",  1400),
    Race("Maiden (Dirt)",       "Maiden", 0,    5,  "early",  "Tokyo",     "Dirt",  1400),

    Race("Daily Hai Nisai Stakes",  "G3", 100,   6,  "late",   "Hanshin",   "Turf",  1600),
    Race("Kyoto Himba Stakes",      "G3", 200,   6,  "early",  "Kyoto",     "Turf",  1400),
    Race("Nakayama Himba Stakes",   "G3", 200,   9,  "early",  "Nakayama",  "Turf",  1200),
    Race("Chunichi Shimbun Hai",    "G3", 300,  12,  "early",  "Chukyo",    "Turf",  2000),
    Race("Arlington Cup",           "G3", 300,   1,  "late",   "Hanshin",   "Turf",  1600),
    Race("Radio Nikkei Sho",        "G3", 200,   6,  "early",  "Fukushima", "Turf",  1800),
    Race("Tokai Stakes",            "G3", 400,   1,  "late",   "Chukyo",    "Dirt",  1800),
    Race("Kokura Kinen",            "G3", 300,   7,  "late",   "Kokura",    "Turf",  1800),
    Race("Keio Hai Spring Cup",     "G3", 250,   5,  "early",  "Tokyo",     "Turf",  1400),
    Race("Meji Kinen",              "G3", 350,   9,  "late",   "Nakayama",  "Turf",  1800),

    Race("Yayoi Sho",               "G2", 500,   3,  "early",  "Nakayama",  "Turf",  2000),
    Race("Tulip Sho",               "G2", 400,   3,  "early",  "Hanshin",   "Turf",  1600),
    Race("Fuchu Himba Stakes",      "G2", 600,   9,  "late",   "Tokyo",     "Turf",  1800),
    Race("Mainichi Okan",           "G2", 700,  10,  "early",  "Tokyo",     "Turf",  1800),
    Race("Hanshin Daishoten",       "G2", 800,   3,  "late",   "Hanshin",   "Turf",  3000),
    Race("Satsuki Sho (Trial)",     "G2", 500,   3,  "late",   "Nakayama",  "Turf",  2000),
    Race("Rose Stakes",             "G2", 600,   9,  "early",  "Tokyo",     "Turf",  1800),
    Race("Sports Nippon Sho Osaka Hai", "G2", 900, 3, "late",  "Hanshin",   "Turf",  2000),

    Race("Satsuki Sho",             "G1", 1000,  4,  "early",  "Nakayama",  "Turf",  2000),
    Race("Oka Sho",                 "G1", 1000,  4,  "early",  "Hanshin",   "Turf",  1600),
    Race("Japanese Derby",          "G1", 2000,  5,  "late",   "Tokyo",     "Turf",  2400),
    Race("Yushun Himba",            "G1", 1500,  5,  "late",   "Tokyo",     "Turf",  2400),
    Race("Takarazuka Memorial",     "G1", 3000,  6,  "late",   "Hanshin",   "Turf",  2200),
    Race("Kikka Sho",               "G1", 2000, 10,  "late",   "Kyoto",     "Turf",  3000),
    Race("Shuka Sho",               "G1", 2000, 10,  "late",   "Kyoto",     "Turf",  2000),
    Race("Tenno Sho (Autumn)",      "G1", 4000, 10,  "late",   "Tokyo",     "Turf",  2000),
    Race("Mile Championship",       "G1", 3500, 11,  "late",   "Kyoto",     "Turf",  1600),
    Race("Queen Elizabeth II Cup",  "G1", 3000, 11,  "early",  "Kyoto",     "Turf",  2200),
    Race("Japan Cup",               "G1", 5000, 11,  "late",   "Tokyo",     "Turf",  2400),
    Race("Champions Cup",           "G1", 4000, 12,  "early",  "Chukyo",    "Dirt",  1800),
    Race("Arima Kinen",             "G1", 6000, 12,  "late",   "Nakayama",  "Turf",  2500),
    Race("February Stakes",         "G1", 3000,  2,  "late",   "Tokyo",     "Dirt",  1600),
    Race("Tenno Sho (Spring)",      "G1", 4000,  4,  "late",   "Kyoto",     "Turf",  3200),
    Race("Victoria Mile",           "G1", 3500,  5,  "early",  "Tokyo",     "Turf",  1600),
    Race("Yasuda Kinen",            "G1", 3500,  6,  "early",  "Tokyo",     "Turf",  1600),
    Race("Sprinters Stakes",        "G1", 2500,  9,  "late",   "Nakayama",  "Turf",  1200),
    Race("Takamatsunomiya Kinen",   "G1", 2500,  3,  "late",   "Chukyo",    "Turf",  1200),
    Race("Osaka Hai",               "G1", 4000,  4,  "early",  "Hanshin",   "Turf",  2000),
]

RACE_BY_NAME: dict[str, Race] = {race.name: race for race in ALL_RACES}
