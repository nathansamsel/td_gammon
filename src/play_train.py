import game
import neural_net
import time
import random

net = neural_net.Net([198, 40, 2])
count = 0
while count < 100000:
	count += 1
	gammon = game.Game()


	r1, r2 = (0,0)
	turn = 0
	while r1 == r2:
		r1, r2 = gammon.roll_dice()
		if r1 > r2:
			turn = 1
		elif r2 > r1:
			turn = 0
	start = 1
	moves = 0
	

	while not gammon.game_over():
		actions = []
		if start:
			actions = gammon.get_actions((r1, r2), turn)
			start = 0
		else:
			roll = gammon.roll_dice()
			actions = gammon.get_actions(roll, turn)
		action = None
		if len(actions) > 0:
			values = []
			# like a 1 ply expecti-minimax? just see the value of the possible states that result from each action, choose the max or min values depending on player
			for a in actions:
				gammon.apply_action(a, turn)
				# could search further, through next chance node to opponents possible moves here
				values.append(net.feedforward(gammon.get_inputs(turn))[turn])
				gammon.undo_action(a, turn)
			max_val = 0
			max_index = 0
			min_val = 1
			min_index = 0
			for i in range(0, len(values)):
				if turn == 0 and max_val < values[i]:
					max_val = values[i]
					max_index = i
				elif turn == 1 and min_val > values[i]:
					min_val = values[i]
					min_index = i
			if turn == 0:
				action = actions[max_index]
			else:
				action = actions[min_index]
			inputs_before = gammon.get_inputs(turn)
			gammon.apply_action(action, turn)
			net.do_td(inputs_before, net.feedforward(gammon.get_inputs(turn)), .1)
			moves += 1
		turn = (turn + 1) % 2
