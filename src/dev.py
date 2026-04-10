from uicord import *
import inspect
import discord
DEV_CMDS = {}

class Option:
    def __init__(self, options):
        self.options = options

    def __class_getitem__(cls, items):
        if not isinstance(items, tuple):
            items = (items,)
        return cls(items)

class MultiStr(str):
    pass

def register(
    name=None
):
    def wrapper(func):
        _name=name or func.__name__
        DEV_CMDS[_name]=func
        
    return wrapper

@register(name="Stat Set")
async def set_stat(ctx,
    User: discord.User,
    Stat: Option["Speed", "Stamina", "Power", "Guts", "Wit"],
    Amount: int
):
    await ctx.respond(
        "You have no career, nub",
        ephemeral=True
    )

@register(name="Announce News")
async def announce(ctx,
    Channel: discord.TextChannel,
    Role: discord.Role=None,
    Title: str=None,
    Description: MultiStr="",
    Photo: discord.File=None
):
    Title = Title if not Role else f"{Title} {Role.mention}"
    msg = await Channel.send(
        view=View(Container(
            Text(Title),
            Text(">>> " + Description),
            *([] if Photo is None else [
                MediaGallery(
                    MediaGalleryItem(Photo.url)
                )
            ]), color=0xbb11aa
        ))
    )
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    
class Panel(View):
    def __init__(self, cmds):
        super().__init__()

        self.cmds=[]
        cont = Container(color=0x151588)

        for name, cmd in cmds.items():
            cmd_button=Button(
                name
            )
            @interaction(cmd_button)
            async def _cmd(ctx, cmd=cmd):
                await self.run(ctx, cmd)
            self.cmds.append(cmd_button)
            if len(self.cmds)==5:
                cont.add_item(ActionRow(*self.cmds))
                self.cmds=[]
        if self.cmds:
            cont.add_item(ActionRow(*self.cmds))
        self.add(cont)
    async def run(self, ctx, cmd):
        modal = Modal()

        self.values={}
        self.items={}

        for name, sig in inspect.signature(cmd).parameters.items():
            if name in ["interaction", "i","ctx"]:
                continue

            if sig.default is not inspect.Parameter.empty:
                self.values[name]=sig.default
            else:
                self.values[name]="No Value"

            anno = sig.annotation
            item = None

            if anno in (str, int):
                item=discord.ui.InputText(
                    required=self.values[name] == "No Value"
                )
            elif isinstance(anno, Option):
                item = Choices(
                    options=[
                        Choice(label=str(opt), value=str(opt))
                        for opt in anno.options
                    ],
                    required=self.values[name] == "No Value"
                )
            elif anno == MultiStr:
                item=discord.ui.InputText(
                    style=discord.InputTextStyle.long,
                    required=self.values[name] == "No Value"
                )
            elif anno == discord.File:
                item=discord.ui.FileUpload(
                    min_values=1,
                    max_values=1,
                    required=self.values[name] == "No Value"
                )
            elif anno == bool:
                item=Checkbox()
            else:
                match anno:
                    case discord.User:
                        item=Choices(
                            discord.ComponentType.user_select,
                            required=self.values[name] == "No Value"
                        )
                    case discord.Member:
                        item=Choices(
                            discord.ComponentType.user_select,
                            required=self.values[name] == "No Value"
                        )
                    case discord.TextChannel:
                        item=Choices(
                            discord.ComponentType.channel_select,
                            required=self.values[name] == "No Value"
                        )
                    case discord.Role:
                        item=Choices(
                            discord.ComponentType.role_select,
                            required=self.values[name] == "No Value"
                        )
            self.items[name]=item
            modal.add_item(label=name, item=item)
        @interaction(modal)
        async def _submit(ctx):
            args=[]
            for name, item in self.items.items():
                try:
                    _v = item.picked
                except AttributeError:
                    try:
                        _v = item.value
                    except AttributeError:
                        try:
                            _v = item.values[0]
                        except IndexError:
                            _v = None
                args.append(_v or self.values[name])
            await ctx.respond(
                "Submitted", ephemeral=True
            )
            await cmd(ctx, *args)
        await ctx.response.send_modal(modal)
    async def show(self, ctx):
        self.owner=ctx.author.id
        await ctx.respond(
            view=self, ephemeral=True
        )
