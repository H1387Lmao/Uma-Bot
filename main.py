from src import Uma, views
uma = Uma()

@uma.cmd(name="start", dev=True)
async def start_adventure(ctx):
    await ctx.respond(
        view=views.prof(
            {}, ctx.author.id
        )
    )

uma.run(
  "MTQ1NjMwMzc5NzY5NjU5NDA2MQ.GLVJd4.XP1fJE4WDLRwqY-cKFlpR_DuirBc41KUX_1hb0"
)
