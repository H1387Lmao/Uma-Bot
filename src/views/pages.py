import functools
from uicord import *
from .state import view_state
from .translations import tr

def error(prof, uid, label, back_button=None, back_view_factory=None):
    title = tr('errors.' + label, 0, prof)
    description = tr('errors.' + label, 1, prof)
    components = []
    if back_button: components.append(back_button)
    elif back_view_factory: components.append(_create_back_button(prof["settings"]['lang'], back_view_factory))
    title_text = Text(f"## **{title}**\n-# {description}")
    return View(Container(title_text, ActionRow(*components)) if components else Container(title_text), owner=uid)

def pagination_buttons(parent_factory, max_pages, lang, current_page=0, loop=False, back_factory=None, far_buttons=False):
    components = []
    if back_factory: components.append(_create_back_button(lang, back_factory))
    if parent_factory:
        first = Button("≪", disabled=(current_page == 0))
        left = Button("◀", disabled=(current_page == 0 and not loop))
        right = Button("▶", disabled=(current_page >= max_pages and not loop))
        last = Button("≫", disabled=(current_page >= max_pages))

        @interaction(first)
        async def _first(ctx): await ctx.response.edit_message(view=parent_factory(0))
        @interaction(left)
        async def _left(ctx):
            p = (current_page - 1) % (max_pages + 1) if loop else current_page - 1
            await ctx.response.edit_message(view=parent_factory(p))
        @interaction(right)
        async def _right(ctx):
            p = (current_page + 1) % (max_pages + 1) if loop else current_page + 1
            await ctx.response.edit_message(view=parent_factory(p))
        @interaction(last)
        async def _last(ctx): await ctx.response.edit_message(view=parent_factory(max_pages))
        
        if far_buttons:
            if back_factory: return [Separator(), ActionRow(components[0]), ActionRow(first, left, right, last)]
            return [Separator(), ActionRow(first, left, right, last)]
        components.extend([left, right])
    return [Separator(), ActionRow(*components)]

def _create_back_button(lang, view_factory):
    emoji = view_state.bot.get_em("ui_back")
    button = Button(emoji=emoji, text=tr("ui.label", 0, lang))
    @interaction(button)
    async def _back(ctx): await ctx.response.edit_message(view=view_factory())
    return button
