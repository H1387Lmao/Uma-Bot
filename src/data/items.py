from ..views.state import view_state

Items=[
    ("monies", 10000),
    ("carats", 1000),
    "sprint_shoe",
    "mile_shoe",
    "medium_shoe",
    "long_shoe",
    "dirt_shoe"
]

ITEMS_BY_ID=dict()

class Item:
    def __init__(
        self, id, capacity
    ):
        ITEMS_BY_ID[id]=self
        print("added item", id, capacity)
        self.name = id.replace("_", " ").title()
        self.id = id
        self.capacity=capacity
    @property
    def emoji(self):
        return view_state.bot.get_em("items_"+self.id, "❓")

ITEMS = [Item(item, 10) if isinstance(item, str) else Item(*item) for item in Items]
