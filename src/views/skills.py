from uicord import *
from .translations import *
from .pages import pagination_buttons, _back_button
from ..skills import MOST_EXPENSIVE_SKILLS
from .state import view_state

def create_skill_container(
    prof, uid, page, skill, skills_buying, **kwargs
):
    sp=prof["career"].skill_points
    bot = view_state.bot
    inc = Button(
        text=None, emoji=bot.get_em("ui_inc"),
        disabled=(skill.id in skills_buying) or (skill.price > sp)
    )
    dec = Button(
        text=None, emoji=bot.get_em("ui_dec"),
        disabled=skill.id not in skills_buying
    )
    am = Button(
        text=str(skills_buying.get(skill.id, 0)),
        disabled=True
    )
    async def update_shop(i):
        await i.response.edit_message(
            view=skill_shop(
                prof,
                uid,
                page,
                skills_buying,
                **kwargs
            )
        )
    @interaction(inc)
    async def _inc(i):
        skills_buying.setdefault(skill.id, 0)
        kwargs["total"]+=skill.price
        skills_buying[skill.id]+=1
        await update_shop(i)
    @interaction(dec)
    async def _dec(i):
        skills_buying[skill.id]-=1
        kwargs["total"]-=skill.price
        await update_shop(i)

    return Container(
        Section(
            Text(f"# **{skill.name}** {skill.color()}\n-# {skill.price} SP"),
            accessory=Thumbnail(
                bot.get_em(
                    skill.icon, skill.icon
                ).url
            )
        ),
        Separator(),
        Text(f"-# *{skill.desc}*"),
        ActionRow(
            dec, am, inc
        )
    )

def skill_shop(prof, uid, page=0, skills_buying={}, **kwargs):
    per_page = 2

    skills_displayed = MOST_EXPENSIVE_SKILLS[
        page*per_page:
        (page+1)*per_page
    ]

    containers=[]

    for skill in skills_displayed:
        skill = create_skill_container(prof, uid, page, skill, skills_buying, **kwargs)
        containers.append(skill)
        
    PActionRow=pagination_buttons(
        lambda p: skill_shop(prof, uid, p, skills_buying, **kwargs),
        len(MOST_EXPENSIVE_SKILLS)//per_page,
        prof,
        page,
        loop=True,
        back_factory = lambda: view_state.views.career(
            prof, uid
        )
    )[1]

    Checkout=Button(
        tr("career.skills.buy", 0, prof),
        color=Colors.Green,
        disabled=kwargs["total"]==0
    )

    @interaction(Checkout)
    async def _checkout(i):
        for skid, am in skills_buying.items():
            if not am: continue
            career.skills.append(skid)
        career.skill_points-=kwargs["total"]
        await i.response.edit_message(
            view=skill_shop(prof, uid, page, total=0)
        )
    career = prof["career"]

    PActionRow.add(
        Checkout
    )
    return View(
        Container(
            Text(f"# {tr("career.skills.title", 0, prof)}\n"
                f"-# **{career.skill_points-kwargs["total"]} {tr("training.skill_pts_label", 0, prof)}**"
            ),
        ),
        *containers,
        Container(
            PActionRow
        )
    )
