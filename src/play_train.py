import game
import neural_net
import time
import random
import time
import copy

# create value function, and load weights previously saved
net = neural_net.Net([198, 40, 1])
net.load()
count = 0
won = 0

# run through 1000 games
while count < 1000:
	count += 1
	gammon = game.Game()
	moves = 0
	actions_list = []
	states = []
	r1, r2 = (0,0)
	turn = 0
	# logic for first roll
	# each player rolls a die, and the largest roll gets to go first
	# keep rolling if tie
	while r1 == r2:
		r1, r2 = gammon.roll_dice()
		if r1 > r2:
			turn = 1
		elif r2 > r1:
			turn = 0
	start = 1
	# add first state to list of states for eligibility trace
	if turn == 1:
		states.append(gammon.get_inputs(turn))
	# use over variable so can set it like a flag for games that go over 500 moves
	# these games are probably stuck in some sort of infinite loop of attacking-bar-attacking
	# this only happens once every 1500 games or so
	over = 0
	while not over:
		# get actions for a given dice roll
		# starting roll is different from every subsequent roll
		actions = []
		if start:
			actions = gammon.get_actions((r1, r2), turn)
			start = 0
		else:
			roll = gammon.roll_dice()
			actions = gammon.get_actions(roll, turn)
		action = None
		# if there are actions available, the loop through and apply each one
		# take the state that results from each action and feed it through the value function
		# which is the neural network of inputs arranged to be a representation of the board state
		# one set of inputs could map to more than 1 board state due to how number of pieces at points on the board are encoded
		if len(actions) > 0:
			# keep track of the values that result from feeding the applied action's state through the value function
			# this is a 1-ply search due to the time it was taking to complete a 2-ply search
			# to make this 2-ply all we have to due is save the resulting states instead of values resulting from them
			# then at each state, apply each of the 21 possible unique dice rolls (actions), to get a set of states that could result from that state
			# then feed each of those states through the value function and weight it by probability of the given dice roll (1/18 or 1/36)
			# then pick the value that minimizes the value for opponent, and the value that maximizes the value for yourself (agent)
			values = []
			for a in actions:
				gammon.apply_action(a, turn)
				values.append(net.feedforward(gammon.get_inputs(turn))[0])
				gammon.undo_action(a, turn)
				gammon.last_attacked = 0
			if turn == 1:
				action = actions[values.index(max(values))]
			else:
				action = actions[values.index(min(values))]
			# take the action that was deemed the "best" action
			gammon.apply_action(action, turn)
			moves += 1
			actions_list.append((action, turn))
			# add state to list of states for eligibility trace
			if turn == 1:
				states.append(gammon.get_inputs(turn))
		# switch turns and check for game over
		turn = (turn + 1) % 2
		over = gammon.game_over()
		if moves > 500:
			over = 1
	# reverse states to walk back through and create eligibility trace
	states.reverse()
	lamda = .3
	# loss = 0 reward, win = 1 reward
	reward = 0	
	if gammon.off_pieces[1] == 15:
		won += 1
		print "1 won.  {0}/{1}".format(won, count)
		reward = 1
	else:
		print "0 won"
	# loop through all the states (backwards) 
	for i in range(len(states)-1, 0, -1):
		if i != len(states)-1:
			# define reward in terms of self so as to build up discount factor on future rewards
			reward = (1 - lamda) * net.feedforward(states[i]) + lamda * reward
			# apply learning
			net.do_td(states[i-1], net.feedforward(states[i]), reward, .1)
		else:
			# apply final reward if terminal state
			net.do_td(states[i-1], reward, reward, .1)
# save network weights
net.save()
