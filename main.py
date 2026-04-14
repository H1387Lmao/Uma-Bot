from src import Uma, views, card, utils, shell, dev, debug
import sys, atexit, signal
from uicord import *
import discord
import os, asyncio
import io
import textwrap
import traceback
from contextlib import redirect_stdout

uma = Uma(
    dev="--dev" in sys.argv #wtf is this temporary shi
)

TOKEN = "MTQ1NjMwMzc5NzY5NjU5NDA2MQ.GLVJd4.XP1fJE4WDLRwqY-cKFlpR_DuirBc41KUX_1hb0"

def main():
    if "--dev" not in sys.argv or "--no-tui" in sys.argv: #wtf is this temporary shi
        uma.run(TOKEN)
    else:
        asyncio.run(
            shell.start_bot(
                uma,
                TOKEN
            )
        )


if "--no-cmds" in sys.argv:
    main()
    sys.exit()

@uma.cmd(
    name="start",
    description="Start Your Career as a Trainer!",
    dev=False
)
async def start_adventure(ctx):
    await views.prof(ctx, uma.database, ctx.author.id)

@uma.cmd(
    name="profile",
    description="Shows a member or your trainer card",
)
async def prof(ctx, member: discord.Member|None=None):
    target = member or ctx.author
    
    if str(target.id) not in uma.database:
        await ctx.respond(view=View(
            Container(
                Text("Couldn't find that user's profile!")
            )
        ))
    else:
        await ctx.defer()
        prof = uma.database[str(target.id)]
        _u_c = prof["career"]

        em = uma.get_uma("Haru Urara")
        _fields = {
            "Fans": prof["stats"]["fans"],
            "Carats": prof["stats"]["carats"],
            "Level": prof["stats"]["exp"]//1000
        }
        if _u_c:
            em = uma.get_uma(_u_c.name)
        if prof["club"]:
            _fields["Club"]=prof["club"].name
        if not os.path.exists("./bin"):
            os.mkdir("./bin")
        _out = card(
            target.avatar.url,
            em.url,
            target.name,
            _fields,
            "...",
            output_path=f"./bin/{target.id}.png"
        )
        await ctx.respond(
            view=View(Container(
                MediaGallery(
                    MediaGalleryItem(f"attachment://{target.id}.png")
                )
            )), files=[discord.File(f"bin/{target.id}.png")]
        )
        _out.unlink()
        
@uma.cmd(
    name="reset",
    dev=True,
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
        uma.loop.create_task(
            uma.close()
        )
        
signal.signal(signal.SIGINT, exit_handler)
if os.name!="nt":
    signal.signal(signal.SIGTSTP, exit_handler)

atexit.register(exit_handler)

main()
