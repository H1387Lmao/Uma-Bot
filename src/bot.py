from discord.ext import bridge, commands
import discord
from uicord import *
from pathlib import Path
import json, sys
import asyncio
from .views.state import view_state
from .views.translations import tr, SUPPORTED_LANGS
from .utils import CleanerContext, safe_get_user
from .db import Database

PREFIXES = [
    "uma ",
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

        self.database = Database()
        
        self.view_state = view_state
        self.db_path = Path("database/db.pkl")

        view_state.logger.print(f"[light blue]Loaded Temporary Database")
        self.database.temp_load(self.db_path)
    def save(self):
        self.database.save(str(self.db_path))
        view_state.logger.print(f"[light blue]Saved Database")

    async def on_ready(self):
        view_state.logger.print(f"[light purple]Ready as {self.user}[reset]")

        if self.db_path.exists():
            view_state.logger.print(f"[light blue]Loading Database")
            self.database = await Database.load(self, str(self.db_path))
        else:
            view_state.logger.print(f"[light blue]Created Database")
        emojis = await self.fetch_emojis()
        self.em = {v.name: v for v in emojis}
        self.em["carat"]=self.em["carats"] #use new version

        view_state.logger.print(f"[light purple]Fetched Emojis | Count: {len(self.em)}[reset]")

        view_state.emojis = self.em

    def get_em(self, emoji_name, default=None):
        return view_state.emojis.get(emoji_name, default)

    def get_em_url(self, emoji_name):
        em = self.get_em(emoji_name)
        return em.url if em else None

    def get_uma(self, uma_name):
        return view_state.emojis.get(
            uma_name.replace(" ", "_").lower(),
            ":horse:"
        )
   
    def cmd(self, **kwargs):
        dev = kwargs.pop("dev", False)
        def decorator(func):
            async def wrapper(ctx: bridge.Context, *args, **kwargs):
                if dev and ctx.author.id not in Developers:
                    return
                return await func(CleanerContext(ctx), *args, **kwargs)
            _name = kwargs.get("name") or func.__name__
            view_state.logger.print(f"[light yellow]Adding: {_name}[reset]")

            aliases=[]
            for lang in SUPPORTED_LANGS:
                name = tr(f"cmd.{_name}", 0, lang)
                if name == _name:
                    view_state.logger.print(f"[dark grey]skipped translation [{lang}]: {name}[reset]")
                    continue
                if '[' not in name:
                    aliases.append(name)
                    view_state.logger.print(f"[light green]added translation [{lang}]: {name}[reset]")
            kwargs['aliases'] = aliases
            if not dev:
                self.bridge_command(**kwargs)(wrapper)
            else:
                self.command(**kwargs)(wrapper)
        return decorator
    async def sfetch_user(self, id):
        return await safe_get_user(self, id)
    def run(self, t):
        print("running ts now")
        super().run(t)
