from src import Uma, views, view_profile, utils, shell, dev, debug
import sys, atexit, signal
from uicord import *
import discord
import os, asyncio
import io, time
import textwrap
import traceback
from contextlib import redirect_stdout
from dotenv import load_dotenv
import psutil
from src.views.trade import start_trade
from src.trading import Trade

load_dotenv()

async def main():

    uma = Uma(
        dev="--dev" in sys.argv #wtf is this temporary shi
    )

    TOKEN = os.getenv("TOKEN")

    @uma.cmd(
        name="carats_add",
        force_prefixcmd=True
    )
    @uma.dev_only
    async def add_c(ctx, target: discord.Member, amount: int=500):
        uma.database[str(target.id)]["stats"]["carats"]+=amount
        await ctx.respond(
            f"successfully given " 
             "{target.display_name}"
             "{amount} carats", 
        ephemeral=True)

    @uma.cmd(
        no_exclude=True,
        no_delete=True,
        name="trade",
        description="Trade items with another player"
    )
    async def trade(ctx, target: discord.Member):
        if str(target.id) not in uma.database:
            return await ctx.respond(
                "Target has no profile!",
                ephemeral=True
            )
        elif str(ctx.author.id) not in uma.database:
            return await ctx.respond(
                "You haven't made a profile yet!",
                ephemeral=True
            )
        prof = uma.database[str(ctx.author.id)]
        tprof = uma.database[str(target.id)]
        trade = Trade(ctx.author, target, prof, tprof)
        await ctx.respond(
            view=start_trade(trade)
        )

    @uma.cmd(
        no_exclude=True,
        no_delete=True,
        name="info",
        description="View System Info"
    )
    async def bot_info(ctx):
        await ctx.defer()
        proc = psutil.Process(os.getpid())
    
        active_count = uma.activity_tracker.count
        guild_count = len(uma.guilds)
        ping = uma.latency
        users = len([i for i in uma.database.keys() if i.isdigit()])

        database_size = uma.get_file_size(uma.db_path)
        memory_usage = proc.memory_info().rss
        
        await ctx.respond(
            view=View(
                Container(
                    Section(
                    Grid(
                        texts=[
                            GridItem(
                                str(active_count),
                                "Active Users"
                            ),
                            GridItem(
                                str(guild_count),
                                "Server Count"
                            ),
                            GridItem(
                                str(users),
                                "Users"
                            ),
                            GridItem(
                                f"{ping:2f}s",
                                "Latency"
                            ),
                            GridItem(
                                database_size,
                                "Database File"
                            ),
                            GridItem(
                                f"{memory_usage/ (1024 * 1024):.2f} MB",
                                "RAM Usage"
                            )
                        ]
                    ),
                        accessory=Thumbnail(
                            url=uma.user.avatar.url
                        )
                    )
                )
            )
        )
    @uma.cmd(
        name="start",
        description="Start Your Career as a Trainer!",
        dev=False
    )
    async def start_adventure(ctx):
        await views.prof(ctx, uma.database, ctx.author.id)

    @uma.cmd(
        name="profile",
        no_exclude=True,
        no_delete=True,
        description="Shows a member or your trainer card",
    )
    async def prof(ctx, member: discord.Member|None=None):
        target = member or ctx.author
    
        if str(target.id) not in uma.database:
            await ctx.respond(view=View(
                Container(
                    Text("Couldn't find that user's profile!")
                )
            ), ephemeral=True)
        else:
            await ctx.defer()
            prof = uma.database[str(target.id)]
            await ctx.respond(
                view=view_profile(
                    target, prof, target.id==ctx.author.id
                )
            )
        
    @uma.cmd(
        name="reset",
        dev=True,
        no_exclude=True,
        no_delete=True,
        description="Restart the bot"
    )
    async def reset(ctx: utils.CleanerContext):
        uma.save()
        await ctx.defer()
        await utils.CleanerContext.cleanup_all()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @uma.cmd(
        name="panel",
        dev=True,
        no_exclude=True,
        no_delete=True,
        description="Panel for developers"
    )
    async def panel(ctx):
        await dev.Panel(
            dev.DEV_CMDS
        ).show(ctx)

    state.DEV_IDS.append(735679718506102881)

    def exit_handler(*args):
        uma.save()
        try:
            asyncio.run(
                uma.close()
            )
        except:
            exit()
        
    signal.signal(signal.SIGINT, exit_handler)
    if os.name!="nt":
        signal.signal(signal.SIGTSTP, exit_handler)

    atexit.register(exit_handler)

    await uma.start(TOKEN)

asyncio.run(main())
