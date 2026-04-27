from uicord import *
from ..data import ITEMS
from .state import view_state

import time
import discord

class RequestView(View):
    def __init__(self, user, item):
        super().__init__()
        emoji = view_state.bot.get_em("items_"+item)
        self.add(
            Container(
                Section(
                    Text(f"## Club Notification\n### {user.mention} is asking for 10 {emoji}"),
                    accessory=Thumbnail(
                        url=emoji.url
                    )
                ),
                ActionRow(
                    discord.ui.Button(
                        label="Send",
                        custom_id=f"request_item:{user.id}:{item}"
                    )
                )
            )
        )

def request(prof, uid, requested="monies"):
    last_req = prof.setdefault(
        "last_req_time", 0
    )
    if (last_req-28800)>5: #8 hours
        return View("cooldown, message not implemented")
    item_choices=Choices(
        options=[
            discord.SelectOption(
                label=item.name, emoji=item.emoji,
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
                "Can only send requests on servers!"
            )
        #prof["last_req_time"]=time.time()
        await i.channel.send(
            view=RequestView(
                user = i.user,
                item = requested
            )
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
