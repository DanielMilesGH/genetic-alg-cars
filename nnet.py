import numpy as np
import math
import random 

MUTATION_WEIGHT_MODIFY_CHANCE = 0.35
MUTATION_ARRAY_MIX_PERC = 0.5

class Nnet:
	def __init__(self, num_input, num_hidden, num_output):
		self.num_input = num_input
		self.num_hidden = num_hidden
		self.num_output = num_output

		# for printing
		self.hidden_inputs=None
		self.hidden_outputs=None
		self.final_inputs=None
		self.final_outputs=None
		# randomly selecting input -> hidden weights 
		# the size is num_hidden, num_input, meaning that it will output a matrix
		# of num_hidden lists inside, and num_input numbers within each list 
		self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))		

		# randomly selecting hidden -> output weights
		# same as input, although this time it has num_output lists inside, with num_hidden values
		# in each list
		self.weight_hidden_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))

		# choosing activation function (to limit output to 0.00 to 1)
		# self.activation_function = lambda x: scipy.special.expit(x) # sigmoid 
		# manually written sigmoid, to avoid scipy import
		self.activation_function = lambda x: 1/(1+np.exp(-x))

	def get_outputs(self, inputs_list):
		# getting list of inputs, and converting it into a 2 dimensional numpy array, [[i1],[i2],[i3]].
		# we then transpose it to turn it into a column vector
		inputs = np.array(inputs_list, ndmin=2).T
		
		# getting hidden values by mutliplying the weights matrix and the inputs together
		# in the first cycle, the weights are given my np.random.normal()
		# 
		# because it is a NxM matrix multiplied by a 1xM column vector,
		# hidden_inputs is itself a column vector, [[x1],[x2],[x3]].T 
		hidden_inputs = np.dot(self.weight_input_hidden, inputs)
		self.hidden_inputs = hidden_inputs
		# activation function just applies the sigmoid function to each value in the
		# column vector, meaning that hidden_outputs is still a column vector,
		# but now each value is between 0 and 1
		hidden_outputs = self.activation_function(hidden_inputs)
		self.hidden_outputs = hidden_outputs
		# final_inputs is again a column vector, because weight_hidden_output
		# is a (num_output, num_hidden) matrix, being multiplied by hidden_outputs,
		# which we said earlier is a column vector
		final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
		self.final_inputs = final_inputs
		# final_outputs is then finally a column vector, representing 
		# each output neurons activation
		final_outputs = self.activation_function(final_inputs)
		self.final_outputs = final_outputs

		# print('final outputs',final_outputs)

		return final_outputs

	def get_max_value(self, inputs_list):
		# gives a list, then outputs a list (in the form of a column vector)
		outputs=self.get_outputs(inputs_list)
		return outputs

	def modify_weights(self):
		Nnet.modify_array(self.weight_input_hidden)
		Nnet.modify_array(self.weight_hidden_output)	
		
	def create_mixed_weights(self, net1, net2): # this function actually "breeds" the arrays
		self.weight_input_hidden = Nnet.get_mix_from_arrays(net1.weight_input_hidden, net2.weight_input_hidden)
		self.weight_hidden_output = Nnet.get_mix_from_arrays(net1.weight_hidden_output, net2.weight_hidden_output)

	def modify_array(a): # this function mutates our array
		# np.nditer is a special multi-dimensional efficient indexer
		# basically just indexing through a list
		#
		# so for each value in the array passed to it, 
		# it will call a random number between 0 and 1, and if it is less
		# than the mutation weight chance, change the current index's value (i[...]) into
		# a random number between 0 and 1,
		# minus 0.5 as we want our weights to be between -0.5 and 0.5
		for i in np.nditer(a, op_flags=['readwrite']):
			if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
				i[...] = np.random.random_sample() - 0.5

	def get_mix_from_arrays(ar1, ar2): # this function creates the breeding framework
		# ar1 and ar2 are two neural networks' weight_input_hidden values
		# or weight_hidden_output values
		# these are both matrices

		# array.size gives number of values in the array
		total_entries = ar1.size
		# .shape outputs (cols, rows), so indexing 0 and 1 gets us those
		num_rows = ar1.shape[0]
		num_cols = ar1.shape[1]

		# if total entries are 100, we then do 100 - (100*mix percent), so that
		# if mix percent is only 0.05, only 5 of the total entires will be mixed
		num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERC)
		
		# idx represents index
		# np.arrange(num) is the same as range(num), but outputs an array
		# [0,1,2,...,num]
		#
		# np.random.choice() then takes that range array, and randomly selects 
		# num_to_take numbers from the range
		# those selected random numbers will now be the index values in the next step
		idx = np.random.choice(np.arange(total_entries), num_to_take, replace=False)

		# res is a (num_rows,num_cols) matrix filled with random values between 0 and 1
		# this will act as the mixed array of ar1 and ar2
		res = np.random.rand(num_rows, num_cols)

		# for row: for col: is a common way of indexing through every value in a multi-dimensional array
		# (row * num_cols) + col is a formula for getting which number you are on in the 
		# matrix, so printing all of them would look like [1,2,3,4,5...matrix.size]
		for row in range(0, num_rows):
			for col in range(0, num_cols):
				index= (row * num_cols) + col
				# if the current index is in idx, the randomly selected index's,
				# make res's index equal to ar1's index
				# otherwise, make it equal to ar2's index
				if index in idx:
					res[row][col] = ar1[row][col]
				else:
					res[row][col] = ar2[row][col]

		# res is now a matrix that represents a mixture of ar1 and ar2
		# 
		# mutation_array_mix_perc represents how much of a mix it actually is,
		# it represents what percent of res is made up of ar1
		# and 1-mutation_array_mix_perc represents the percent of res that is
		# made up of ar2
		return res

	def printStuff(self):
		print('These are the weight values from input to hidden:', self.weight_input_hidden)
		print('\n')
		print('\n')
		print('These are the weight values from hidden to output:', self.weight_hidden_output)
		print('\n')
		print('\n')


#various tests
if __name__=='__main__':
	def test():
		nnet = Nnet(4, 5, 4)
		inputs = [0.1, 0.3, 0.2, 0.3]
		output = nnet.get_max_value(inputs)
		print(output)


	# def tests():
	# 	ar1 = np.random.uniform(-0.5, 0.5, size=(3, 4))
	# 	ar2 = np.random.uniform(-0.5, 0.5, size=(3, 4))
	# 	# print('ar1.size', ar1.size, sep='\n')
	# 	# print('ar1', ar1, sep='\n')

	# 	# print('ar1', ar1, sep='\n')

	# 	print('')

	# 	# print('ar1', ar1, sep='\n')
	# 	# print('ar2', ar2, sep='\n')
	# 	print(ar1)
	# 	Nnet.get_outputs()
	# 	mixed = Nnet.get_mix_from_arrays(ar1, ar2)
	# 	# print('mixed', mixed, sep='\n')

	# tests() 
