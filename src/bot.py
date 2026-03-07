from discord.ext import bridge, commands
import discord
from uicord import *
from pathlib import Path
import json, sys
from .views.state import view_state
from .views.translations import tr, SUPPORTED_LANGS

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
        view_state.bot = self

        
    async def on_ready(self):
        print("Ready as", self.user)
        
        emojis = await self.fetch_emojis()
        self.em = {v.name: v for v in emojis}

        print("Fetched Emojis | Count:", len(self.em))

        view_state.emojis = self.em

    def get_em(self, emoji_name, default=None):
        return view_state.emojis.get(emoji_name, default)

    def get_uma(self, uma_name):
        return view_state.emojis.get(
            uma_name.replace(" ", "_").lower(),
            ":horse:"
        )
   
    def cmd(self, **kwargs):
        dev = kwargs.pop("dev", False)
        def decorator(func):
            async def wrapper(ctx: bridge.Context, *args, **kwargs):
                if dev and ctx.author not in Developers:
                    return
                return await func(ctx, *args, **kwargs)
            _name = kwargs.get("name") or func.__name__
            print("adding command: ", _name)

            aliases=[]
            for lang in SUPPORTED_LANGS:
                name = tr(f"cmd.{_name}", 0, lang)
                if name == _name:
                    print(f"skipped translation [{lang}]: {name}")
                    continue
                if '[' not in name:
                    aliases.append(name)
                    print(f"added translation [{lang}]: {name}")
            kwargs['aliases'] = aliases
            if not dev:
                self.bridge_command(**kwargs)(func)
            else:
                self.command(**kwargs)(func)
        return decorator
