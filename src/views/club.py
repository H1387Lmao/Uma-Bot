from .state import view_state
from uicord import *
from .translations import tr
from .pages import _back_button, pagination_buttons
from ..club import Club
from ..utils import get_fan_graph
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
        _formed_club = Club(
            ctx.user.id, [], info, [],
            color=int(h[:6], 16)
        )
        c = view_state.bot.database.setdefault("clubs", {})
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

def club(prof, uid, page=0, is_view=False):
    if prof['club'] is None:
        return no_club(prof, uid)
    _club = view_state.bot.database["clubs"][prof['club']]

    elements = []
    containers = []

    match page:
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
