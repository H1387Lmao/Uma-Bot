from .state import view_state
from uicord import *
from .translations import tr
from .pages import _back_button, pagination_buttons, error
from ..club import Club
from ..utils import get_fan_graph
from .lb import leaderboard
import hashlib
import discord

class CreateClub(Modal):
    def __init__(self, prof):
        super().__init__( 
            tr("club.create.title",0,prof)
        )
        self.prof=prof

        self.add_input(
            tr("club.create.name",0,prof)
        )
        self.add_input(
            tr("club.create.description",0,prof),
            "long"
        )
        self.add_item(
            tr("club.create.photo",0,prof),
            item=discord.ui.FileUpload(
                min_values=1,
                max_values=1,
                required=False
            )
        )
        self.add_item(
            tr("page.single_words",0,prof),
            item=discord.ui.CheckboxGroup(
                options=[
                    discord.CheckboxGroupOption(
                        label=tr("club.create.public",0,prof),
                        description=tr("club.create.public_desc",0,prof),
                        value="IsPublic"
                    )
                ],
                required=False
            )
        )
    async def callback(self, ctx):
        v = self.values
        info = {
            "privacy": int("IsPublic" in self.values[3]),
            "name": self.values[0],
            "description": self.values[1],
            "photo": None if len(self.values[2])==0 else self.values[2][0].url
        }
        h=hashlib.md5(str(info["photo"]).encode('utf-8')).hexdigest()
        c = view_state.bot.database.setdefault("clubs", {})
        _formed_club = Club(
            ctx.user.id, [], info, [],
            color=int(h[:6], 16),
            index=len(c)
        )
        c[len(c)]=_formed_club

        self.prof["club"]=len(c)-1
        await ctx.response.edit_message(
            view=club(self.prof, ctx.user.id)
        )

def no_club(prof, uid):
    create = Button(tr("club.buttons.create",0,prof))
    @interaction(create)
    async def _create(i):
        await i.response.send_modal(
            CreateClub(prof)
        )
    return View(Container(
        Section(
            Text(
                tr("error.club.not_found", 0, prof)
            ),
            accessory=Thumbnail(
                url="https://gametora.com/images/404.png"
            )
        ),
        ActionRow(
            create,
            _back_button(prof, lambda: 
                view_state.views.home(prof, uid)
            )
        ),
        color=0x15AA15
    ),owner=uid)

def club_header(prof, c) -> list[discord.ui.ViewItem]:
    return [
        Section(
            Text(f"# **{c.name}**\n-# **{c.description}**"),
            accessory=Thumbnail(
                url=c.photo
            )
        )
    ]

def club_stats(prof, uid, page, is_view, current=7, _club=None):
    graphs = MediaGallery()
    days = current
    graphs.add_item(
        url=get_fan_graph(_club.get_timespan(
            days
        ))
    )
    rd = RadioButtons(
        options=[
            RadioButtonOption(
                label=tr("club.page.entrycount", 0, prof, i),
                default=current == i,
                value=i
            )
            for i in [7, 14, 31, 45]
        ],
        custom_on=view_state.bot.get_em("radio_on"),
        custom_off=view_state.bot.get_em("radio_off")
    )
    @interaction(rd)
    async def _switch(i):
        await i.response.edit_message(
            view=club_stats(prof, uid, page, is_view, rd.value, _club)
        )

    return View(
        Container(
            *club_header(prof, _club),
            rd,
            graphs
        ),
        Container(
            ActionRow(_back_button(
                prof,
                lambda: club(prof, uid, page, is_view),
            ))
        )
    )

def club(prof, uid, page=0, is_view=False, _passed_club_id=None):
    if not is_view and prof['club'] is None:
        return no_club(prof, uid)

    _club = view_state.bot.database["clubs"][
        _passed_club_id or prof["club"]
    ]

    elements = []
    containers = []

    bot=view_state.bot

    if not is_view:
        leave  = Button("Leave", color=Colors.Red)
        invite = Button("Invite")
        
        @interaction(leave)
        async def _leave(i):
            if _club.member_ids and i.user.id==_club.owner_id:
                return await i.response.edit_message(
                    view=error(
                        prof, uid, "club.cant_leave",
                        back_view_factory=lambda: club(prof, uid, page, is_view)
                    )
                )
            prof["club"]=None
            await ctx.response.edit_message(
                view=club(prof, uid, page, True, _club.index)
            )
        @interaction(invite)
        async def _invite(i):
            invite_modal = Modal("Invite a user")
            a=Choices(discord.ComponentType.user_select, required=True)
            invite_modal.add_item(
                "User",
                item=a
            )
            @interaction(invite_modal)
            async def _inv(ctx):
                if await _club.invite_user(a.picked):
                    await ctx.response.edit_message(
                        view=club(prof, uid, page, is_view)
                    )
                else:
                    return await ctx.response.edit_message(
                        view=error(
                            prof, uid, "club.cant_invite",
                            back_view_factory=lambda: club(prof, uid, page, is_view)
                        )
                    )
            await i.response.send_modal(
                modal=invite_modal
            )
    else:
        invite=None
        leave = Button(
            "Join",
            color=Colors.Green,
            disabled=not _passed_club.privacy
        )
        @interaction(leave)
        async def _join(i):
            prof["club"]=_passed_club_id
            await i.response.edit_message(
                view=club(prof, uid, page)
            )

    match page:
        case 0:
            lb = Button(tr("page.club.btns", 2, prof))
            @interaction(lb)
            async def _view_lb(i):
                await i.response.edit_message(
                    view=leaderboard(
                        prof,
                        uid,
                        lambda: club(prof, uid, page, is_view, ),
                        2
                    )
                )
            elements.append(
                ActionRow(lb)
            )
        case 2:
            stats = Button(tr("club.buttons.view_stats", 0, prof))
            @interaction(stats)
            async def _view(i):
                await i.response.edit_message(
                    view=club_stats(prof, uid, page, is_view, _club=_club)
                )
            elements.append(
                ActionRow(stats)
            )
    return View(
        Container(
            *club_header(prof, _club),
            discord.ui.Separator(
                spacing=discord.SeparatorSpacingSize.large
            ),
            Text(f"## **{tr("club.page.titles", page, prof)}**"),
            *elements,
            color=_club.color
        ),
        *containers,
        Container(
            ActionRow(
                invite, leave
            ),
            *pagination_buttons(
                lambda p: club(prof, uid, p, is_view),
                2,
                prof,
                page,
                back_factory=lambda: view_state.views.home(prof, uid, 1),
                loop=True
            )[1:]
        )
    )

def club_search(prof, uid):
    return View(Text("wip"))
