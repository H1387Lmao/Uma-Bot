from uicord import *
from ..data import ITEMS, ITEMS_BY_ID
from .state import view_state
import time
import discord

class RequestView(View):
    def __init__(self, user, item_id, timestamp, _donators):
        super().__init__()
        item = ITEMS_BY_ID[item_id]
        emoji = item.emoji
        total = 0
        donators = ""
        for (id, amount) in _donators.items():
            donators+=f"{id};{amount},"
            total+=amount
        donators=donators[:-1] #remove extra comma

        self.add(
            Container(
                Section(
                    Text(f"## Club Notification\n### {user.mention} is asking for {item.capacity} {emoji}"),
                    Text(f"-# People donated {total}/{item.capacity}{emoji}"),
                    accessory=Thumbnail(
                        url=emoji.url
                    )
                ),
                ActionRow(
                    discord.ui.Button(
                        label="Donate",
                        custom_id=f"request_item:{user.id}:{item_id}:{timestamp}:{donators}"
                    )
                ),
                Text(f"-# Expiry: <t:{timestamp+28800}:R>")
            )
        )

def request(prof, uid, requested="monies"):
    last_req = prof.setdefault(
        "last_req_time", 0
    )
    if (last_req-28800)>5: #8 hours
        return View(Text("cooldown, message not implemented"))
    item_choices=Choices(
        options=[
            discord.SelectOption(
                label=f"{item.capacity} "+item.name, emoji=item.emoji,
                default=item.id == requested,
                value=item.id
            )
            for item in ITEMS
        ]
    )
    @interaction(item_choices)
    async def _switch(i):
        await i.response.edit_message(
            view=request(
                prof, uid, item_choices.picked
            )
        )
        
    send_button=Button("Send", color=Colors.Green)
    @interaction(send_button)
    async def _send(i):
        if i.guild is None:
            return await i.respond(
                "Can only send requests on servers!",
                ephemeral=True
            )
        prof["last_req_time"]=int(time.time())
        await i.channel.send(
            view=RequestView(
                user = i.user,
                item_id = requested,
                timestamp = prof["last_req_time"],
                _donators = {}
            )
        )
        return await i.respond(
            f"Sent! Wait for it to expire <t:{prof["last_req_time"]}:R>",
            ephemeral=True
        )

        
    return View(
        Container(
            Text("### Send an item request"),
            ActionRow(
                item_choices
            ),
            ActionRow(
                send_button
            )
        )
    )

view_state.views.RequestView=RequestView
