print("\033[s\033[0;0d\033[?1049h", end="")

from src import Uma, views
import sys, atexit, signal
from uicord import state
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

@uma.cmd(name="music")
async def play_music(ctx, arg: str, *, a1: str|None=""):
    if arg.lower() not in ["play", "skip", "leave", "autoplay"]:
        return await ctx.respond("Invalid command supplied only: `play, skip, leave, autoplay` are supported")
    if ctx.guild is None:
        return ctx.respond("Not in a guild")
    cmd = arg.lower().strip()
    if cmd=="leave" and ctx.voice_client is None:
        return
    if ctx.author.voice:
        queue = get_queue(ctx.guild.id)
        match cmd:
            case "play":
                await queue.ensure_joined(ctx)
                await queue.add_song(ctx, a1)
            case "leave":
                await queue.leave()
            case "skip":
                await queue.skip(ctx)
            case "autoplay":
                await queue.set_autoplay(ctx)
    else:
        await ctx.send("You must be in a voice channel!")

state.DEV_IDS.append(735679718506102881)

def exit_handler():
    print("\033[?1049l\033[u")

signal.signal(signal.SIGINT, lambda: sys.exit(1))
atexit.register(exit_handler)

uma.run(
  "MTQ1NjMwMzc5NzY5NjU5NDA2MQ.GLVJd4.XP1fJE4WDLRwqY-cKFlpR_DuirBc41KUX_1hb0"
)

