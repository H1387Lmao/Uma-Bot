import discord

async def safe_get_user(bot: discord.Client, id: int) -> discord.Member | None:
	user = bot.get_user(id)
	if not user:
		user = await bot.fetch_user(id)
	return user