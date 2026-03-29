from src import Uma, views, card, utils
import sys, atexit, signal
from uicord import state, View, Container, MediaGallery, MediaGalleryItem, Text
import discord
import os

uma = Uma()

@uma.cmd(
    name="start",
    description="Start Your Career as a Trainer!",
    dev=True
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
    await ctx.defer()
    await utils.CleanerContext.cleanup_all()
    os.execv(sys.executable, [sys.executable] + sys.argv)

state.DEV_IDS.append(735679718506102881)

def exit_handler():
    pass

signal.signal(signal.SIGINT, lambda: sys.exit(1))
atexit.register(exit_handler)

uma.run(
  "MTQ1NjMwMzc5NzY5NjU5NDA2MQ.GLVJd4.XP1fJE4WDLRwqY-cKFlpR_DuirBc41KUX_1hb0"
)

