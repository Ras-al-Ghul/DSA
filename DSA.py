import collections as CO
import threading as TH
import random as RA
import time as TI
import queue as QU
import sys as SY

class Node:
	def __init__(self, label, domain, probability):
		# your label
		self.label = label
		# your domain
		self.domain = domain
		# list of neighbour objects
		self.neighbours = []
		# current value
		self.val = self.domain[RA.randint(0,len(self.domain)-1)]
		# dict with keys being neighbour objects and values being dicts
		# values are dicts with keys being neighbour's domain and value being list of util values
		self.util_table = {}
		# holds round number
		self.round_num = 0
		# holds context
		self.context = CO.defaultdict(dict)
		# changing probability
		self.probability = probability
	def add_neighbours(self, neighbours):
		for i in neighbours:
			# add neighbour to your list
			self.neighbours.append(i)
			# add yourself to neighbour's list
			i.neighbours.append(self)
	def set_init_val(self, val):
		# can be used to start DSA at certain value
		self.val = val
	def set_constraint_table(self,constraints):
		for i in xrange(len(constraints)):
			# current object
			__temp_obj = constraints[i][0]
			# current list under consideration
			__temp_list_of_lists = constraints[i][1]
			__temp_dict = {}
			# for adding into neighbour's dict
			__my_vals = [[] for z in self.domain]
			for j in xrange(len(__temp_list_of_lists)):
				# get the value from it's domain
				__cur_val = __temp_obj.domain[j]
				# create key, value pair
				__temp_dict[__cur_val] = __temp_list_of_lists[j][:]
				# set __my_vals
				for k in xrange(len(self.domain)):
					__my_vals[k].append(__temp_list_of_lists[j][k])
			
			# set the util_table dict to the current object's dict
			self.util_table[__temp_obj] = __temp_dict

			# create dict for neighbour
			__temp_dict = {}
			for j in xrange(len(self.domain)):
				__temp_dict[self.domain[j]] = __my_vals[j]
			# set neighbour's dict
			__temp_obj.util_table[self] = __temp_dict
	def select_new_val(self, old_val):
		# set this to minimum value, not just 0
		__util_list = [0 for i in self.domain]
		for i in self.neighbours:
			# it is a tuple
			for j in xrange(len(self.domain)):
				__util_list[j] += self.util_table[i][self.context[self.round_num][i]][j]
		
		__next_val = self.domain[__util_list.index(max(__util_list))]
		__new_util = max(__util_list)

		__old_util = 0
		for i in self.neighbours:
			__old_util += self.util_table[i][self.context[self.round_num][i]][self.domain.index(old_val)]

		# delete key
		# del self.context[self.round_num]
		# increment the round number
		self.round_num+=1
		# return the best value
		return __next_val, __new_util, __old_util
	def tell_neighbours(self):
		for i in self.neighbours:
			try:
				i.context[i.round_num][self] = self.val
			except Exception as e:
				print "error", e
	def DSA(self):
		# print self.util_table
		# print self.label, self.val
		__start_time = TI.time()
		# send initial value to neighbours
		self.tell_neighbours()

		# execute for 10 seconds
		while TI.time() - __start_time < 2:
			__inner_start = TI.time()
			__inner_flag = False
			while len(self.context[self.round_num]) < len(self.neighbours):
				if TI.time() - __inner_start > 0.1:
					if len(self.context[self.round_num]) >= 0:
						for i in self.neighbours:
							if i not in self.context[self.round_num]:
								self.context[self.round_num][i] = i.val
					else:
						__inner_flag = True
						break
				else:
					continue
			if __inner_flag:
				break
			__temp_val, __new_util, __old_util = self.select_new_val(self.val)
			if __new_util > __old_util:
				if RA.random() < self.probability:
					self.val = __temp_val
					self.tell_neighbours()
					# print "changed"

def main():
	# declare nodes with labels and domains
	A = Node('A', [0,1], 0.8)
	B = Node('B', [0,1], 0.8)
	C = Node('C', [0,1], 0.8)
	D = Node('D', [0,1], 0.8)

	# there should be 'sum(number of edges in the graph)' items in the square braces
	A.add_neighbours([B,C])
	B.add_neighbours([C,D])

	# list of nodes
	nodes_list = [A,B,C,D]

	# init_val_list = [0,0,0,0]
	# for i in xrange(len(init_val_list)):
	# 	nodes_list[i].set_init_val(init_val_list[i])

	# similar to add_neighbours, and for each neighbour,
	# make a list of tuples, where each tuple has an object and a list of lists
	# list of list will be indexed by neighbour's domain values
	# each list in list of list will be indexed by self's domain values
	# chronological order from above declare nodes is followed
	A.set_constraint_table([(B,[[3,4],[2,1]]), (C,[[1,2],[2,1]])])
	B.set_constraint_table([(C,[[2,1],[3,3]]), (D,[[2,4],[1,2]])])

	for i in nodes_list:
		print i.label, i.val
	
	# create processes
	p_list = []
	for i in nodes_list:
		temp = TH.Thread(target=i.DSA,args=())
		temp.start()
		p_list.append(temp)

	# wait for processes to terminate
	for p in p_list:
		p.join()

	for i in nodes_list:
		print i.label, i.val

if __name__ == '__main__':
	main()