    # storage.py
from uicord import *
from .translations import translator, tr
from .pages import pagination_buttons
from .state import view_state

def storage(parent, prof, uid, page=0):
    # Umamusume
    # Support Cards
    # Items
    # Badges

    title = tr("page.storage.titles", page, prof)
    
    parent_factory = lambda page: storage(parent, prof, uid, page=page)
    back_factory = lambda: parent(prof, uid)
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
            list_umas = "\n".join(
                f"{bot.get_uma(a)}**{a}** ×{b[0]}" for a, b in prof["inventory"]["umas"].items()
            )
            elements = [
                Text(list_umas or tr("page.storage.no_umas"))
            ]
        case _:
            elements=[]

    return View(
        Container(
            Text(f"# {title}"),
            *elements,
            *nav_buttons
        ), owner=uid
    )

view_state.views.storage = storage
