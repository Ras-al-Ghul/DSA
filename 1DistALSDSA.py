import collections as CO
import threading as TH
import random as RA
import time as TI
import queue as QU
import sys as SY

screen_lock = TH.Semaphore(value=1)
second_lock = TH.Semaphore(value=1)
global_val = 0
global_calc_list = []
global_queue = QU.Queue()

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
		# voting rights - one for each value in domain
		self.voting_rights = [0 for i in self.domain]
		# columns are indexed by values in domain, rows are indexed by neighbours
		self.without_context_table = []
		# key is which neighbour, value is a 1D array which has preference values for each value in the domain of the neighbour
		self.neighbour_message = {}
		# with_context_weight
		self.with_context_weight = 1.0
		# without_context_weight
		self.without_context_weight = 0.0
		# neighbour voting weights
		self.neighbour_voting_weights = []
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
		# with this we ensure that the context is the same throughout this function
		__old_round_num = self.round_num
		self.round_num += 1

		# set this to minimum value, not just 0
		__util_table_given_context = [0 for i in self.domain]
		for i in self.neighbours:
			# create a temp list which will help in normalizing to 1
			__util_list = [0 for k in self.domain]
			for j in xrange(len(self.domain)):
				__util_list[j] += self.util_table[i][self.context[__old_round_num][i]][j]
			for j in xrange(len(self.domain)):
				__util_table_given_context[j] += (__util_list[j]/float(sum(__util_list)))
		
		# normalize the sums
		__temp_sum = sum(__util_table_given_context)
		for j in xrange(len(self.domain)):
			__util_table_given_context[j] = __util_table_given_context[j]/__temp_sum

		# calculate the without_context scores
		__temp_without_context = [0 for i in self.domain]
		for i in xrange(len(self.neighbours)):
			for j in xrange(len(self.domain)):
				__temp_without_context[j] += (self.without_context_table[i][j] * self.neighbour_voting_weights[i])
		# normalize them
		# __temp_sum = sum(__temp_without_context)
		# for j in xrange(len(self.domain)):
		# 	__temp_without_context[j] = (__temp_without_context[j]/float(__temp_sum))

		# screen_lock.acquire()
		# print self.label, __temp_without_context
		# screen_lock.release()

		# calculate the weighted sum
		__weighted_choices = [0 for i in self.domain]
		for i in xrange(len(self.domain)):
			# (__util_table_given_context[i] * self.with_context_weight) +
			__weighted_choices[i] = (__util_table_given_context[i] * self.with_context_weight) + (__temp_without_context[i] * self.without_context_weight)

		__next_index = __weighted_choices.index(max(__weighted_choices))
		__next_val = self.domain[__next_index]

		# look in __util_table_given_context
		# __next_index = __util_table_given_context.index(max(__util_table_given_context))
		# __next_val = self.domain[__next_index]
		__new_util = 0
		# calculate unnormalized utility
		for i in self.neighbours:
			__new_util += self.util_table[i][self.context[__old_round_num][i]][__next_index]

		__old_util = 0
		for i in self.neighbours:
			__old_util += self.util_table[i][self.context[__old_round_num][i]][self.domain.index(old_val)]

		# delete key
		# del self.context[__old_round_num]
		# increment the round number
		# self.round_num+=1
		# return the best value
		return __next_val, __new_util, __old_util
	def tell_neighbours(self):
		for i in self.neighbours:
			try:
				i.context[i.round_num][self] = self.val
			except Exception as e:
				print "error", e
	def calc_utility(self):
		global global_calc_list
		__util = 0
		for i in xrange(len(global_calc_list)):
			__cur_obj = global_calc_list[i][0]
			__cur_neighbour_list = global_calc_list[i][1]
			for j in __cur_neighbour_list:
				tempval = __cur_obj.util_table[j][j.val][__cur_obj.domain.index(__cur_obj.val)]
				__util += tempval
				# print tempval
		return __util
	def set_voting_rights(self):
		# adjusts the voting rights for the values in my domain
		for i in self.neighbours:
			for j in i.domain:
				for k in xrange(len(self.domain)):
					self.voting_rights[k] += self.util_table[i][j][k]
		__temp_sum = sum(self.voting_rights)
		for k in xrange(len(self.domain)):
			self.voting_rights[k] = self.voting_rights[k]/float(__temp_sum)
	def create_without_context_table(self):
		# this along with the __util_table_given_context will decide next value to choose
		self.without_context_table = [[0 for j in self.domain] for i in self.neighbours]
	def create_neighbour_message(self):
		# creates messages which will fill the neighbour's without_context_table
		for i in self.neighbours:
			# rows are my domain, columns are neighbour's domain
			__temparr = [[0 for k in i.domain] for j in self.domain]
			for j in xrange(len(self.domain)):
				for k in xrange(len(i.domain)):
					__temparr[j][k] = self.util_table[i][i.domain[k]][j]
			# normalize
			for j in xrange(len(self.domain)):
				__temp_sum = sum(__temparr[j])
				for k in xrange(len(i.domain)):
					__temparr[j][k] = __temparr[j][k]/float(__temp_sum)
			# multiply with voting rights					
			for j in xrange(len(self.domain)):
				for k in xrange(len(i.domain)):
					__temparr[j][k] = (__temparr[j][k] * self.voting_rights[j])
			__temp_msg = [0 for k in i.domain]
			# sum over columns
			for j in xrange(len(self.domain)):
				for k in xrange(len(i.domain)):
					__temp_msg[k] += __temparr[j][k]
			# add to dict
			self.neighbour_message[i] = __temp_msg
	def send_neighbour_message(self):
		for key, value in self.neighbour_message.items():
			for j in xrange(len(key.domain)):
				key.without_context_table[key.neighbours.index(self)][j] = value[j]
	def set_neighbour_voting_weights(self):
		self.neighbour_voting_weights = [0 for i in self.neighbours]
		for i in xrange(len(self.neighbours)):
			for j in self.neighbours[i].domain:
				self.neighbour_voting_weights[i] += sum(self.util_table[self.neighbours[i]][j])

		# normalize
		__temp_sum = sum(self.neighbour_voting_weights)
		for i in xrange(len(self.neighbours)):
			self.neighbour_voting_weights[i] = (self.neighbour_voting_weights[i]/float(__temp_sum))
	def DSA(self):
		global screen_lock
		# print self.util_table
		# print self.label, self.val

		# each neighbour has different contribution to util
		self.set_neighbour_voting_weights()
		# set the voting rights
		self.set_voting_rights()
		# create without_context_table
		self.create_without_context_table()
		# create the neighbour_message dict
		self.create_neighbour_message()

		# wait for neighbours to create without_context_table
		TI.sleep(1)

		# add the message to neighbour's without_context_table
		self.send_neighbour_message()

		# for above to happen
		TI.sleep(1)

		screen_lock.acquire()
		print self.label, self.without_context_table
		screen_lock.release()

		# set the start time
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
					
					__old_val = self.val
					self.val = __temp_val
					# screen_lock.acquire()
					global global_queue
					global_queue.put((self.label, __old_val, __temp_val))
					# print self.label, " value changed from ", __old_val, " to ", __temp_val
					# __temp_global = self.calc_utility()
					# global global_val
					# if __temp_global > global_val:
					# 	global_val = __temp_global
					# 	print "global utility changed ", global_val
					# screen_lock.release()
					self.tell_neighbours()

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

	init_val_list = [0,0,0,1]
	for i in xrange(len(init_val_list)):
		nodes_list[i].set_init_val(init_val_list[i])

	# similar to add_neighbours, and for each neighbour,
	# make a list of tuples, where each tuple has an object and a list of lists
	# list of list will be indexed by neighbour's domain values
	# each list in list of list will be indexed by self's domain values
	# chronological order from above declare nodes is followed
	A.set_constraint_table([(B,[[3,4],[2,1]]), (C,[[1,2],[2,1]])])
	B.set_constraint_table([(C,[[2,1],[3,3]]), (D,[[2,4],[1,2]])])

	global global_calc_list
	# same order as above
	global_calc_list = [[A,[B,C]],[B,[C,D]],[C,[]],[D,[]]]

	for i in nodes_list:
		print i.label, i.val,
	
	print ""

	# create processes
	p_list = []
	for i in xrange(len(nodes_list)):
		temp = TH.Thread(target=nodes_list[i].DSA,args=())
		temp.start()
		p_list.append(temp)

	# wait for processes to terminate
	for p in p_list:
		p.join()

	i = 0
	while True:
		count = 0
		for j in nodes_list:
			if i in j.context:
				print j.label, ":",
				for key, value in j.context[i].items():
					print key.label, value,
				print ""
			else:
				count += 1
		if count == len(nodes_list):
			break
		i += 1

	for i in nodes_list:
		print i.label, i.val,

	print "\n"
	global global_queue
	while True:
		if global_queue.empty():
			break
		temp = global_queue.get()
		print temp[0], " changed from ", temp[1], " to ", temp[2]

	print "\nglobal utility ",A.calc_utility()

if __name__ == '__main__':
	main()