class Human:
	def __init__(self):
		self.action_history = []
	
	def get_action_choices(self, available_actions):
		# does not check if valid action
		print "Available actions: {0}".format(available_actions)
		action_start = raw_input("Type start: ")
		if action_start != 'bar':
			action_start = int(action_start)
		action_end = raw_input("Type end: ")
		if action_end != 'off':
			action_end = int(action_end)
		return (action_start, action_end)

