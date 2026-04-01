from .state import view_state
from uicord import *
from .translations import tr
import discord

channel_id = 1488811152287727617

class FeedbackModal(Modal):
    def __init__(self, channel):
        super().__init__("Contact Us")

        self.channel=channel

        self.feedback_type = Choices(
            options=[
                discord.SelectOption(
                    label="Feedback",
                    description="Feedback you have about the bot",
                    default=True
                ),
                discord.SelectOption(
                    label="Bug Report",
                    description="Bugs/Exploits you found in the bot",
                ),
                discord.SelectOption(
                    label="Inquiry",
                    description="Questions you have about the bot",
                ),
                discord.SelectOption(
                    label="Other",
                    description="Not specified"
                )
            ]
        )
        self.add_item(
            "Contact Type",
            item=self.feedback_type
        )
        self.add_input("Information", "long")

        self.more_info = discord.ui.CheckboxGroup(
            options=[
                discord.CheckboxGroupOption(
                    label="Anonymous Send",
                    value="Yes",
                    description="Send the feedback as anonymous"
                )
            ],
            required=False
        )

        self.add_item("More options", self.more_info)

    async def callback(self, ctx):
        await ctx.respond("-# Sent!\n-# Wait for developers to read!", ephemeral=True)

        await self.channel.send(
            view=self.get_view(ctx, self.values)
        )
    def get_view(self, ctx, values):
        user = ctx.user.display_name if not values[2] else "Anonymous"
        if ctx.guild:
            guild = ctx.guild.name if not values[2] else "Anonymous Server"
        else:
            guild = "Direct Message"

        return View(
            Container(
                Text(f"# **<@&1477697620330680564>**\n-# From `{user}` in (**{guild}**)"),
                Text(f"-# `{values[0][0]}`"),
                Text(f">>> {values[1]}")
            )
        )

async def _send_feedback(ctx):
    channel = view_state.bot.get_channel(channel_id)
    await ctx.response.send_modal(
        FeedbackModal(channel)
    )
