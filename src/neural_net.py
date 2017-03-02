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
		self.weights = [np.random.randn(y,x) for x, y in zip(sizes[:-1], sizes[1:])]
		
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

	def do_td(self, inputs, next_prediction, learning_rate):
		# Forward Pass
		
		prediction = self.feedforward(inputs)
		
		# Reverse Pass
		# TD-Gammon weight update
		
		# calculate errors of output neurons
		error_olayer = (next_prediction - prediction) * prediction * (1 - prediction)
		
		# change output layer weights
		for j in range(0,2):
			for i in range(0,40):
				self.weights[1][j][i] = self.weights[1][j][i] + (learning_rate * error_olayer[j] * self.outputs[i])

		# calculate hidden layer errors
		error_hlayer1 = np.zeros((40,))
		for j in range(0,40):
			for i in range(0,2):
				error_hlayer1[j] = error_hlayer1[j] + error_olayer[i] * self.weights[1][i][j]
		error_hlayer = self.outputs * (1 - self.outputs) * error_hlayer1
		
		# change hidden layer weights
		for j in range(0,40):
			for i in range(0,198):
				self.weights[0][j][i] = self.weights[0][j][i] + (3.0 * error_hlayer[j] * inputs[i])
	
	def sigmoid(self, z):
    	# sigmoid activation function
		return 1.0 / (1.0 + np.exp(-z))
	
	def save(self):
		with open('../data/weights_file', 'wb') as wf:
			pickle.dump(self.weights, wf)
		with open('../data/biases_file', 'wb') as bf:
			pickle.dump(self.biases, bf)
		
	def load(self):
		with open('../data/weights_file', 'rb') as wf:
			self.weights = pickle.load(wf)
		with open('../data/biases_file', 'rb') as bf:
			self.biases = pickle.load(bf)
