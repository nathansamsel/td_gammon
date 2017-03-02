import game
import neural_net
import human_agent
import time
import random

net = neural_net.Net([198, 40, 1])
gammon = game.Game()
human = human_agent.Human()
print "\n\nStarting game...\n\n"
# 2 players roll dice, the largest goes first using the roll
# r1 is white, r2 is black
r1, r2 = (0,0)
turn = 0
# keep rolling if get same
while r1 == r2:
	r1, r2 = gammon.roll_dice()
	print "Human rolled a {0}, Computer rolled a {1}".format(r1, r2)
	if r1 > r2:
		print "Human gets first turn!\n"
		turn = 1
	elif r2 > r1:
		print "Computer gets first turn!\n"
		turn = 0
start = 1
zero_actions = []
one_actions = []
while not gammon.game_over():
	actions = []
	roll = gammon.roll_dice()
	if start:
		actions = gammon.get_actions((r1, r2), turn)
	else:
		actions = gammon.get_actions(roll, turn)
	action = None
	if turn == 1:
		# Human chooses action
		print "Human's turn!"
		if start:
			print "Human rolled a {0}".format((r1, r2))
		else:
			print "Human rolled a {0}".format(roll)
		if len(actions) > 0:
			action = human.get_action_choices(actions)
			gammon.apply_action(action, turn)
		else:
			print "No available actions"
	else:
		# Computer chooses action
		print "Computer's turn!"
		if start:
			print "Computer rolled a {0}".format((r1, r2))
		else:
			print "Computer rolled a {0}".format(roll)
		if len(actions) > 0:
			print "Available actions: {0}".format(actions)
			action = random.choice(actions)
			print "Computer's action choice: {0}".format(action)
			gammon.apply_action(action, turn)
	if turn == 0:
		zero_actions.append(action)
	else:
		one_actions.append(action)
	print "Gameboard state: {0}\n\n".format(gammon.board)
	start = 0
	turn = (turn + 1) % 2
print "\nGame Over!!!"
