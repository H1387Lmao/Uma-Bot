from typing import Any
import discord
from ..utils import safe_get_user
from uicord import View, Container, ActionRow, Button, interaction, Text
from ..bot import Uma
from ..views.translations import tr  # pyright: ignore[reportUnknownVariableType]
from ..views.state import view_state

InviteOnly = 0
Public = 1

primitives = str|bool|int

class Club:
	def __init__(
		self,
		owner_id: int,
		member_ids: list[int],
		info: dict[str, primitives]
	):

		self.privacy: primitives = info.setdefault('privacy', InviteOnly)
		self.name: primitives = info['name']
		self.description: primitives = info.setdefault('description', '')

		self.owner = None
		self.member_ids: list[int] = member_ids
		self.members = []
		self.owner_id: int = owner_id

		self.bot: Uma = view_state.bot

	async def load_members(self):
		self.owner: discord.Member | None = await safe_get_user(self.bot, self.owner_id)
		self.members: list[discord.User | discord.Member | None] = [ 
			await safe_get_user(bot, member) for member in self.member_ids
		]
	def calculate_fans(self):
		self.fans = 0
		for member_id in self.member_ids:
			prof = self.bot.database[str(member_id)]

			self.fans += prof['stats']['fans']
	def invite_view(self, prof: dict[str, Any]) -> View:  # pyright: ignore[reportExplicitAny]
		accept  = Button(tr('club.view.accept', 0, prof))
		decline = Button(tr('club.view.decline', 0, prof))

		@interaction(accept)  # pyright: ignore[reportUntypedFunctionDecorator]
		async def _accept(ctx: discord.Interaction):  # pyright: ignore[reportUnusedFunction]
			await ctx.response.edit_message(
				view=View(
					Container(
						Text("Successfully Responded!")
					)
				)
			)
			assert ctx.user is not None
			self.members.append(ctx.user)
			self.member_ids.append(ctx.user.id)

		@interaction(decline)  # pyright: ignore[reportUntypedFunctionDecorator]
		async def _decline(ctx: discord.Interaction):  # pyright: ignore[reportUnusedFunction]
			await ctx.response.edit_message(
				view=View(
					Container(
						Text("Successfully Responded!")
					)
				)
			)

		return View(
			Container(
				Text(f"# {tr('club.view.invite_msg', 0, prof)}"),
				ActionRow(
					accept, decline
				)
			)
		)
	async def invite_user(self, ctx, id: int):
		user: discord.Member | None = await safe_get_user(bot, id)
		if user is None:
			return False
		prof: dict[str, Any] = self.bot.database[str(user.id)]  # pyright: ignore[reportUnknownVariableType]
		if prof['clubs'] != None:
			return False
		try:
			_ = await user.send(view=self.invite_view(prof))  # pyright: ignore[reportCallIssue]
		except discord.Forbidden:
			return False
		else:
			return True