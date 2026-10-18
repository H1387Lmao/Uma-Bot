from uicord import *
from ..trading import *
from .state import view_state
from discord import SelectOption

def get_trades(slots):
    bot = view_state.bot
    carats_emoji = bot.get_em("carats")

    trade_list = ""
    for trade_item in slots:
        if trade_item.item_type=="carats":
            trade_list+=f"-# {carats_emoji} x{trade_item.amount}\n"
        elif trade_item.item_type=="uma":
            name = trade_item.item_id
            if name != "???":
                trade_list+=f"-# {bot.get_uma(name)}{name} x{trade_item.amount}\n"
            else:
                trade_list+="-# ??? (Not Specified)\n"

    return trade_list.strip() or "-# No Items"

def edit_list(_ctx, ongoing_trade):
    bot = view_state.bot
    owner = _ctx.user

    prof = ongoing_trade.t1prof if owner == ongoing_trade.t1 else ongoing_trade.t2prof

    carats = prof["stats"]["carats"]

    info = Modal("Trade")
    for i, trade_item in enumerate(ongoing_trade.slots[owner.id]):
        if trade_item.item_type=="carats":
            info.add_input(
                "Carats",
                default=str(trade_item.amount),
                description=f"You have {carats} carats",
                required=True
            )
        elif trade_item.item_type=="uma":
            info.add_item(
                f"Uma",
                item=Choices(
                    options=[
                        SelectOption(
                            emoji=bot.get_uma(n),
                            label=n,
                            value="uma_"+n,
                            default=n==trade_item.item_id
                        ) for n in list(prof["inventory"]["umas"].keys())[:25]
                    ],
                    placeholder="Select Uma",
                    required=True
                )
            )
    @interaction(info)
    async def submit(ctx):
        values = info.values
        ongoing_trade.refresh_slots(ctx.user.id)
        ongoing_trade.t1ready=False
        ongoing_trade.t2ready=False
        
        for i, v in enumerate(values):
            if isinstance(v, list):
                v=v[0] # select option returns list for some reason
            if v.startswith("uma_"):
                am = ongoing_trade.add_uma(
                    ctx.user, uma:=v.removeprefix("uma_")
                )
                if am>prof["inventory"]["umas"][uma][0]:
                    return await ctx.respond(
                        f"Failed to save! Insufficient amount (uma: `{uma}`)",
                        ephemeral=True
                    )
                ongoing_trade.remove_unknown_item(ctx.user.id, "uma")
            elif v.isdigit():
                if int(v)>prof["stats"]["carats"]:
                    return await ctx.respond(
                        "Failed to save! Insufficient amount",
                        ephemeral=True
                    )
                ongoing_trade.set_carats(
                    ctx.user, int(v)
                )
            else:
                return await ctx.respond(
                    "Failed to save! Invalid number",
                    ephemeral=True
                )
        await _ctx.message.edit(
            view=start_trade(ongoing_trade)
        )
        return await ctx.response.defer()
    return info
    
def start_trade(ongoing_trade):
    bot = view_state.bot

    add_item = Button("Add Item", color=Colors.Grey)
    confirm  = Button("Confirm", color=Colors.Green)
    edit     = Button("Edit", color=Colors.Blue, emoji=bot.get_em("ui_edit"))
    cancel   = Button("Cancel Trade", color=Colors.Red)

    title    = Text(f"## Ongoing Trade!")
    owner, target = ongoing_trade.t1, ongoing_trade.t2

    t1_conf = bot.get_em("ui_tick") if ongoing_trade.t1ready else ""
    t2_conf = bot.get_em("ui_tick") if ongoing_trade.t2ready else ""

    @interaction(cancel)
    async def _cancel(ctx):
        await ctx.response.edit_message(
            view=View(Text(f"Trade cancelled by {ctx.user.mention}!"))
        )

    @interaction(confirm)
    async def _confirm(ctx):
        if not ongoing_trade.has_values():
            return await ctx.respond(
                view=View(
                    Container(
                        Text("One or more values hasnt been filled!")
                    )
                )
            )
        if ctx.user.id==owner.id:
            ongoing_trade.t1ready=True
        elif ctx.user.id==target.id:
            ongoing_trade.t2ready=True            

        if ongoing_trade.t1ready and ongoing_trade.t2ready:
            ongoing_trade.send_items()

            confirm.disabled=True
            edit.disabled=True
            add_item.disabled=True
            cancel.disabled=True
            title.content="## Trade Complete!"
            
            await ctx.response.edit_message(
                view=confirm.view
            )
        else:
            await ctx.response.edit_message(
                view=start_trade(ongoing_trade)
            )

    @interaction(edit)
    async def _edit(ctx):
        if len(ongoing_trade.slots[ctx.user.id])==0:
            return await ctx.respond(
                "Add an item first!",
                ephemeral=True,
            )
        await ctx.response.send_modal(
            modal=edit_list(ctx, ongoing_trade)
        )

    @interaction(add_item)
    async def add(ctx):
        if len(ongoing_trade.slots[ctx.user.id])>=5:
            return await ctx.respond(
                "A single trade can only have 5 items!",
                ephemeral=True
            )
    
        await ctx.respond(
            view=trade_add_item(
                ongoing_trade, ctx
            ),
            ephemeral=True
        )
    
    return View(
        Container(
            title,
            Separator(),
            Section(
                Text(f"## {t1_conf}{owner.display_name}'s Side\n"),
                Text(
                    get_trades(list(ongoing_trade.slots.values())[0])
                ),
                accessory=Thumbnail(
                    url=owner.avatar.url
                )
            ),
            Separator(),
            Section(
                Text(f"## {t2_conf}{target.display_name}'s Side"),
                Text(
                    get_trades(list(ongoing_trade.slots.values())[1])
                ),
                accessory=Thumbnail(
                    url=target.avatar.url
                )
            ),
            ActionRow(
                add_item, edit, confirm, cancel
            )
        ),
        owner=[owner.id, target.id]
    )

def trade_add_item(
    trade,
    original_ctx=None,
    selected_item_type="carats"
):

    bot = view_state.bot
    carats_emoji = bot.get_em("carats")
    spe= bot.get_uma("Special Week")

    ItemType = Choices(
        options=[
            SelectOption(
                label="Carats",
                emoji=carats_emoji,
                description="Carats",
                default=selected_item_type=="carats",
                value="carats"
            ),
            SelectOption(
                label="Umamusume",
                emoji=spe,
                description="Horse girl",
                default=selected_item_type=="uma",
                value="uma"
            ),
        ],
        placeholder="Item Type"
    )
    @interaction(ItemType)
    async def set_item(ctx):
        await ctx.response.edit_message(
            view=trade_add_item(
                trade, original_ctx, ItemType.picked
            )
        )
    
    confirm = Button(
        "Confirm", Colors.Green
    )

    @interaction(confirm)
    async def _confirm(ctx):
        match selected_item_type:
            case "carats":
                trade.set_carats(ctx.user, 0)
            case "uma":
                trade.add_uma(ctx.user)
        try:
            await original_ctx.message.edit(
                view=start_trade(trade)
            )
        except:
            await original_ctx.edit(
                view=start_trade(trade)
            )

        trade.t1ready=False
        trade.t2ready=False

        ItemType.disabled=True
        confirm.disabled=True

        await ctx.response.edit_message(
            view=confirm.view
        )

        await ctx.edit_original_response(
            view=confirm.view, delete_after=0
        )

    return View(
        Container(
            ActionRow(ItemType),
            ActionRow(confirm)
        )
    )

