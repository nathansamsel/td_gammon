import os
import copy
import time
import random
import numpy as np

class Game:
	def __init__(self):
		self.dice = 6
		self.board = [[0, 0] for _ in range(0, 24)]
		self.bar_pieces = [0, 0]
		self.off_pieces = [0, 0]
		self.bearing_off = [0,0]
		
		# set up board starting position
		
		# set up white
		self.board[23][1] = 2
		self.board[12][1] = 5
		self.board[7][1] = 3
		self.board[5][1] = 5
		
		# set up black
		self.board[0][0] = 2
		self.board[11][0] = 5
		self.board[16][0] = 3
		self.board[18][0] = 5
		#print self.board
		
	def roll_dice(self):
		return (random.randint(1, 6), random.randint(1, 6))
		
	# pass in 1 for white, 0 for black
	def get_actions(self, roll, player):
		actions = []
		r1, r2 = roll
		
		# check for bearing off of black
		for i in range(0, 24):
			if self.board[i][0] != 0 and i < 18:
				break
		else:
			self.bearing_off[0] = 1
			
		# check for bearing off of white
		for i in range(0, 24):
			if self.board[i][1] != 0 and i > 5:
				break
		else:
			self.bearing_off[1] = 1
		
		# check for moves to get off bar if on the bar
		if self.bar_pieces[0] > 0 and player == 0:
			for i in range(0, 5):
				if self.board[i][1] <= 1 and r1 == i:
					actions.append(('bar', r1))
					#print "bar1"
			for i in range(0, 5):
				if self.board[i][1] <= 1 and r2 == i and r1 != r2:
					actions.append(('bar', r2))
					#print "bar2"
					
		elif self.bar_pieces[1] > 0 and player == 1:
			for i in range(17, 23):
				if self.board[i][0] <= 1 and r1 == 23 - i:
					actions.append(('bar', 23 - i))
			for i in range(17, 23):
				if self.board[i][0] <= 1 and r2 == 23 - i and r1 != r2:
					actions.append(('bar', 23 - i))
			
		# check for bearning off moves
		elif self.bearing_off[player] == 1:
			if player == 0:
				removed = -1
				for i in range(17, 24):
					if self.board[i][player] > 0 and 23 - i < r1:
						actions.append((i, 'off'))
						removed = i
				for i in range(17, 24):
					if self.board[i][player] > 0 and 23 - i < r2 and i != removed:
						actions.append((i, 'off'))
			else:
				removed = -1
				for i in range(0, 6):
					if self.board[i][player] > 0 and i < r1:
						actions.append((i, 'off'))
						removed = i
				for i in range(0, 6):
					if self.board[i][player] > 0 and i < r2 and i != removed:
						actions.append((i, 'off'))
						
		# check for regular moves
		else:
			for i in range(0, 24):
				if self.board[i][player] != 0:
					if player == 0:
						# test r1 moves
						if i + r1 <= 23:
							if self.board[i+r1][1] <= 1:
								actions.append((i, i+r1))
						# test r2 moves
						if i + r2 <= 23:
							if self.board[i+r2][1] <= 1:
								actions.append((i, i+r2))
						# test r1 + r2 moves
						# check validity of intermediate move first
						if i + r1 + r2 <= 23:
							if self.board[i+r1+r2][1] <=1 and self.board[i+r1][1] == 0:	
								actions.append((i, i+r1+r2))
					else:
						# test r1 moves
						if i - r1 >= 0:
							if self.board[i-r1][0] <= 1:
								actions.append((i, i-r1))
						# test r2 moves
						if i - r2 >= 0:
							if self.board[i-r2][0] <= 1:
								actions.append((i, i-r2))
						# test r1 + r2 moves
						# check validity of intermediate move first
						if i - r1 - r2 >= 0:
							if self.board[i-r1-r2][0] <= 1 and self.board[i-r1][0] == 0:
								actions.append((i, i-r1-r2))
		return actions
		
	def apply_action(self, action, player):
		start, end = action
		if end == 'off':
			self.board[start][player] -= 1
			self.off_pieces[player] += 1
		elif start == 'bar':
			if self.board[end][(player + 1) % 2] == 1:
				self.board[end][(player + 1) % 2] = 0
				self.bar_pieces[(player + 1) % 2] += 1
			self.bar_pieces[player] -= 1
			self.board[end][player] += 1
		else:
			# attack opponent piece and move to bar
			if self.board[end][(player + 1) % 2] == 1:
				self.board[end][(player + 1) % 2] = 0
				self.bar_pieces[(player + 1) % 2] += 1
			# remove from starting position and move to end position
			self.board[start][player] -= 1
			self.board[end][player] += 1
		return copy.deepcopy(self.board)
	
	def undo_action(self, action, player):
		start, end = action
		if end == 'off':
			self.board[start][player] += 1
			self.off_pieces[player] -= 1
		elif start == 'bar':
			self.bar_pieces[player] += 1
			self.board[end][player] -= 1
		else:
			# remove from starting position and move to end position
			self.board[start][player] += 1
			self.board[end][player] -= 1
	
	
	def get_inputs(self, player):
		inputs = []
		# 192 inputs representing tokens at each point
		for i in range(0, 24):
			if self.board[i][0] >= 1:
				inputs.append(1)
			else:
				inputs.append(0)
			if self.board[i][0] >= 2:
				inputs.append(1)
			else:
				inputs.append(0)
			if self.board[i][0] >= 3:
				inputs.append(1)
			else:
				inputs.append(0) 
			if self.board[i][0] >= 4:
				inputs.append((self.board[i][0] - 3) / 2)
			else:
				inputs.append(0)
			if self.board[i][1] >= 1:
				inputs.append(1)
			else:
				inputs.append(0)
			if self.board[i][1] >= 2:
				inputs.append(1)
			else:
				inputs.append(0)
			if self.board[i][1] >= 3:
				inputs.append(1)
			else:
				inputs.append(0) 
			if self.board[i][1] >= 4:
				inputs.append((self.board[i][1] - 3) / 2)
			else:
				inputs.append(0)
		# 2 inputs for bar pieces
		inputs.append(self.bar_pieces[0])
		inputs.append(self.bar_pieces[1])
		# 2 inputs for removed pieces
		inputs.append(self.off_pieces[0])
		inputs.append(self.off_pieces[1])
		# 2 inputs for turn (binary fashion)
		if player == 0:
			inputs.append(1)
			inputs.append(0)
		else:
			inputs.append(0)
			inputs.append(1)
		return inputs
	
	def game_over(self):
		# if all pieces are off the board for one of the players, then the game is over
		if self.off_pieces[0] == 15 or self.off_pieces[1] == 15:
			return True
		else:
			return False
	
	def winner(self):
		# return the winner or error
		if self.off_pieces[0] == 15:
			return 0
		elif self.off_pieces[1] == 15:
			return 1
		else:
			return -1
