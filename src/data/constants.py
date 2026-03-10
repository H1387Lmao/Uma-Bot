# Global constants
MAX_STATS = 1200
DEFAULT_STATS = (87, 98, 85, 89, 80)

# Level requirement scaling constants
SCALING = {
    "r": (75, 125, 150, 180, 200),
    "sr": (35, 50, 75, 90, 125),
    "ssr": (6, 7, 13, 20, 25)
}

def GET_SCALER(level):
    return (level * 0.35) + 1
