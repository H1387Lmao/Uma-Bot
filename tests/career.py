import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.career import *

if __name__=="__main__":
	c = Career.create_new('Haru Urara', 67, [])
	for i in range(66):
		goal_info = c.get_needed_goal()
		print('turn:',c.turn,goal_info or 'No goal info')
	
		c.advance()

