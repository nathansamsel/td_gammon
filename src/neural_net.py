import itertools
import numpy as np
import random
import pickle
import Image
import time

np.seterr(all='ignore')

class Net(object):

	def __init__(self, sizes):
		self.outputs = []
		# sizes should be [198, 40, 1]
		self.weights = [np.random.randn(y,x) for x, y in zip(sizes[:-1], sizes[1:])]
		self.eligibility_trace_o = 0
		
	def feedforward(self, inputs):
        # calculate input to hidden layer neurons
		in_hlayer = np.dot(self.weights[0], inputs)
		
		# feed inputs of hidden layer neurons through the activation function
		out_hlayer = np.array([self.sigmoid(z) for z in in_hlayer]).reshape(40,)
		
		# keep track of outputs for use in reverse pass during the learning process
		self.outputs = out_hlayer

		# multiply the hidden layer outputs by the corresponding weights to calculate the inputs to the output layer neurons
		in_olayer = np.dot(self.weights[1], out_hlayer.transpose())

		# feed inputs of output layer neurons through the activation function
		out_olayer = np.array([self.sigmoid(z) for z in in_olayer])
		
		# return the vector of outputs from the output layer
		return out_olayer

	def do_td(self, state, prediction_t_plus_1, e_trace, learning_rate):
		# Forward Pass
		
		prediction_t = self.feedforward(state)
		
		# Reverse Pass
		# TD-Gammon weight update
		
		# change output layer weights
		for i in range(0,40):
			self.weights[1][0][i] = self.weights[1][0][i] + learning_rate * (prediction_t_plus_1 - prediction_t) * e_trace
		
		# change hidden layer weights
		for j in range(0,40):
			for i in range(0,198):
				self.weights[0][j][i] = self.weights[0][j][i] + learning_rate * (prediction_t_plus_1 - prediction_t) * e_trace
	
	def sigmoid(self, z):
    	# sigmoid activation function
		return 1.0 / (1.0 + np.exp(-z))
	
	def save(self):
		with open('../data/weights_file', 'wb') as wf:
			pickle.dump(self.weights, wf)
		
	def load(self):
		with open('../data/weights_file', 'rb') as wf:
			self.weights = pickle.load(wf)
