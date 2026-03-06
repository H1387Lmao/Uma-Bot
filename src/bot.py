from discord.ext import bridge, commands
import discord
from uicord import *
from pathlib import Path
import json, sys
from .views.state import view_state

PREFIXES = [
    "devuma ",
    "dev "
]

Developers = [
    735679718506102881,
    1252175358741057586
]

class Uma(bridge.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.playing_status = discord.Game(name="Umamusume: Pretty Derby")

        super().__init__(
            command_prefix=commands.when_mentioned_or(*PREFIXES),
            intents=intents,
            activity=self.playing_status,
            help_command=None,
            chunk_guilds_at_startup=True,
            case_insensitive=True
        )

        
    async def on_ready(self):
        print("Ready as", self.user)
        
        emojis = await self.fetch_emojis()
        self.em = {v.name: v for v in emojis}

        print("Fetched Emojis | Count:", len(self.em))

        view_state.emojis = self.em
   
    def cmd(self, **kwargs):
        dev = kwargs.pop("dev", False)
        def decorator(func):
            async def wrapper(ctx: bridge.Context, *args, **kwargs):
                if dev and ctx.author not in Developers:
                    return
                return await func(ctx, *args, **kwargs)
            print("added", kwargs.get("name") or func.__name__)
            return self.bridge_command(**kwargs)(func)
        return decorator
