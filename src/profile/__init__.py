from uicord import *
from ..views.state import view_state

def view_profile(user, prof, _is_owner=False):
    bot = view_state.bot
    
    edit_prof=Button(
        text="Edit",
        emoji=bot.get_em("ui_edit"),
        color=Colors.Blue
    )

    profile_settings = prof["settings"].setdefault("profile",{
        "uma": "Special Week"
    })

    umoji=bot.get_uma(profile_settings["uma"])
    carats=prof["stats"]["carats"]
    club = prof["club"].name if prof["club"] else "No Club"

    stats = str(bot.get_em("carat"))+" Carats"+f" {carats}"
    
    return View(Container(
        Section(
            Text(
                f"# {umoji} **{user.display_name}**"
            ),
            Text(f"-# **{bot.get_em("ui_club")}** {club}"),
            accessory=Thumbnail(
                url=user.avatar.url
            )
        ),
        Separator(),
        Text(
            stats
        ),
        ActionRow(edit_prof) if _is_owner else None,
        ), owner=user.id
    )
