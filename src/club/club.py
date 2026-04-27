from typing import Any
import discord
from ..utils import safe_get_user
from uicord import View, Container, ActionRow, Button, interaction, Text
from ..views.translations import tr  # pyright: ignore[reportUnknownVariableType]
from ..views.state import view_state
import time
from itertools import repeat
from uicord import Colors

InviteOnly = 0
Public = 1

primitives = str|bool|int|None

class Club:
    def __init__(
        self,
        owner_id: int,
        member_ids: list[int],
        info: dict[str, primitives],
        snapshots: list[
            tuple[int, int] #(timestamp, fancount)
        ],
        color: int = 0x676767,
        index: int = 0
    ):
        self.info=info
        self.privacy: primitives = info['privacy']
        self.name: primitives = info['name']
        self.description: primitives = info['description'] or 'No Description'
        self.photo: str = info['photo'] or "https://gametora.com/images/404.png"
        self.owner = None
        self.member_ids: list[int] = member_ids
        self.members = []
        self.owner_id: int = owner_id
        self.snapshots=snapshots
        self.color=color
        self.index=index

        self.bot = view_state.bot
        self.calculate_fans()

    async def load_members(self):
        self.owner: discord.Member | None = await safe_get_user(self.bot, self.owner_id)
        self.members: list[discord.User | discord.Member | None] = [ 
            await safe_get_user(bot, member) for member in self.member_ids
        ]
    def get_member_ids(self):
        return [self.owner_id, *self.member_ids]
    def __reduce__(self):
        return (self.__class__,(
            self.owner_id,
            self.member_ids,
            self.info,
            self.snapshots,
            self.color,
            self.index
        ))
    def calculate_fans(self):
        self.fans = 0
        for member_id in self.member_ids:
            try:
                prof = self.bot.database[str(member_id)]
            except KeyError: continue
            self.fans += prof['stats']['fans']
        self.create_snapshot()
    def create_snapshot(self):
        self.snapshots.append((int(time.time()), self.fans))
    def get_timespan(self, entries=7):
        spans = []
        prev_ts = None
        prev_val = None
    
        for timestamp, snapshot in self.snapshots[max(0, len(
            self.snapshots
        )-entries):]:
            if prev_ts is None:
                prev_ts = timestamp
                prev_val = snapshot
                continue
    
            if abs(timestamp - prev_ts) > 86400 or snapshot != prev_val:
                spans.append(snapshot)
                if len(spans) == entries:
                    break
    
            prev_ts = timestamp
            prev_val = snapshot
    
        if spans:
            if len(spans) < entries:
                spans += [0] * (entries - len(spans))
    
        return spans
    def invite_view(self, prof: dict[str, Any]) -> View:  # pyright: ignore[reportExplicitAny]
        accept  = Button(tr('club.invite.accept', 0, prof), color=Colors.Green)
        decline = Button(tr('club.invite.decline', 0, prof), color=Colors.Red)

        @interaction(accept)  # pyright: ignore[reportUntypedFunctionDecorator]
        async def _accept(ctx: discord.Interaction):  # pyright: ignore[reportUnusedFunction]
            await ctx.response.edit_message(
                view=View(
                    Container(
                        Text(tr("club.msg.success", 0, prof))
                    )
                )
            )
            assert ctx.user is not None
            self.members.append(ctx.user)
            self.member_ids.append(ctx.user.id)
            prof["club"]=self.index

        @interaction(decline)  # pyright: ignore[reportUntypedFunctionDecorator]
        async def _decline(ctx: discord.Interaction):  # pyright: ignore[reportUnusedFunction]
            await ctx.response.edit_message(
                view=View(
                    Container(
                        Text(tr("club.msg.success", 0, prof))
                    )
                )
            )

        return View(
            Container(
                Text(f"# {tr('club.invite.invite_msg', 0, prof, self.name)}"),
                ActionRow(
                    accept, decline
                )
            )
        )
    async def invite_user(self, user=None):
        if user is None:
            return False
        prof: dict[str, Any] = self.bot.database[str(user.id)]  # pyright: ignore[reportUnknownVariableType]
        if prof['club'] != None:
            return False
        try:
            await user.send(view=self.invite_view(prof))
        except discord.Forbidden:
            return False
        else:
            return True
