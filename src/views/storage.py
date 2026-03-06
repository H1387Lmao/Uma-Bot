from uicord import *
from .translations import *
from .pages import page_buttons
from .state import view_state
import discord as dsc

TRAINEES=0
SUPPORTS=1

def storage(parent, prof, uid, page=0, **kwargs):
	title = Text(tr(prof['lang'], page+STORAGE_OFF))
	buttons = [
		Button(emoji=view_state.emojis['ui_roll1x'], label=None),
		Button(emoji=view_state.emojis['ui_roll10x'], label=None)
	]
	return View(
		Container(
			title,
			ActionRow(*buttons),
			*page_buttons(storage, MAXPAGES=1, BACK=parent)
		)
	)
