MAX_STATS = 1200
DEFAULT_STATS = (87, 98, 85, 89, 80)

JANUARY = 0
FEBUARY = 1
MARCH = 2
APRIL = 3
MAY = 4
JUNE = 5
JULY = 6
AUGUST = 7
SEPTEMBER = 8
OCTOBER = 9
NOVEMBER = 10
DECEMBER = 11

EARLY = 1
LATE = 2

SCALING = {
    "r": (75, 125, 150, 180, 200),
    "sr": (35, 50, 75, 90, 125),
    "ssr": (6, 7, 13, 20, 25)
}

def GET_SCALER(level):
    return (level * 0.35) + 1
