from discord.ext import bridge, commands, tasks
import discord
from uicord import *
from pathlib import Path
import json, sys, time, os
import asyncio
from .views.state import view_state
from .views.translations import tr, SUPPORTED_LANGS
from .utils import CleanerContext, safe_get_user
from .data import ITEMS_BY_ID
from functools import wraps
from .db import Database
import traceback

MAIN_PRF = [
    "uma "
]
DEV_PRF = [
    "dev "
]

Developers = [
    735679718506102881,
    1252175358741057586
]

class ActivityTracker:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.users = {}

    def mark(self, user):
        self.users[user.id] = time.monotonic() + self.timeout

    def active(self, user):
        expiry = self.users.get(user.id)

        if expiry is None:
            return False

        if expiry <= time.monotonic():
            self.users.pop(user.id, None)
            return False

        return True

    def cleanup(self):
        now = time.monotonic()

        for user_id, expiry in list(self.users.items()):
            if expiry <= now:
                del self.users[user_id]

    @property
    def count(self):
        self.cleanup()
        return len(self.users)

    @property
    def active_users(self):
        self.cleanup()
        return set(self.users)

class Uma(bridge.Bot):
    def __init__(self, dev=False):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.playing_status = discord.Game(name="Umamusume: Pretty Derby")
        self.dev = dev

        self.activity_tracker = ActivityTracker()
        PREFIXES = DEV_PRF if self.dev else MAIN_PRF
            
        super().__init__(
            command_prefix=commands.when_mentioned_or(*PREFIXES),
            intents=intents,
            activity=self.playing_status,
            help_command=None,
            chunk_guilds_at_startup=True,
            case_insensitive=True
        )
        view_state.bot = self
        if not self.dev:
            self.db_path = Path("database/db.pkl")
        else:
            self.db_path = Path("database/dev.pkl")

        self.database = Database(None, self.db_path)
        
        self.view_state = view_state
        view_state.logger.print(f"[light blue]Loaded Temporary Database")
        self.database.temp_load(self.db_path)

        self._save.start()
    def get_file_size(self, path):
        try:
            bytes_size = os.path.getsize(path)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_size < 1024.0:
                    return f"{bytes_size:.2f} {unit}"
                bytes_size /= 1024.0
        except FileNotFoundError:
            return "File not found."
    @tasks.loop(seconds=30)
    async def _save(self):
        self.save()
        
    @_save.before_loop
    async def before_auto_save(self):
        await self.wait_until_ready()
        await asyncio.sleep(30)
    
    def save(self):
        self.database.save(self.db_path)

    def get_user_prof(self, user):
        if isinstance(user, discord.User):
            p=user.id
        elif isinstance(user, int):
            p=user
        else:
            return None
        prof = self.database.get(str(p))
        return prof

    async def on_ready(self):
        view_state.logger.print(f"[light purple]Ready as {self.user}[reset]")

        if self.db_path.exists():
            view_state.logger.print(f"[light blue]Loading Database")
            self.database = await Database.load(self, self.db_path)
        else:
            view_state.logger.print(f"[light blue]Created Database")
        emojis = await self.fetch_emojis()
        self.em = {v.name: v for v in emojis}
        self.em["carat"]=self.em["carats"] #use new version

        view_state.logger.print(f"[light purple]Fetched Emojis | Count: {len(self.em)}[reset]")

        view_state.emojis = self.em

        view_state.logger.print(f"Servers: "+", ".join(map(lambda a: a.name, self.guilds)))

        @self.before_invoke
        async def track_prefix(ctx):
            if ctx.author.bot:
                    return
            
            self.activity_tracker.mark(ctx.author)
    async def on_error(self, event_name, *args, **kwargs):
        print(f"Error in {event_name}: {args[0]}")
    async def on_interaction(self, interaction):
        self.activity_tracker.mark(interaction.user)
        if interaction.type == discord.InteractionType.component:
            cid = interaction.data.get("custom_id")
            if cid.startswith("request_item:"):
                if not str(interaction.user.id) in self.database:
                    return await interaction.respond(f"You have no account to donate, please use `uma start`!", ephemeral=True)
                _, uid, item_id, timestamp, donators = cid.split(":")
                if str(interaction.user.id)==uid:
                    return await interaction.respond(f"You cant donate to yourself!", ephemeral=True)
                item = ITEMS_BY_ID[item_id]
                print(donators)
                donators = dict(
                    (uid, int(amount))
                    for entry in donators.split(",")
                    if entry
                    for uid, amount in [entry.split(";")]
                ) if donators else {}
                amounted = donators.setdefault(
                    str(interaction.user.id), 0
                )
                total = sum(donators.values())
                
                # donator profile
                dprof = self.database[str(interaction.user.id)]
                
                # receiver profile
                rprof = self.database[str(uid)]
                
                donated = min(item.capacity-total,min(dprof["inventory"]["items"].get(item_id, 0), item.capacity//5))
                if not donated:
                    return await interaction.respond("Unable to donate!", ephemeral=True)
                donators[str(interaction.user.id)]+=donated
                ditems = dprof["inventory"]["items"]
                ritems = rprof["inventory"]["items"]

                ritems.setdefault(item_id, 0)
                ritems[item_id]+=donated
                ditems[item_id]-=donated
                
                await interaction.message.edit(
                    view=view_state.views.RequestView(
                        await self.sfetch_user(uid), item_id, int(timestamp), donators
                    )
                )
                return await interaction.respond(f"Thanks for donating {donated}{item.emoji}", ephemeral=True)

        await self.process_application_commands(interaction)
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
    def get_item(self, prof, id, default=0):
        return prof["inventory"]["items"].setdefault(id, default)
    def get_item_em(self, id):
        return self.get_em("items_"+id)
    def on_error(self, e):
        print("\033[31m", end="")
        traceback.print_exc()
        print("\033[0m", end="")
    def cmd(self, **kwargs):
        dev = kwargs.pop("dev", False)
        is_prefix_forced = kwargs.pop("force_prefixcmd", False)
        no_delete = kwargs.pop("no_delete", False)
        no_remove = kwargs.pop("no_exclude", False)
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                ctx, args=args[0], args[1:]
                if dev and ctx.author.id not in Developers:
                    return
                if no_delete:
                    return await func(ctx, *args, **kwargs)
                return await func(CleanerContext(ctx), *args, **kwargs)
            _name = kwargs.get("name") or func.__name__
            if dev and not self.dev and not no_remove:
                view_state.logger.print(f"[light red]Skipped Developer Branch Command: {_name}[reset]")
                return

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
            if not is_prefix_forced and not dev:
                self.bridge_command(
                    integration_types={
                        discord.IntegrationType.guild_install, 
                        discord.IntegrationType.user_install
                    },
                    contexts={
                        discord.InteractionContextType.guild,
                        discord.InteractionContextType.bot_dm,
                        discord.InteractionContextType.private_channel
                    },
                    **kwargs
                )(wrapper)
            else:
                self.command(**kwargs)(wrapper)
        return decorator
    async def sfetch_user(self, id):
        return await safe_get_user(self, id)
    def run(self, t):
        print("running ts now")
        if self.dev:
            view_state.logger.print(f"[light cyan]Running branch [gold](Developer)[reset]")
        else:
            view_state.logger.print(f"[light cyan]Running branch [dark white](Main)[reset]")
        super().run(t)

    def dev_only(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ctx = args[0]
        
            if ctx.author.id not in Developers:
                return
        
            return await func(*args, **kwargs)
        
        return wrapper
