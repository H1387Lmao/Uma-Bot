    # storage.py
from uicord import *
from .translations import translator, tr
from .pages import pagination_buttons
from .state import view_state
from ..data import SUPPORT_IDS
from .request_item import request
support_costs = [1,2,3,4]
uma_costs = [2,4,8,16]

def view_info(prof, p, pg, upgrading, n, c, l, is_support=False, adding=0):
    bot = view_state.bot
    cost = support_costs if is_support else uma_costs
    t = "umas" if not is_support else "supports"
    a = "star" if not is_support else "diamond"
    
    _star=str(bot.get_em(a))
    _star_dim=str(bot.get_em(f"{a}_dim"))
    _star_none=str(bot.get_em(f"{a}_none"))

    level = l+1 if not is_support else l

    stars = _star*level+_star_dim*adding+_star_none*(5-l-adding)
    _r = bot.get_em("ui_r")
    _l = bot.get_em("ui_l")

    left=Button(
        emoji=_l,
        text=None,
        disabled=adding==0
    )
    
    right=Button(
        emoji=_r, text=None,
        disabled=prof["inventory"][t][n][0]<sum(cost[l:l+adding+1])
    )
    
    upgrade=Button(
        tr("page.storage.upgrade", 0, prof),
        disabled=adding == 0,
        color=Colors.Green
    )

    async def switch(ctx, view):
        await ctx.response.edit_message(
            view=p(prof, ctx.user.id, pg, upgrading)
        )

    @interaction(left)
    async def _left(ctx):
        upgrading[n]=adding-1
        await switch(
            ctx,
            p(prof, ctx.user.id, pg, upgrading)
        )
        
    @interaction(right)
    async def _right(ctx):
        upgrading[n]=adding+1
        await switch(
            ctx,
            p(prof, ctx.user.id, pg, upgrading)
        )

    @interaction(upgrade)
    async def _upgrade(ctx):
        upgrading[n]=0
        prof["inventory"][t][n][1]+=adding
        prof["inventory"][t][n][0]-=sum(cost[l:l+adding])
        await switch(
            ctx,
            p(prof, ctx.user.id, pg, upgrading)
        )
    name = SUPPORT_IDS[n].name if is_support else n
    return [
        Container(
            Section(
                Text(f"# {name}\n**×{c}**{stars}"),
                accessory=Thumbnail(
                    url= (
                        bot.get_uma(name).url \
                        if not is_support else \
                        bot.get_em("sc_"+str(n)).url
                    )
                )
            ),
            ActionRow(
                left, upgrade, right
            )
        )
    ]

def show_supports(prof, uid, page=0, upgrading={}):
    umas_displayed=[]
    umas = prof["inventory"]["supports"]
    for name, (count, level) in list(umas.items())[page*4:page*4+4]:
        adding=upgrading.setdefault(name, 0)
        umas_displayed.extend(
            view_info(prof, show_supports, page, upgrading, name, count, level, True, adding)
        )
    if not umas_displayed:
        umas_displayed = [
            Text(tr("page.storage.no_umas", 0, prof))
        ]

    return View(
        *umas_displayed,
        Container(
            *pagination_buttons(
                lambda p: show_supports(prof, uid, p, upgrading),
                (len(umas)-1)//4,
                prof,
                page,
                loop=True,
                back_factory=lambda: storage(prof, uid, 1)
            )
        ),
        owner=uid
    )

def show_umas(prof, uid, page=0, upgrading={}):
    umas_displayed=[]
    umas = prof["inventory"]["umas"]
    
    for name, (count, level) in list(umas.items())[page*4:page*4+4]:
        adding=upgrading.setdefault(name, 0)
        umas_displayed.extend(
            view_info(prof, show_umas, page, upgrading, name, count, level, False, adding)
        )
    if not umas_displayed:
        umas_displayed = [
            Text(tr("page.storage.no_umas", 0, prof))
        ]

    return View(
        *umas_displayed,
        Container(
            *pagination_buttons(
                lambda p: show_umas(prof, uid, p, upgrading),
                (len(umas)-1)//4,
                prof,
                page,
                loop=True,
                back_factory=lambda: storage(prof, uid, 0)
            )
        )
    )

def storage(prof, uid, page=0):
    # Umamusume
    # Support Cards
    # Items
    # Badges

    title = tr("page.storage.titles", page, prof)
    
    parent_factory = lambda page: storage(prof, uid, page=page)
    back_factory = lambda: view_state.views.home(prof, uid)
    nav_buttons = pagination_buttons(
        parent_factory=parent_factory,
        max_pages=3,
        lang=prof["settings"]["lang"],
        current_page=page,
        loop=True,
        back_factory=back_factory
    )

    bot = view_state.bot

    match page:
        case 0:
            show_list = Button(tr("page.storage.show_umas",0,prof))
            @interaction(show_list)
            async def _show(ctx):
                await ctx.response.edit_message(
                    view=show_umas(prof, uid)
                )
            elements = [
                ActionRow(show_list)
            ]
        case 1:
            show_list = Button(tr("page.storage.show_supports",0,prof))
            @interaction(show_list)
            async def _show(ctx):
                await ctx.response.edit_message(
                    view=show_supports(prof, uid)
                )
            elements = [
                ActionRow(show_list)
            ]
        case 3:
            req_item = Button(
                "Request Item",
                color=Colors.Green
            )
            @interaction(req_item)
            async def _show(ctx):
                await ctx.response.edit_message(
                    view=request(prof, uid)
                )
            elements = [
                ActionRow(req_item)
            ]
        case _:
            elements=[
                Text(tr("page.storage.no_umas", 0, prof))
            ]

    return View(
        Container(
            Text(f"# {title}"),
            *elements,
            *nav_buttons
        ), owner=uid
    )

view_state.views.storage = storage
