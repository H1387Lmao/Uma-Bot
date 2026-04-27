from uicord import *
from .pages import *
from .state import view_state

#modes include, global players, global clubs, club players

def get_leaderboard_list(prof, mode):
    _items = []
    bot = view_state.bot

    match mode:
        case 0:
            for i, profile in bot.database.items():
                if not i.isdigit():
                    continue
                _items.append(
                    (profile["name"], profile["stats"]["fans"])
                )
        case 1:
            for i, club in bot.database["clubs"].items():
                _items.append(
                    (club.name, club.fans)
                )
        case 2:
            for member_id in bot.database["clubs"][prof["club"]].get_member_ids():
                profile = bot.database[str(member_id)]
                _items.append(
                    (profile["name"], profile["stats"]["fans"])
                )
                
               
    items = []

    for i, p in enumerate(sorted(
        _items,
        key=lambda k: k[1],
        reverse=True
    )):
        items.append((i+1, *p))
    return items

def leaderboard(prof, uid, b, mode=0, pages=[0,0,0]):
    def switch_page(p):
        pages[mode]=p
        return leaderboard(prof, uid, mode, pages)
    items = get_leaderboard_list(prof, mode)

    modes = RadioButtons(
        options=[
            RadioButtonOption(
                label="Players",
                default=mode==0,
                value=0
            ),
            RadioButtonOption(
                label="Clubs",
                default=mode==1,
                value=1
            ),
            RadioButtonOption(
                label="Members",
                default=mode==2,
                value=2,
                disabled=prof["club"] is None
            )
        ],
        custom_on=view_state.bot.get_em("radio_on"),
        custom_off=view_state.bot.get_em("radio_off")
    )

    @interaction(modes)
    async def _switch_mode(ctx):
        await ctx.response.edit_message(
            view=leaderboard(
                prof, uid, b, modes.value, pages,
            )
        )

    display=""
    for rank, name, value in items:
        display+=f"### {rank} **{name}**\n-# {value} Fans\n"
    title=["Players", "Clubs", "Members"][mode]
    
    return View(
        Container(
            Text(f"## **{title}**\n"+display),
        ),
        Container(
            modes,
            *pagination_buttons(
                switch_page,
                len(items)//10,
                prof,
                pages[mode],
                back_factory=b,
                loop=True
            )
        ),
        owner=uid
    )
