import itertools
import numpy as np
import random
import pickle
import Image
import time

np.seterr(all='ignore')

class Net(object):

	# sizes = [198, 40, 1] for mnist data
	# 198 inputs for the backgammon representation
	# 40 hidden layer
	# 4 outputs (maybe 1 for now?)
	def __init__(self, sizes):
		self.weights = [np.random.randn(y,x) for x, y in zip(sizes[:-1], sizes[1:])]
		
	def feedforward(self, inputs):
        # calculate input to hidden layer neurons
		in_hlayer = np.dot(self.weights[0], inputs)
		
		# feed inputs of hidden layer neurons through the activation function
		out_hlayer = np.array([self.sigmoid(z) for z in in_hlayer]).reshape(30,)

		# multiply the hidden layer outputs by the corresponding weights to calculate the inputs to the output layer neurons
		in_olayer = np.dot(self.weights[1], out_hlayer.transpose())

		# feed inputs of output layer neurons through the activation function
		out_olayer = np.array([self.sigmoid(z) for z in in_olayer])
		
		# return the vector of outputs from the output layer
		return out_olayer
	
	# TODO: Backpropagate the error according to TD weight update
		
	def sigmoid(self, z):
    	# sigmoid activation function
		return 1.0 / (1.0 + np.exp(-z))
