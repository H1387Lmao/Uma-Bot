# pages.py
import inspect
from uicord import Button, ActionRow, Separator, interaction
from .state import view_state
from .translations import tr

def error(prof, uid, label, back_button=None, back_fn=None):
    _back_button = back_button or page_back(locals_, back_fn, prof)
    title       = tr('errors.'+label, 0, prof)
    description = tr('errors.'+label, 1, prof)
    return View(Container(
        Text(f"## **{title}**\n-4 {description}"),
        ActionRow(
            _back_button
        ),
    ), owner=uid)

def page_back(locals_, back_fn, lang):
    back_em  = view_state.bot.get_em("ui_back")
    back_btn = Button(emoji=back_em, text=tr("ui.label", 0, lang))

    sig = inspect.signature(back_fn)
    back_snapshot = {
        k: locals_[k]
        for k in sig.parameters
        if k in locals_ and k != "page"
    }

    @interaction(back_btn)
    async def _back(ctx):
        await ctx.response.edit_message(
            view=back_fn(**back_snapshot)
        )

    return back_btn

def page_buttons(parent_fn=None, *, max_pages=0, back_fn=None):
    frame = inspect.currentframe().f_back
    locals_ = frame.f_locals

    # Only grab args that parent_fn actually accepts
    if parent_fn is not None:
        sig = inspect.signature(parent_fn)
        snapshot = {
            k: locals_[k]
            for k in sig.parameters
            if k in locals_ and k != "page"
        }
    page = locals_.get("page", 0)

    lang = locals_.get("prof", {}).get("lang", None) or locals_.get("lang", None) or "English"

    components = []

    # BACK BUTTON (optional, inserted first)

    # LEFT (previous page)
    left = Button("◀", disabled=page == 0)

    @interaction(left)
    async def _left(ctx):
        await ctx.response.edit_message(
            view=parent_fn(page=page - 1, **snapshot)
        )

    # RIGHT (next page)
    right = Button("▶", disabled=page >= max_pages)

    @interaction(right)
    async def _right(ctx):
        await ctx.response.edit_message(
            view=parent_fn(page=page + 1, **snapshot)
        )
    if back_fn is not None:
        components.append(
            page_back(locals_, back_fn, lang)
        )
    if parent_fn is not None:
        components.extend([left, right])
    
    return [Separator(), ActionRow(*components)]
