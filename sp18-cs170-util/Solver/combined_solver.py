import os
import pdb
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *
from networkx.algorithms import approximation
import unionfind
import itertools
import networkx.algorithms as algo
from math import exp
import random
"""
======================================================================
  Complete the following function.
======================================================================
"""



class mainb():
	def __init__(self, G, start, list):
		self.G = G
		self.start = start
		self.walk = []
		self.howmanyperms = 1
		self.mst_aprox(G, start)

	def calculateweight(self, path):
		cost = 0
		for i in range(len(path) - 1):
			cost += self.G[path[i]][path[i+1]]['weight']
		return cost

	def dijkreturn(self, fromm):
		pathcost = 0
		path_back = nx.dijkstra_path(self.G, fromm, self.start)
		for i in range(len(path_back) - 1):
			pathcost += self.G[path_back[i]][path_back[i + 1]]['weight']
		return path_back

	def mst_aprox(self, G, start):

		self.dominatingset = list(approximation.min_weighted_dominating_set(G, 'weight'))
		self.bell = dict(algo.shortest_paths.all_pairs_bellman_ford_path(G))
		self.intactset = self.dominatingset[:]
		self.current = self.start
		self.queue={}

		self.copydomi = self.dominatingset[:]
		self.shortest = 4000000000

		cal = 0
		while(len(self.dominatingset) != 0):
			for i in self.dominatingset:
				cal += self.calculateweight(self.bell[self.current][i])
				self.queue[i] = [cal, self.bell[self.current][i]]
			self.goal = min(self.queue, key = self.queue.get)
			self.walk += self.queue[self.goal][1][1:]
			self.queue={}
			self.current = self.goal
			self.dominatingset.remove(self.goal)
		self.walk += self.dijkreturn(self.current)[1:]
		minim = cal
		self.dominatingset= self.copydomi[:]
		self.permus = []

		if self.start in self.dominatingset:
			self.copydomi.remove(self.start)
			try:
				iterate = itertools.permutations(self.copydomi)
				for i in range(self.howmanyperms):
					self.permus += [next(iterate)]
			except:
				iterate = itertools.permutations(self.copydomi)
				self.permus = list(iterate)

		else:
			try:
				iterate = itertools.permutations(self.copydomi)
				for i in range(self.howmanyperms):
					self.permus += [next(iterate)]
			except:
				iterate = itertools.permutations(self.copydomi)
				self.permus = list(iterate)

		for i in self.permus:
			self.current = self.start
			cal = 0
			tempwalk =[]
			for k in i:
				cal += self.calculateweight(self.bell[self.current][k])
				tempwalk += self.bell[self.current][k][1:]
				self.current = k
			cal += self.calculateweight(self.bell[self.current][self.start])
			tempwalk += self.bell[self.current][self.start][1:]
			if minim > cal:
				self.walk = tempwalk[:]
				minim = cal

bell = 0
greedy = 0
count = 0
localcount = 0
def solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=[]):
	"""
	Write your algorithm here.
	Input:
		list_of_kingdom_names: An list of kingdom names such that node i of the graph corresponds to name index i in the list
		starting_kingdom: The name of the starting kingdom for the walk
		adjacency_matrix: The adjacency matrix from the input file

	Output:
		Return 2 things. The first is a list of kingdoms representing the walk, and the second is the set of kingdoms that are conquered
	"""
	G = adjacency_matrix_to_graph(adjacency_matrix)
	starting_kingdom_i = list_of_kingdom_names.index(starting_kingdom)
	closed_walk = [starting_kingdom]
	conquered_kingdoms = []
	gclosed_walk = []
	gconquered_kingdoms = []
	mai=main(list_of_kingdom_names, starting_kingdom, adjacency_matrix, 1, G, params)
	maii = mainb(G, starting_kingdom_i, list_of_kingdom_names)

	for k in maii.walk:
		closed_walk.append(list_of_kingdom_names[k])
	for l in maii.intactset:
		conquered_kingdoms.append(list_of_kingdom_names[l])


	for k in mai.finalclosed_walk:
		gclosed_walk += [list_of_kingdom_names.index(k)]
	for l in mai.finalconquered_kingdoms:
		gconquered_kingdoms += [list_of_kingdom_names.index(l)]

	global bell
	global greedy
	global count
	costb, solution_message1 = cost_of_solution(G, [list_of_kingdom_names.index(starting_kingdom)] + maii.walk, maii.intactset)
	costg, solution_message2 = cost_of_solution(G, gclosed_walk, gconquered_kingdoms)
	if costg == 'infinite':
		count += 1
		mai=main(list_of_kingdom_names, starting_kingdom, adjacency_matrix, 0, G, params)
		gclosed_walk=[]
		gconquered_kingdoms=[]
		for k in mai.finalclosed_walk:
			gclosed_walk += [list_of_kingdom_names.index(k)]
		for l in mai.finalconquered_kingdoms:
			gconquered_kingdoms += [list_of_kingdom_names.index(l)]
		costg, solution_message2 = cost_of_solution(G, gclosed_walk, gconquered_kingdoms)

	if costb < costg:
		bell+=1
		return closed_walk, conquered_kingdoms
	else:
		pass
		greedy += 1
		return mai.finalclosed_walk, mai.finalconquered_kingdoms

class main():

	def __init__(self, list_of_kingdom_names, starting_kingdom, adjacency_matrix, local, G, params=[]):
		# key : index, value : length of walk at that time(after walk is updated)
		self.conquered_at = {}
		self.counter = 0
		self.totalcost = 0
		self.M = adjacency_matrix
		self.G = G

		self.goal = len(list_of_kingdom_names)
		self.starting_kingdom = starting_kingdom
		self.num_king = len(list_of_kingdom_names)

		# somewhere that has surrendered and doesn't have not-yet surrendered neigbor => don't need to go
		self.donelist = []

		self.list_of_kingdom_names = list_of_kingdom_names

		self.starting_index = list_of_kingdom_names.index(starting_kingdom)

		self.h = {}
		#  0 means unconquered and 1 means conquered(second element of dict). Third one means whether it is surrendered or not
		self.h[self.starting_index] = [0 + self.M[self.starting_index][self.starting_index],0, 0]
		# hq.heappush(h, (0 + M[starting_index][starting_index],starting_index))
		for i in self.getn(self.starting_index):
			self.h[i[0]] = [(i[1]+i[2]),0, 0]

		self.conquered_kingdoms=[]
		self.surrendered=[]
		# surrendered kingdom
		self.csize = 0
		self.ssize = 0


		self.closed_walk=[self.starting_index]


	# do it for only start point
		self.current_conquer = min(self.h, key = self.h.get)
		if self.current_conquer != self.starting_index:
			# think about it later
		#     if len(getn(M, current_conquer)) == 1:
		#         sum = 0
		#         for i in getn(M, starting_index):
		#             sum += i[1]+i[2]
		#         if h[current_conquer] + M[starting_index][current_conquer] >
			self.closed_walk += [self.current_conquer]
			self.h[self.current_conquer][1] = 1
			# self.h[self.current_conquer][2] = 1
			self.conquered_kingdoms += [self.current_conquer]
			# self.update_dict(self.current_conquer)

		else:
			self.conquered_kingdoms += [self.current_conquer]
		self.h[self.current_conquer][1] = 1

		# for simulated annealing
		self.conquered_at[self.current_conquer] = len(self.closed_walk)

		if self.current_conquer not in self.surrendered:
				self.ssize+=1
				self.surrendered += [self.current_conquer]
				self.h[self.current_conquer][2] = 1

		self.csize += 1
		self.update_dict(self.current_conquer)
		# self.ssize += 1
#  we increase surrender size in surrender function. But we increase by one(right above) manually to consider the conquered city itself(city just conquered).
#  We can just remove above part(adding the city in surrender list), since it will be done in surrender function.

		# self.surrender(self.current_conquer)

	# while loop
		while (self.ssize != self.goal):
			self.current_conquer = min(self.h, key = self.h.get)
			# while(self.current_conquer in self.conquered_kingdoms):
			#     self.h.pop(self.current_conquer)
			#     self.current_conquer = min(self.h, key = self.h.get)
			while(self.h[self.current_conquer][2] == 1 and len(self.getns(self.current_conquer))==0):
				self.donelist += [self.current_conquer]
				self.h.pop(self.current_conquer)
				self.current_conquer = min(self.h, key = self.h.get)

			self.conquered_kingdoms += [self.current_conquer]
			self.update_walk(self.current_conquer)

			# for annealing
			self.conquered_at[self.current_conquer] = len(self.closed_walk)

			self.h[self.current_conquer][1] = 1
			if self.current_conquer not in self.surrendered:
				self.ssize+=1
				self.surrendered += [self.current_conquer]
				self.h[self.current_conquer][2] = 1

			self.csize+=1
			# self.ssize+=1
			# print('goal',self.goal)
			# print('csize',self.csize)
			# if self.ssize==3:
			# print('conking',self.conquered_kingdoms)
			# print('surking',self.surrendered)

			# self.surrender(self.current_conquer)

			self.update_dict(self.current_conquer)


		# let's go back to home Now, self.current_conquer is my location and we want shortest path back to starting point. Dijkstra will be good.
		self.originalbackcost = self.dijk(self.current_conquer)
		if local:
			self.localsearch()

		self.finalclosed_walk = []
		self.finalconquered_kingdoms = []

		for j in self.conquered_kingdoms:
			self.finalconquered_kingdoms += [self.list_of_kingdom_names[j]]
		for i in self.closed_walk:
			self.finalclosed_walk += [self.list_of_kingdom_names[i]]

		self.totalcost = cost_of_solution(self.G, self.finalclosed_walk, self.finalconquered_kingdoms)

# pop out conquered one and add new neighbors of currently conquered city
	def update_dict(self, index):
		topoplist = []
		topoppath = []
		for i in self.h:
			if self.h[i][1] == 1:
				topoplist += [i]

		for q in topoplist:
			self.h.pop(q)

		for j in self.h:
			# make sure that you can just pass some kingdom if you want to. Then you need to change the below
			if len(self.conquered_kingdoms) == 1 and self.current_conquer != self.starting_index:
				ind = [self.starting_index]
				cost = self.M[self.starting_index][ind[0]]
				self.h[j] += [str(self.starting_index) + 'a']
			elif len(self.conquered_kingdoms) == 1:
				break;
			else:
				ind = self.closed_walk[-self.increment_closed_walk - 1:]
				cost = 0
				for i in range(len(ind) - 1):
					if str(ind[i]) + 'a' in self.h[j]:
						inde = self.h[j].index(str(ind[i]) + 'a')
						self.h[j] = self.h[j][:inde + 1]
						cost = 0
					else:
						self.h[j] += [str(ind[i]) + 'a']
					cost += self.M[ind[i]][ind[i + 1]]

			# toprocess = []
			# for i in ind[:-1]:
			# 	toprocess += [str(i) + 'a']
			self.h[j][0] += cost
			# self.h[j] += toprocess

		for k in self.getn(index):
			if self.h.get(k[0]):
				if self.h[k[0]][0] >= k[1] + k[2]:
					self.h[k[0]][0] =  k[1] + k[2]
					topoppath += [k[0]]
				else:
					pass
			else:
				try:
					if self.conquered_kingdoms.index(k[0]):
						pass
				except:
					# we know that k[0] is not surrendered because if it is, then it must be in h already
					if k[0] not in self.conquered_kingdoms and k[0] not in self.donelist:
						if k[0] in self.surrendered :
							self.h[k[0]] = [k[1] + k[2], 0, 1]
						else :
							self.h[k[0]] = [k[1] + k[2],0,0]

		self.surrender(index)

		for p in topoppath:
			self.h[p] = self.h[p][:3]

	def surrender(self, current_index):

		toprocess = self.getns(current_index)
		for i in toprocess:
			if i not in self.surrendered:
				self.h[i][2] = 1
				self.surrendered += [i]
				self.ssize += 1

		# nindex = 0
		# realindex = current_index * len(self.M[0]) + nindex
		# for i in self.M[current_index]:
		# 	pdb.set_trace()
		# 	if i == 'x' or realindex in self.surrendered:
		# 		realindex += 1
		# 	elif self.h[realindex][2] == 0:
		# 		self.h[realindex][2] = 1
		# 		self.surrendered += [realindex]
		# 		realindex += 1
		# 		self.ssize += 1
		# 	else :
		# 		realindex += 1

	def update_walk(self,index):

		inilen = len(self.closed_walk)
		if len(self.h[self.current_conquer]) >= 4:
			self.closed_walk += self.parse_path(self.h[self.current_conquer][3:])
			self.h[self.current_conquer]=self.h[self.current_conquer][:3]
		self.closed_walk += [self.current_conquer]
		self.increment_closed_walk = len(self.closed_walk) - inilen
		# think about it.
		# self.conquered_at(len(len))

# make sure you reverse the order of returning list
	def parse_path(self, path):
		newpath=''
		for j in path:
			newpath += j
		toreturn=[]
		sum = ''
		for i in newpath:
			if i == 'a':
				toreturn += [eval(sum)]
				sum=''
			else:
				sum += i
		toreturn.reverse()
		return toreturn

	# get neighbor
	# return (nindex, edgeweight, conquer cost)
	def getn(self, index):
		# neighbor=[]
		# for i in self.G.neighbors(index):
		# 	if i == 'x':
		# 		nindex += 1
		# 	elif nindex == index:
		# 		nindex += 1
		# 	else :
		# 		neighbor+=[(nindex,i,self.M[nindex][nindex])]
		# 		nindex += 1
		neighbor=[]
		for i in self.G.neighbors(index):
			neighbor += [(i, self.M[index][i],  self.M[i][i])]
		return neighbor

# return non-surrendered
	def getns(self, index):
		# neighbor=[]
		# nindex = 0
		# for i in self.M[index]:
		# 	if i == 'x':
		# 		nindex += 1
		# 	elif self.h.get(nindex):
		# 		if self.h[nindex][2] == 1:
		# 			nindex += 1
		# 		else:
		# 			neighbor += [nindex]
		# 			nindex +=1
		# 	else :
		# 		neighbor += [nindex]
		# 		nindex += 1

		neighbor=[]
		for i in self.G.neighbors(index):
			if i not in self.surrendered:
				neighbor += [i]
		return neighbor

	def dijk(self,start):
		pathcost = 0
		# closed_walk.append('back')
		self.path_back = nx.dijkstra_path(self.G, start,  self.list_of_kingdom_names.index(self.starting_kingdom))
		for i in range(1, len(self.path_back)):
			self.closed_walk.append(self.path_back[i])
		for i in range(len(self.path_back) - 1):
			pathcost += self.M[self.path_back[i]][self.path_back[i + 1]]
		return pathcost

	def dijkreturn(self,start):
		pathcost = 0
		# closed_walk.append('back')
		path_back = nx.dijkstra_path(self.G, start,  self.list_of_kingdom_names.index(self.starting_kingdom))
		for i in range(len(path_back) - 1):
			pathcost += self.M[self.path_back[i]][self.path_back[i + 1]]
		return pathcost, path_back

	def localsearch(self):
		self.candidates= {}
		global localcount
		self.neis=self.conquered_kingdoms[:]
		for i in self.neis:
			self.T = 2000000000
			self.p = exp(-1/self.T)
			self.copykingdoms = self.conquered_kingdoms[:]
			self.copywalks = self.closed_walk[:]
			passs = False
			# it means that the node we are changing is at the last part
			fullcopywalk = False

			potential = -self.M[i][i]
			checker = True
			index = i
			NTR = {}
			size = 0
	# check whether below really removes or not
			self.copykingdoms.remove(i)
			dontconquer = index
			for j in self.getn(index):
				jindex = j[0]
				if jindex not in self.conquered_kingdoms:
					for k in self.getn(jindex):
						kindex = k[0]
						if kindex in self.copykingdoms:
							checker = False
					if checker:
						size += 1
						NTR[jindex] = [self.M[i][jindex] + self.M[jindex][jindex],0,0]
			first={}
			uniongroup={}
			unioned=[]
			uf = unionfind.UnionFind(len(NTR.keys()))
			if len(NTR.keys()) == 0:
				passs = True
			else:
				for p in NTR:
					root = None
					# dont know whether use below
					addiunion = False
					neigh = self.getns(p)
					if p not in unioned:
						if len(neigh) > 0:
							uniongroup[p] = [p]
							unioned += [p]
							root = p
						else:
							first[p] = [self.M[p][dontconquer] + self.M[p][p],0,0]
					else:
						root = uf._root(p)
					for j in neigh:
						if j in NTR.keys():
							uf.union(p,j)
						if j not in unioned:
							uniongroup[root] += [j]
							unioned+=[j]

			self.newclosedwalk=[]

			for q in first:
				back = self.closed_walk[self.conquered_at[i] - 2]
				try :
					front = self.closed_walk[self.conquered_at[i]]
				except:
					front = None
				if q == back:
					self.copykingdoms +=[q]
					size -= 1
					if size != 0:
						potential += self.M[q][q]
					else :
						newbackcost, newpath = self.dijkreturn(back)
						self.copywalks = self.closed_walk[:back] + newpath
						potential += newbackcost - self.originalbackcost + self.M[q][q] - self.M[i][q]
						fullcopywalk = True
					# 	think about it

				# check if front has str type
				elif q == front:
					self.copykingdoms += [q]
					potential += self.M[q][q]
					size -= 1
				# ----------------------------------------maybe I don't need below
				else:
					potential += first[q][0]
					self.copykingdoms+=[q]
					self.newclosedwalk += [q, dontconquer]
			# ----------------------------------------------

			usedroot=[]
			submains=[]
			for q in unioned:
				tosubgraph=[]
				root = uf._root(q)
				if root not in usedroot:
					usedroot += [root]
					for j in uniongroup[root]:
						tosubgraph += [j]
				self.subG = self.G.subgraph(tosubgraph)

				# !!!!!!!self.subG    -- adjacency matrix. check!
				self.subG[dontconquer][dontconquer] = 4000000001
				submains += [submain(self.list_of_kingdom_names, dontconquer, self.subG, self.subG, 0, params=[])]

			for q in submains:
				self.newclosedwalk += q.closed_walk
				self.copykingdoms += q.conquered_kingdoms
				potential += q.totalcost
			dontconquerindex = self.conquered_at[dontconquer] - 1
			if not fullcopywalk:
				self.copywalks = self.closed_walk[:dontconquerindex + 1] + self.newclosedwalk + self.closed_walk[dontconquerindex + 1:]
			if not passs:
				self.candidates[potential] = [self.copykingdoms, self.copywalks]
		if self.candidates:
			finalpotential = min(self.candidates)
			if finalpotential < 0:
				localcount += 1
				self.closed_walk = self.candidates[finalpotential][1]
				self.conquered_kingdoms = self.candidates[finalpotential][0]
				self.totalcost += finalpotential
				self.T -= 1
				if self.T < 0:
					T=0.00001
			elif self.p > random.random():
				self.T -= 1
				if self.T < 0:
					T=0.00001
				coun = 0
				for l in NTR:
					if coun ==0:
						self.neis +=[l]
						coun +=1
						print('ha')
# nwalkinfo = [walks to update, index to plugin, new conquered kingdom, potential, last conquered kingdom]
# nwalkinfo = self.localsearch()
#
# path_back2 = nx.dijkstra_path(G, nwalkinfo[4], list_of_kingdom_names.index(starting_kingdom))
# backcost2 = 0
# for i in range(1, len(path_back)):
# 	closed_walk.append(list_of_kingdom_names[path_back[i]])
# for i in range(1, len(path_back) - 1):
# 	backcost += adjacency_matrix[i][i + 1]
#
# conquered_kingdoms = nwalkinfo[3]
# closed_walk = closed_walk[:nwalkinfo[1]] + nwalkinfo[0] + closed_walk[nwalkinfo[1]:]


class submain(main):
	def __init__(self,list_of_kingdom_names, starting_kingdom, adjacency_matrix, local ,G, params=[]):
		super().__init__(list_of_kingdom_names, starting_kingdom, adjacency_matrix, local, G, params=[])



"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def solve_from_file(input_file, output_directory, params=[]):
	print('Processing', input_file)

	input_data = utils.read_file(input_file)
	number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
	closed_walk, conquered_kingdoms = solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=params)

	basename, filename = os.path.split(input_file)
	output_filename = utils.input_to_output(filename)
	output_file = f'{output_directory}/{output_filename}'
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	utils.write_data_to_file(output_file, closed_walk, ' ')
	utils.write_to_file(output_file, '\n', append=True)
	utils.write_data_to_file(output_file, conquered_kingdoms, ' ', append=True)


def solve_all(input_directory, output_directory, params=[]):
	input_files = utils.get_files_with_extension(input_directory, 'in')

	for input_file in input_files:
		solve_from_file(input_file, output_directory, params=params)
	# global count
	# global localcount
	# print("count : ", count)
	# print("localcount : ", localcount)

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Parsing arguments')
	parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
	parser.add_argument('input', type=str, help='The path to the input file or directory')
	parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
	parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
	args = parser.parse_args()
	output_directory = args.output_directory
	if args.all:
		input_directory = args.input
		solve_all(input_directory, output_directory, params=args.params)
	else:
		input_file = args.input
		solve_from_file(input_file, output_directory, params=args.params)
