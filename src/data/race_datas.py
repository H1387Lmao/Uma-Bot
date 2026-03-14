from .models import RaceData

SCHEDULES: dict[int, list[RaceData]] = {

    # ── JUNIOR YEAR ──────────────────────────────────────────────────────────

    # Turn 5 — June First Half
    5: [
        RaceData("Chukyo", "Chukyo Junior Stakes",       distance=1200, grade=0, turf=True),
    ],
    # Turn 6 — June Second Half
    6: [
        RaceData("Nakayama", "Cosmo Dream Race",          distance=1200, grade=1, turf=True),
    ],
    # Turn 7 — July First Half
    7: [
        RaceData("Tokyo", "Lily Cup",                     distance=1400, grade=1, turf=True),
    ],
    # Turn 8 — July Second Half
    8: [
        RaceData("Tokyo",    "Junior Stakes",             distance=1600, grade=1, turf=True),
        RaceData("Hakodate", "Hakodate Junior Stakes",    distance=1200, grade=3, turf=True),
    ],
    # Turn 10 — August Second Half
    10: [
        RaceData("Sapporo", "Sapporo 2-Year Stakes",      distance=1200, grade=3, turf=True),
        RaceData("Niigata", "Niigata Junior Stakes",      distance=1600, grade=3, turf=True),
    ],
    # Turn 11 — September First Half
    11: [
        RaceData("Kokura",  "Kokura Junior Stakes",       distance=1200, grade=3, turf=True),
        RaceData("Sapporo", "Sapporo Junior Stakes",      distance=1800, grade=3, turf=True),
    ],
    # Turn 12 — September Second Half
    12: [
        RaceData("Niigata", "Niigata 2-Year Stakes",      distance=1200, grade=3, turf=True),
    ],
    # Turn 13 — October First Half
    13: [
        RaceData("Tokyo", "Saudi Arabia Royal Cup",       distance=1600, grade=3, turf=True),
    ],
    # Turn 14 — October Second Half
    14: [
        RaceData("Nakayama", "Pegasus Jumbo Stakes",      distance=2000, grade=1, turf=True),
        RaceData("Tokyo",    "Artemis Stakes",            distance=1600, grade=3, turf=True),
    ],
    # Turn 15 — November First Half
    15: [
        RaceData("Chukyo",  "Chukyo 2-Year Stakes",       distance=1400, grade=1, turf=False),
        RaceData("Kokura",  "Kokura 2-Year Stakes",       distance=1700, grade=3, turf=True),
        RaceData("Kyoto",   "Fantasy Stakes",             distance=1400, grade=3, turf=True),
        RaceData("Kyoto",   "Daily Hai Junior Stakes",    distance=1600, grade=4, turf=True),
        RaceData("Tokyo",   "Keio Hai Junior Stakes",     distance=1400, grade=4, turf=True),
    ],
    # Turn 16 — November Second Half
    16: [
        RaceData("Tokyo",    "Tokyo 2-Year Stakes",                distance=1800, grade=4, turf=True),
        RaceData("Kyoto",    "Kyoto 2-Year Stakes",                distance=2000, grade=3, turf=True),
        RaceData("Kyoto",    "Kyoto Junior Stakes",                distance=2000, grade=3, turf=True),
        RaceData("Tokyo",    "Tokyo Sports Hai Junior Stakes",     distance=1800, grade=3, turf=True),
    ],
    # Turn 17 — December First Half
    17: [
        RaceData("Hanshin", "Hanshin Juvenile Fillies",   distance=1600, grade=5, turf=True),
    ],
    # Turn 18 — December Second Half
    18: [
        RaceData("Hanshin",  "Asahi Hai Futurity Stakes", distance=1600, grade=5, turf=True),
        RaceData("Nakayama", "Hopeful Stakes",            distance=2000, grade=5, turf=True),
    ],
    
    # ── CLASSIC YEAR ─────────────────────────────────────────────────────────
    # Turn 19 — January First Half
    19: [
        RaceData("Nakayama", "Fairy Stakes",              distance=1600, grade=3, turf=True),
        RaceData("Nakayama", "Keisei Hai",                distance=2000, grade=3, turf=True),
    ],
    # Turn 20 — January Second Half
    20: [
        RaceData("Kyoto", "Shinzan Kinen",                distance=1600, grade=3, turf=True),
        RaceData("Kyoto", "Kinkakuji Stakes",             distance=1400, grade=3, turf=True),
    ],
    # Turn 21 — February First Half
    21: [
        RaceData("Kyoto",  "Kisaragi Sho",                distance=1800, grade=3, turf=True),
        RaceData("Tokyo",  "Kyodo News Hai",              distance=1800, grade=3, turf=True),
        RaceData("Tokyo",  "Queen Cup",                   distance=1600, grade=3, turf=True),
    ],
    # Turn 22 — February Second Half
    22: [
        RaceData("Hanshin", "Himeyama Stakes",            distance=2000, grade=3, turf=True),
        RaceData("Tokyo",   "Keihin Hai",                 distance=1300, grade=3, turf=False),
    ],
    # Turn 23 — March First Half
    23: [
        RaceData("Nakayama", "Eastern Road",              distance=2000, grade=1, turf=True),
        RaceData("Nakayama", "Yayoi Sho",                 distance=2000, grade=4, turf=True),
        RaceData("Hanshin",  "Tulip Sho",                 distance=1600, grade=4, turf=True),
        RaceData("Hanshin",  "Fillies' Revue",            distance=1400, grade=4, turf=True),
    ],
    # Turn 24 — March Second Half
    24: [
        RaceData("Chukyo",   "Spring Stakes",             distance=1600, grade=4, turf=True),
        RaceData("Hanshin",  "Sansho Stakes",             distance=1800, grade=1, turf=False),
        RaceData("Nakayama", "Flower Cup",                distance=1800, grade=3, turf=True),
        RaceData("Hanshin",  "Mainichi Hai",              distance=1800, grade=3, turf=True),
        RaceData("Chukyo",   "Falcon Stakes",             distance=1400, grade=3, turf=True),
    ],
    # Turn 25 — April First Half
    25: [
        RaceData("Hanshin",  "Oka Sho",                   distance=1600, grade=5, turf=True),
        RaceData("Nakayama", "Satsuki Sho",               distance=2000, grade=5, turf=True),
        RaceData("Nakayama", "New Zealand Trophy",        distance=1600, grade=4, turf=True),
        RaceData("Hanshin",  "Arlington Cup",             distance=1600, grade=3, turf=True),
    ],
    # Turn 26 — April Second Half
    26: [
        RaceData("Hanshin", "Mainichi Cup",               distance=1600, grade=4, turf=True),
        RaceData("Tokyo",   "Keio Hai Spring Cup",        distance=1600, grade=4, turf=True),
        RaceData("Tokyo",   "Aoba Sho",                   distance=2400, grade=4, turf=True),
        RaceData("Tokyo",   "Flora Stakes",               distance=2000, grade=4, turf=True),
    ],
    # Turn 27 — May First Half
    27: [
        RaceData("Kyoto",   "Kyoto Shimbun Hai",          distance=2200, grade=4, turf=True),
        RaceData("Hanshin", "Sports Nippon Sho Osaka-Hamburg Cup", distance=2400, grade=4, turf=True),
        RaceData("Tokyo",   "NHK Mile Cup",               distance=1600, grade=5, turf=True),
    ],
    # Turn 28 — May Second Half
    28: [
        RaceData("Tokyo", "Yushun Himba",                 distance=2400, grade=5, turf=True),
        RaceData("Tokyo", "Tokyo Yushun",                 distance=2400, grade=5, turf=True),
        RaceData("Tokyo", "Meguro Kinen",                 distance=2500, grade=4, turf=True),
    ],
    # Turn 29 — June First Half
    29: [
        RaceData("Tokyo",   "Yasuda Kinen",               distance=1600, grade=5, turf=True),
        RaceData("Kyoto",   "Aoi Stakes",                 distance=1200, grade=3, turf=True),
        RaceData("Tokyo",   "Epsom Cup",                  distance=1800, grade=3, turf=True),
        RaceData("Hanshin", "Mermaid Stakes",             distance=2000, grade=3, turf=True),
        RaceData("Hanshin", "Naruo Kinen",                distance=2000, grade=3, turf=True),
    ],
    # Turn 30 — June Second Half
    30: [
        RaceData("Kokura",   "Kokura Kinen",              distance=2000, grade=3, turf=True),
        RaceData("Hanshin",  "Takarazuka Kinen",          distance=2200, grade=5, turf=True),
        RaceData("Hakodate", "Hakodate Sprint Stakes",    distance=1200, grade=3, turf=True),
        RaceData("Tokyo",    "Unicorn Stakes",            distance=1600, grade=3, turf=False),
    ],
    # Turn 31 — July First Half
    31: [
        RaceData("Chukyo",    "CBC Sho",                  distance=1200, grade=3, turf=True),
        RaceData("Hakodate",  "Hakodate Kinen",           distance=2000, grade=3, turf=True),
        RaceData("Chukyo",    "Procyon Stakes",           distance=1400, grade=3, turf=False),
        RaceData("Fukushima", "Radio Nikkei Sho",         distance=1800, grade=3, turf=True),
        RaceData("Fukushima", "Tanabata Sho",             distance=2000, grade=3, turf=True),
    ],
    # Turn 32 — July Second Half
    32: [
        RaceData("Chukyo",  "Chukyo Kinen",               distance=1600, grade=3, turf=True),
        RaceData("Niigata", "Ibis Summer Dash",           distance=1000, grade=3, turf=True),
        RaceData("Sapporo", "Queen Stakes",               distance=1800, grade=3, turf=True),
    ],
    # Turn 33 — August First Half
    33: [
        RaceData("Ooi",     "Japan Dirt Classic",         distance=2000, grade=5, turf=False),
        RaceData("Sapporo", "Elm Stakes",                 distance=1700, grade=3, turf=False),
        RaceData("Kokura",  "Kokura Kinen",               distance=2000, grade=3, turf=True),
        RaceData("Niigata", "Leopard Stakes",             distance=1800, grade=3, turf=False),
        RaceData("Niigata", "Sekiya Kinen",               distance=1600, grade=3, turf=True),
    ],
    # Turn 34 — August Second Half
    34: [
        RaceData("Sapporo", "Sapporo Kinen",              distance=2000, grade=4, turf=True),
        RaceData("Niigata", "Niigata Kinen",              distance=2000, grade=3, turf=True),
        RaceData("Sapporo", "Keeneland Cup",              distance=1200, grade=3, turf=True),
        RaceData("Kokura",  "Kitakyushu Kinen",           distance=1200, grade=3, turf=True),
    ],
    # Turn 35 — September First Half
    35: [
        RaceData("Nakayama",  "Sprinters Stakes",         distance=1200, grade=5, turf=True),
        RaceData("Hanshin",   "Centaur Stakes",           distance=1200, grade=4, turf=True),
        RaceData("Longchamp", "Prix Niel",                distance=2400, grade=4, turf=True),
        RaceData("Hanshin",   "Rose Stakes",              distance=1800, grade=4, turf=True),
        RaceData("Nakayama",  "Keisei Hai Autumn Handicap", distance=1600, grade=3, turf=True),
        RaceData("Nakayama",  "Shion Stakes",             distance=2000, grade=3, turf=True),
    ],
    # Turn 36 — September Second Half
    36: [
        RaceData("Hanshin",  "Kilometer Challenge Cup",   distance=1200, grade=3, turf=True),
        RaceData("Chukyo",   "Rose Stakes",               distance=1600, grade=4, turf=True),
        RaceData("Nakayama", "Sports Nippon Sho St. Lite Kinen", distance=2000, grade=4, turf=True),
        RaceData("Nakayama", "Sankei Sho All Comers",     distance=2200, grade=4, turf=True),
        RaceData("Hanshin",  "Kobe Shimbun Hai",          distance=2400, grade=4, turf=True),
        RaceData("Hanshin",  "Sirius Stakes",             distance=2000, grade=3, turf=False),
    ],
    # Turn 37 — October First Half
    37: [
        RaceData("Tokyo", "Fuchu Umamusume Stakes",       distance=1800, grade=4, turf=True),
        RaceData("Kyoto", "Kyoto Daishoten",              distance=2400, grade=4, turf=True),
        RaceData("Tokyo", "Mainichi Okan",                distance=1800, grade=4, turf=True),
    ],
    # Turn 38 — October Second Half
    38: [
        RaceData("Kyoto",  "Swan Stakes",                 distance=1400, grade=4, turf=True),
        RaceData("Tokyo",  "Fuji Stakes",                 distance=1600, grade=4, turf=True),
        RaceData("Kyoto",  "Kikuka Sho",                  distance=3000, grade=5, turf=True),
        RaceData("Kyoto",  "Shuka Sho",                   distance=2000, grade=5, turf=True),
        RaceData("Tokyo",  "Tenno Sho (Autumn)",          distance=2000, grade=5, turf=True),
    ],
    # Turn 39 — November First Half
    39: [
        RaceData("Kyoto",     "Queen Elizabeth II Cup",   distance=2400, grade=5, turf=True),  # corrected grade 4→5
        RaceData("Tokyo",     "Masashino Stakes",         distance=1600, grade=3, turf=False),
        RaceData("Tokyo",     "Copa Republica Argentina", distance=2500, grade=4, turf=True),
        RaceData("Fukushima", "Fukushima Kinen",          distance=2000, grade=3, turf=True),
        RaceData("Kyoto",     "Miyako Stakes",            distance=1800, grade=3, turf=False),
    ],
    # Turn 40 — November Second Half
    40: [
        RaceData("Tokyo",  "Japan Cup",                   distance=2400, grade=5, turf=True),
        RaceData("Kyoto",  "Mile Championship",           distance=1600, grade=5, turf=True),
        RaceData("Kyoto",  "Keihan Hai",                  distance=1200, grade=3, turf=True),
    ],
    # Turn 41 — December First Half
    41: [
        RaceData("Chukyo",   "Champions Cup",             distance=1800, grade=5, turf=False),
        RaceData("Nakayama", "Stayers Stakes",            distance=3600, grade=4, turf=True),
        RaceData("Nakayama", "Capella Stakes",            distance=1200, grade=3, turf=False),
        RaceData("Hanshin",  "Challenge Cup",             distance=2000, grade=3, turf=True),
        RaceData("Chukyo",   "Chunichi Shimbun Hai",      distance=2000, grade=3, turf=True),
        RaceData("Nakayama", "Turquoise Stakes",          distance=1600, grade=3, turf=True),
    ],
    # Turn 42 — December Second Half
    42: [
        RaceData("Nakayama", "Arima Kinen",               distance=2500, grade=5, turf=True),
        RaceData("Ooi",      "Tokyo Daishoten",           distance=2000, grade=5, turf=False),
        RaceData("Hanshin",  "Hanshin Cup",               distance=1400, grade=4, turf=True),
    ],

    # ── SENIOR YEAR ──────────────────────────────────────────────────────────

    # Turn 43 — January First Half
    43: [
        RaceData("Tokyo",    "January Stakes",            distance=1600, grade=3, turf=False),
        RaceData("Chukyo",   "Aichi Hai",                 distance=2000, grade=3, turf=True),
        RaceData("Kyoto",    "Kyoto Kimpai",              distance=1600, grade=3, turf=True),
        RaceData("Nakayama", "Nakayama Kimpai",           distance=2000, grade=3, turf=True),
        RaceData("Kyoto",    "Nikkei Shinshun Hai",       distance=2400, grade=4, turf=True),
    ],
    # Turn 44 — January Second Half
    44: [
        RaceData("Chukyo",   "Chukyo Kinen",              distance=1600, grade=3, turf=True),
        RaceData("Nakayama", "American Jockey Club Cup",  distance=2200, grade=4, turf=True),
        RaceData("Kawasaki", "Bellhein Memorial",         distance=2100, grade=5, turf=False),
        RaceData("Tokyo",    "Negishi Stakes",            distance=1400, grade=3, turf=False),
        RaceData("Kyoto",    "Silk Road Stakes",          distance=1200, grade=3, turf=True),
        RaceData("Chukyo",   "Tokai Stakes",              distance=1800, grade=4, turf=False),
    ],
    # Turn 45 — February First Half
    45: [
        RaceData("Tokyo", "Diamond Stakes",               distance=3400, grade=4, turf=True),
        RaceData("Tokyo", "Tokyo Shimbun Hai",            distance=1600, grade=3, turf=True),
        RaceData("Kyoto", "Kyoto Kinen",                  distance=2200, grade=4, turf=True),
    ],
    # Turn 46 — February Second Half
    46: [
        RaceData("Nakayama", "Nakayama Kinen",            distance=1800, grade=4, turf=True),
        RaceData("Hanshin",  "Hankyu Hai",                distance=1400, grade=3, turf=True),
        RaceData("Tokyo",    "February Stakes",           distance=1600, grade=5, turf=False),
        RaceData("Chukyo",   "Aichi Cup",                 distance=2000, grade=4, turf=True),
        RaceData("Kokura",   "Kokura Daishoten",          distance=1800, grade=3, turf=True),
        RaceData("Kyoto",    "Kyoto Umamusume Stakes",    distance=1400, grade=3, turf=True),
    ],
    # Turn 47 — March First Half
    47: [
        RaceData("Nakayama", "Nakayama Umamusume Stakes", distance=1600, grade=3, turf=True),
        RaceData("Nakayama", "Ocean Stakes",              distance=1200, grade=3, turf=True),
        RaceData("Chukyo",   "Kinko Sho",                 distance=2000, grade=4, turf=True),
    ],
    # Turn 48 — March Second Half
    48: [
        RaceData("Nakayama", "Nikkei Sho",                distance=2500, grade=4, turf=True),
        RaceData("Chukyo",   "Takamatsunomiya Kinen",     distance=1200, grade=5, turf=True),
        RaceData("Hanshin",  "Osaka Hai",                 distance=2000, grade=5, turf=True),
        RaceData("Hanshin",  "Hanshin Daishoten",         distance=3000, grade=4, turf=True),
        RaceData("Nakayama", "March Stakes",              distance=1800, grade=3, turf=False),
    ],
    # Turn 49 — April First Half
    49: [
        RaceData("Hanshin",  "Antares Stakes",            distance=1800, grade=3, turf=False),
        RaceData("Nakayama", "Lord Derby Challenge Trophy", distance=1600, grade=3, turf=True),
        RaceData("Hanshin",  "Hanshin Umamusume Stakes",  distance=1600, grade=4, turf=True),
    ],
    # Turn 50 — April Second Half
    50: [
        RaceData("Kyoto",     "Milers Cup",               distance=1600, grade=4, turf=True),
        RaceData("Kyoto",     "Tenno Sho (Spring)",       distance=3200, grade=5, turf=True),
        RaceData("Fukushima", "Fukushima Umamusume Stakes", distance=1800, grade=3, turf=True),
    ],
    # Turn 51 — May First Half
    51: [
        RaceData("Tokyo",   "Victoria Mile",              distance=1600, grade=5, turf=True),
        RaceData("Tokyo",   "Keio Hai Spring Cup",        distance=1400, grade=4, turf=True),
        RaceData("Niigata", "Niigata Daishoten",          distance=2000, grade=3, turf=True),
    ],
    # Turn 52 — May Second Half
    52: [
        RaceData("Tokyo", "Meguro Kinen",                 distance=2500, grade=4, turf=True),
        RaceData("Kyoto", "Heian Stakes",                 distance=1900, grade=3, turf=False),
    ],
    # Turn 53 — June First Half
    53: [
        RaceData("Tokyo",   "Yasuda Kinen",               distance=1600, grade=5, turf=True),
        RaceData("Tokyo",   "Epsom Cup",                  distance=1800, grade=3, turf=True),
        RaceData("Hanshin", "Mermaid Stakes",             distance=2000, grade=3, turf=True),
        RaceData("Hanshin", "Naruo Kinen",                distance=2000, grade=3, turf=True),
    ],
    # Turn 54 — June Second Half
    54: [
        RaceData("Ooi",      "Teio Sho",                  distance=2000, grade=5, turf=False),
        RaceData("Hanshin",  "Takarazuka Kinen",          distance=2200, grade=5, turf=True),
        RaceData("Hakodate", "Hakodate Sprint Stakes",    distance=1200, grade=3, turf=True),
    ],
    # Turn 55 — July First Half
    55: [
        RaceData("Chukyo",    "CBC Sho",                  distance=1200, grade=3, turf=True),
        RaceData("Hakodate",  "Hakodate Kinen",           distance=2000, grade=3, turf=True),
        RaceData("Chukyo",    "Procyon Stakes",           distance=1400, grade=3, turf=False),
        RaceData("Fukushima", "Tanabata Sho",             distance=2000, grade=3, turf=True),
    ],
    # Turn 56 — July Second Half
    56: [
        RaceData("Chukyo",  "Chukyo Kinen",               distance=1600, grade=3, turf=True),
        RaceData("Niigata", "Ibis Summer Dash",           distance=1000, grade=3, turf=True),
        RaceData("Sapporo", "Queen Stakes",               distance=1800, grade=3, turf=True),
    ],
    # Turn 57 — August First Half
    57: [
        RaceData("Sapporo", "Elm Stakes",                 distance=1700, grade=3, turf=False),
        RaceData("Kokura",  "Kokura Kinen",               distance=2000, grade=3, turf=True),
        RaceData("Niigata", "Sekiya Kinen",               distance=1600, grade=3, turf=True),
    ],
    # Turn 58 — August Second Half
    58: [
        RaceData("Sapporo", "Sapporo Kinen",              distance=2000, grade=4, turf=True),
        RaceData("Sapporo", "Keeneland Cup",              distance=1200, grade=3, turf=True),
        RaceData("Kokura",  "Kitakyushu Kinen",           distance=1200, grade=3, turf=True),
    ],
    # Turn 59 — September First Half
    59: [
        RaceData("Nakayama",  "Keisei Hai Autumn Handicap", distance=1200, grade=4, turf=True),
        RaceData("Hanshin",   "Centaur Stakes",           distance=1200, grade=4, turf=True),
        RaceData("Longchamp", "Prix Foy",                 distance=2400, grade=4, turf=True),
        RaceData("Niigata",   "Niigata Kinen",            distance=2000, grade=3, turf=True),
    ],
    # Turn 60 — September Second Half
    60: [
        RaceData("Nakayama", "Sprinters Stakes",          distance=1200, grade=5, turf=True),
        RaceData("Nakayama", "All Comers",                distance=2200, grade=4, turf=True),
    ],
    # Turn 61 — October First Half
    61: [
        RaceData("Hanshin", "Elk Stakes",                 distance=1600, grade=3, turf=True),
        RaceData("Tokyo",   "Fuchu Himba Stakes",         distance=1800, grade=4, turf=True),
        RaceData("Kyoto",   "Kyoto Daishoten",            distance=2400, grade=4, turf=True),
        RaceData("Tokyo",   "Mainichi Okan",              distance=1800, grade=4, turf=True),
    ],
    # Turn 62 — October Second Half
    62: [
        RaceData("Morioka", "Dirt Sprint",                distance=1200, grade=5, turf=False),
        RaceData("Tokyo",   "Tenno Sho (Autumn)",         distance=2000, grade=5, turf=True),
        RaceData("Tokyo",   "Fuji Stakes",                distance=1600, grade=4, turf=True),
        RaceData("Kyoto",   "Swan Stakes",                distance=1400, grade=4, turf=True),
    ],
    # Turn 63 — November First Half
    63: [
        RaceData("Kyoto",     "Queen Elizabeth II Cup",   distance=2400, grade=5, turf=True),
        RaceData("Nakayama",  "Stayer Stakes",            distance=3600, grade=4, turf=True),
        RaceData("Tokyo",     "Copa Republica Argentina", distance=2500, grade=4, turf=True),
        RaceData("Fukushima", "Fukushima Kinen",          distance=2000, grade=3, turf=True),
        RaceData("Kyoto",     "Miyako Stakes",            distance=1800, grade=3, turf=False),
        RaceData("Tokyo",     "Musashino Stakes",         distance=1600, grade=3, turf=False),
        RaceData("Oi",        "JBC Sprint",               distance=1200, grade=5, turf=False)
    ],
    # Turn 64 — November Second Half
    64: [
        RaceData("Kyoto",  "Mile Championship",           distance=1600, grade=5, turf=True),
        RaceData("Tokyo",  "Japan Cup",                   distance=2400, grade=5, turf=True),
        RaceData("Kyoto",  "Keihan Hai",                  distance=1200, grade=3, turf=True),
    ],
    # Turn 65 — December First Half
    65: [
        RaceData("Chukyo",   "Champions Cup",             distance=1800, grade=5, turf=False),
        RaceData("Nakayama", "Capella Stakes",            distance=1200, grade=3, turf=False),
        RaceData("Hanshin",  "Challenge Cup",             distance=2000, grade=3, turf=True),
        RaceData("Chukyo",   "Chunichi Shimbun Hai",      distance=2000, grade=3, turf=True),
        RaceData("Nakayama", "Turquoise Stakes",          distance=1600, grade=3, turf=True),
    ],
    # Turn 66 — December Second Half
    66: [
        RaceData("Nakayama", "Arima Kinen",               distance=2500, grade=5, turf=True),
        RaceData("Ooi",      "Tokyo Daishoten",           distance=2000, grade=5, turf=False),
        RaceData("Hanshin",  "Hanshin Cup",               distance=1400, grade=4, turf=True),
    ],
}

races_by_turn_name = {turn_id: {data.name.strip(): data for data in races} for turn_id, races, in SCHEDULES.items()}
