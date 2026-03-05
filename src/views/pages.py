import inspect
from uicord import Button, ActionRow, Separator, interaction

#⤫△○◎

def page_buttons(PARENT, *, MAXPAGES=0, BACK=None):
    frame = inspect.currentframe().f_back
    args = frame.f_locals.copy()  # copy to avoid mutation
    print(args)
    page = args.get('page', 0)

    components = []

    # LEFT BUTTON (Previous page)
    left = Button("◀",
        disabled=page == 0,
    )

    @interaction(left)
    async def _left(ctx):
        # decrement page and recall parent generically
        args["page"]-=1
        await ctx.response.edit_message(
            view=PARENT(**args)
        )

    # RIGHT BUTTON (Next page)
    right = Button("▶",
        disabled=page == MAXPAGES,
    )

    @interaction(right)
    async def _right(ctx):
        # increment page and recall parent generically
        args["page"]+=1
        await ctx.response.edit_message(
            view=PARENT(**args)
        )

    # BACK BUTTON (optional)
    if BACK:
        back_btn = Button("⤾")

        @interaction(back_btn)
        async def _back(ctx):
            # call BACK function with same arguments
            await ctx.response.edit_message(view=BACK(**args))

        components.insert(back_btn)
    components.extend([left, right])

    return [Separator(), ActionRow(*components)]
