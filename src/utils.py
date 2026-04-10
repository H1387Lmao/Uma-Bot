import discord
from discord.ext import bridge
from .views.state import view_state
import discord
import urllib.parse
import json    

view_state.last_messages = {}
view_state.all_messages = set()

class CleanerContext:
    def __init__(self, ctx):
        self.ctx = ctx
        self.author = ctx.author
        self.channel = ctx.channel
        self.guild = ctx.guild
        self.user = ctx.author
        self.reply = self.respond

        self.interaction = getattr(ctx, "interaction", None)

    def _key(self):
        return f"{self.channel.id}{self.author.id}"

    async def _cleanup_previous(self):
        prev = view_state.last_messages.get(self._key())
        if prev:
            bot_msg, user_msg = prev

            for msg in (bot_msg, user_msg):
                if msg:
                    try:
                        await msg.delete()
                    except:
                        pass

    async def _store(self, bot_msg):
        user_msg = getattr(self.ctx, "message", None)

        view_state.last_messages[self._key()] = (bot_msg, user_msg)

        if bot_msg:
            view_state.all_messages.add(bot_msg)
        if user_msg:
            view_state.all_messages.add(user_msg)

        return bot_msg

    async def send(self, *args, **kwargs):
        await self._cleanup_previous()
        msg = await self.ctx.send(*args, **kwargs)
        return await self._store(msg)

    async def respond(self, *args, **kwargs):
        await self._cleanup_previous()

        msg = await self.ctx.respond(*args, **kwargs)

        if isinstance(msg, discord.Message):
            return await self._store(msg)

        if self.interaction:
            try:
                m = await self.interaction.original_response()
                return await self._store(m)
            except:
                pass

        return msg

    async def defer(self, *args, **kwargs):
        await self._store(None)
        return await self.ctx.defer(*args, **kwargs)

    @staticmethod
    async def cleanup_all():
        for msg in list(view_state.all_messages):
            try:
                await msg.delete()
            except:
                pass

        view_state.all_messages.clear()
        view_state.last_messages.clear()
        
async def safe_get_user(bot: discord.Client, id: int) -> discord.User | None:
    user = bot.get_user(id)
    if not user:
        user = await bot.fetch_user(id)
    return user

def get_fan_graph(timespan):
    chart_config = {
        "type": "line",
        "data": {
            "labels": list(map(str, range(len(timespan)))),
            "datasets": [
                {
                    "data": timespan,
                    "borderColor": "rgba(20, 255, 20, 1)",
                    "backgroundColor": "rgba(10, 225, 10, .5)",
                    "fill": True,
                    "pointRadius": 0,
                    "borderWidth": 4,
                    "lineTension": 0.3
                }
            ]
        },
        "options": {
            "legend": {
                "display": False,
                "labels": {
                    "fontColor": "white"
                }
            },
            "layout": {
                "padding": {
                    "top": 20,
                    "bottom": 20,
                    "left": 20,
                    "right": 20
                }
            },
            "scales": {
                "x": { "display": False, "ticks": { "color": "white" } },
                "y": { "display": True, "ticks": { "color": "white" } }
            }
        }
    }
    
    chart_json = json.dumps(chart_config)
    encoded_chart = urllib.parse.quote(chart_json)
    return f"https://quickchart.io/chart?bkg=%23121212&c={encoded_chart}"

def get_stat_graph(stats):
    labels = [name for name, _ in stats]
    data = [value for _, value in stats]

    colors = [
        "rgba(54,162,235,0.9)",
        "rgba(255,99,132,0.9)",
        "rgba(255,159,64,0.9)",
        "rgba(255,105,180,0.9)",
        "rgba(75,192,192,0.9)",
        "rgba(255,205,86,0.9)",
    ]

    chart_config = {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)],
                "borderWidth": 0
            }]
        },
        "options": {
            "color": "white",
            "legend": {
                "labels": {
                    "fontColor": "white"
                }
            },
            "plugins": {
                "legend": {
                    "labels": {
                        "color": "white"
                    }
                },

                "tooltip": {
                    "titleColor": "white",
                    "bodyColor": "white"
                },

                "datalabels": {
                    "color": "white",
                    "formatter": "function(value){return value;}"
                }
            }
        }
    }

    chart_json = json.dumps(chart_config)
    encoded_chart = urllib.parse.quote(chart_json)

    return f"https://quickchart.io/chart?bkg=%23121212&c={encoded_chart}"

def get_bar_tiles(percentage, precision=7, total_tiles=7, remainder_tiles=[6]):
    percentage = max(0.0, min(1.0, percentage))
    filled_tiles = percentage * total_tiles

    remainder_tiles = set(remainder_tiles or [])
    result = []

    for i in range(total_tiles):
        relative = filled_tiles - i

        if i in remainder_tiles:
            state = 1 if relative >= 1 else 0
        else:
            if relative >= 1:
                state = precision
            elif relative <= 0:
                state = 0
            else:
                state = int(relative * precision)

        result.append(f"bar_{i}_{state}")

    return result
