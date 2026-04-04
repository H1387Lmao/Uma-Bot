from .state import view_state
from uicord import *
from .translations import tr
from .pages import _back_button
def no_club(prof, uid):
    return View(
        Section(
            Text(
                tr("error.club.not_found", 0, prof)
            ),
            accessory=Thumnail(
                url="https://gametora.com/umamusume/images/404.png"
            )
        ),
        ActionRow(
            _back_button(prof, lambda: club(prof, uid))
        )
    )

def club(prof, uid):
    if prof['club'] is None:
        return no_club(prof, uid)
    return Text("wtf how did you get here")
