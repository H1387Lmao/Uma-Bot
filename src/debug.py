import io
import discord
from uicord import *
import asyncio

DEBUG_CHANNEL = 1476406061874286674

async def send_ch(bot, *args, **kwargs):
    try:
        channel = bot.get_channel(DEBUG_CHANNEL)

        if channel is None:
            print("Channel not found")
            return

        await channel.send(*args, **kwargs)
    except Exception as e:
        print("send_ch error:", e)
        
def show_guilds(bot):
    bot.loop.create_task(send_ch(
        bot,
        view=View(
            Container(
                Text("# All Guilds Within"),
                Text(f">>> {"\n".join(map(lambda g: g.name, bot.guilds))}")
            )
        )
    ))

def show_members(bot):
    lines = []

    for guild in bot.guilds:
        for member in guild.members:
            lines.append(
                f"{member.display_name} | {member.name} ({guild.name})"
            )

    lines = list(dict.fromkeys(lines))

    text = "\n".join(lines)

    async def _send():
        channel = bot.get_channel(DEBUG_CHANNEL)
        if channel is None:
            print("Channel not found")
            return

        file = discord.File(
            fp=io.BytesIO(text.encode("utf-8")),
            filename="members.txt"
        )

        await channel.send(
            content="Member list:",
            file=file
        )

    bot.loop.create_task(_send())
