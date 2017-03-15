import game
import neural_net
import time
import random

net = neural_net.Net([198, 40, 1])
gammon = game.Game()
print "Starting game..."
# 2 players roll dice, the largest goes first using the roll
# r1 is white, r2 is black
r1, r2 = (0,0)
turn = 0
# keep rolling if get same
while r1 == r2:
	r1, r2 = gammon.roll_dice()
	if r1 > r2:
		turn = 1
	elif r2 > r1:
		turn = 0
start = 1
moves = 0
zero_actions = []
one_actions = []
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
		action = random.choice(actions)
		gammon.apply_action(action, turn)
		moves += 1
		
	if turn == 0:
		zero_actions.append(action)
	else:
		one_actions.append(action)
	turn = (turn + 1) % 2
print "finished!!!"
if gammon.off_pieces[0] == 15:
	print "0 wins"
else:
	print "1 wins"
#print gammon.board
print moves
