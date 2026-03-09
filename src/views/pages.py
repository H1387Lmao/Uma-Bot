import functools
from uicord import *
from .state import view_state
from .translations import tr


def error(prof, uid, label, back_button=None, back_view_factory=None):
    title = tr('errors.' + label, 0, prof)
    description = tr('errors.' + label, 1, prof)

    components = []
    if back_button:
        components.append(back_button)
    elif back_view_factory:
        components.append(_create_back_button(prof['lang'], back_view_factory))

    content = Container(Text(f"## **{title}**\n-4 {description}"))
    if components:
        content = Container(content, ActionRow(*components))

    return View(content, owner=uid)


def pagination_buttons(
    parent_factory,
    max_pages,
    lang,
    current_page=0,
    loop=False,
    back_factory=None
):
    components = []

    if back_factory is not None:
        components.append(_create_back_button(lang, back_factory))

    if parent_factory is not None:
        left = Button("◀", disabled=(current_page == 0 and not loop))
        right = Button("▶", disabled=(current_page >= max_pages and not loop))

        @interaction(left)
        async def _left(ctx):
            next_page = current_page - 1
            if loop:
                next_page %= (max_pages + 1)
            await ctx.response.edit_message(
                view=parent_factory(page=next_page)
            )

        @interaction(right)
        async def _right(ctx):
            next_page = current_page + 1
            if loop:
                next_page %= (max_pages + 1)
            await ctx.response.edit_message(
                view=parent_factory(page=next_page)
            )

        components.extend([left, right])

    return [Separator(), ActionRow(*components)]


def _create_back_button(lang, view_factory):
    emoji = view_state.bot.get_em("ui_back")
    button = Button(emoji=emoji, text=tr("ui.label", 0, lang))

    @interaction(button)
    async def _back(ctx):
        await ctx.response.edit_message(view=view_factory())

    return button
