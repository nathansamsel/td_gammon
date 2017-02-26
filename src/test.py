import game
import neural_net
import time

net = neural_net.Net([198, 40, 1])
gammon = game.Game()
roll = gammon.roll_dice()
print "testing..."
print roll
print gammon.get_actions(roll, 0)

print "Starting game..."

# 2 players roll dice, the largest goes first using the roll
# r1 is white, r2 is black
r1, r2 = (0,0)
turn = 0
# keep rolling if get same
while r1 == r2:
	r1, r2 = gammon.roll_dice()
	if r1 > r2:
		print "White goes first!"
		turn = 1
	elif r2 > r1:
		print "Black goes first!"

start = 1
while not gammon.game_over():
	actions = []
	if start:
		actions = gammon.get_actions((r1, r2), turn)
		start = 0
	else:
		actions = gammon.get_actions(gammon.roll_dice(), turn)
		states = []
		for action in actions:
			states.append(gammon.apply_action(action, turn))
		turn = (turn + 1) % 2
		print len(states)
		time.sleep(1)
