from ..views.state import view_state

# arcade

# minigames:

# mines
# coinflip


class Minigame:
    def __init__(self, owner=None, bid=0):
        self.owner = owner
        self.bid = bid

        self.payout=0
    def set_payout(self, am):
        self.payout=am

    async def won(self):
        bot = view_state.bot
        prof = bot.get_user_prof(self.owner)
        if not prof:
            return
        prof["stats"]["carats"]+=am
            
class Mines(Minigame):
    def __init__(self, owner=None, bid=0):
        super().__init__(owner, bid)
