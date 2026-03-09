from hlog import Logger

class ViewStore:
	pass

class State:
	emojis = {}
	bot = None,
	logger = Logger("Uma Logger")
	views=ViewStore()

view_state = State()
