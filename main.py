from src import Uma, views
import sys, atexit, signal
from uicord import state
import discord
uma = Uma()

@uma.cmd(
    name="start",
    description="Start Your Career as a Trainer!",
    dev=True
)
async def start_adventure(ctx):
    await ctx.respond(
        view=views.prof(
            {}, ctx.author.id
        )
    )

state.DEV_IDS.append(735679718506102881)

def exit_handler():
    pass

signal.signal(signal.SIGINT, lambda: sys.exit(1))
atexit.register(exit_handler)

uma.run(
  "MTQ1NjMwMzc5NzY5NjU5NDA2MQ.GLVJd4.XP1fJE4WDLRwqY-cKFlpR_DuirBc41KUX_1hb0"
)

