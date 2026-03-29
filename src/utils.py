import discord
from discord.ext import bridge
from .views.state import view_state
import discord

view_state.last_messages = {}
view_state.all_messages = set()

class CleanerContext:
    def __init__(self, ctx):
        self.ctx = ctx
        self.author = ctx.author
        self.channel = ctx.channel
        self.guild = ctx.guild
        self.user = ctx.author
        self.reply = self.respond

        self.interaction = getattr(ctx, "interaction", None)

    def _key(self):
        return f"{self.channel.id}{self.author.id}"

    async def _cleanup_previous(self):
        prev = view_state.last_messages.get(self._key())
        if prev:
            bot_msg, user_msg = prev

            for msg in (bot_msg, user_msg):
                if msg:
                    try:
                        await msg.delete()
                    except:
                        pass

    async def _store(self, bot_msg):
        user_msg = getattr(self.ctx, "message", None)

        view_state.last_messages[self._key()] = (bot_msg, user_msg)

        if bot_msg:
            view_state.all_messages.add(bot_msg)
        if user_msg:
            view_state.all_messages.add(user_msg)

        return bot_msg

    async def send(self, *args, **kwargs):
        await self._cleanup_previous()
        msg = await self.ctx.send(*args, **kwargs)
        return await self._store(msg)

    async def respond(self, *args, **kwargs):
        await self._cleanup_previous()

        msg = await self.ctx.respond(*args, **kwargs)

        if isinstance(msg, discord.Message):
            return await self._store(msg)

        if self.interaction:
            try:
                m = await self.interaction.original_response()
                return await self._store(m)
            except:
                pass

        return msg

    async def defer(self, *args, **kwargs):
        await self._store(None)
        return await self.ctx.defer(*args, **kwargs)

    @staticmethod
    async def cleanup_all():
        for msg in list(view_state.all_messages):
            try:
                await msg.delete()
            except:
                pass

        view_state.all_messages.clear()
        view_state.last_messages.clear()
        
async def safe_get_user(bot: discord.Client, id: int) -> discord.Member | None:
	user = bot.get_user(id)
	if not user:
		user = await bot.fetch_user(id)
	return user
