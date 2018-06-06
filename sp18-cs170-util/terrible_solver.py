import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *
import heapq as hq
import pdb


from networkx.drawing.nx_agraph import to_agraph



from collections import defaultdict
from heapq import *

"""
======================================================================
  Complete the following function.
======================================================================
"""


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

    mai=main(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params)
# heap format = (edgeweight + conquer, index)
    #print(adjacency_matrix)
    G = adjacency_matrix_to_graph(adjacency_matrix)
    print("G edges:" + str(G.edges()))


    closed_walk =[]
    conquered_kingdoms=[]
    for i in mai.closed_walk:
        closed_walk +=[list_of_kingdom_names[i]]
    for j in mai.conquered_kingdoms:
        conquered_kingdoms += [list_of_kingdom_names[j]]
    #print(closed_walk, conquered_kingdoms, len(set(conquered_kingdoms)),len(set(mai.surrendered)), len(conquered_kingdoms),len(mai.surrendered))
    #print(G.nodes())
    #print(mai.current_conquer)
    # Drawing code
    #A = to_agraph(G)
    #A.layout('dot')
    #nx.draw(G,with_labels = True,)

    #plt.show()

    path_back = nx.dijkstra_path(G, mai.current_conquer, int(starting_kingdom[-1]))
    adjacency_matrix_to_graph(adjacency_matrix)
    print(path_back)
    for i in range(1, len(path_back)):
        closed_walk.append(list_of_kingdom_names[path_back[i]])
    print(closed_walk)
    return closed_walk, conquered_kingdoms

#  we need to figure out
# jhoto - hoel - jhoto case.
class main():

    def __init__(self, list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=[]):
        self.M = adjacency_matrix


        self.goal = len(list_of_kingdom_names)
        self.starting_kingdom = starting_kingdom
        self.num_king = len(list_of_kingdom_names)

        self.list_of_kingdom_names = list_of_kingdom_names

        self.starting_index = list_of_kingdom_names.index(starting_kingdom)


        a=adjacency_matrix
        b=adjacency_matrix_to_edge_list
        # pdb.set_trace()

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
            pass
            self.conquered_kingdoms += [self.current_conquer]
        self.h[self.current_conquer][1] = 1
        # self.h[self.current_conquer][2] = 1
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
            if self.h[self.current_conquer][2] == 1 and len(self.getns(self.current_conquer))==0:
                self.h.pop(self.current_conquer)
                self.current_conquer = min(self.h, key = self.h.get)

            self.conquered_kingdoms += [self.current_conquer]
            self.update_walk(self.current_conquer)
            self.h[self.current_conquer][1] = 1
            # self.h[self.current_conquer][2] = 1
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

# pop out conquered one and add new neighbors of currently conquered city
    def update_dict(self, index):
        topoplist = []
        topoppath = []
        for i in self.h:
            if self.h[i][1] == 1:
                topoplist += [i]
        for j in self.h:
            # make sure that you can just pass some kingdom if you want to. Then you need to change the below
            ind = self.conquered_kingdoms[-1]
            self.h[j][0] += self.M[index][ind]
            self.h[j] += [str(ind) + 'a']
        for k in self.getn(index):
            if self.h.get(k[0]):
                if self.h[k[0]][0] >= k[1]+k[2]:
                    self.h[k[0]][0] =  k[1] + k[2]
                    topoppath += [k[0]]
                else:
                    pass
            else:
                try:
                    if self.conquered.index(k[0]):
                        pass
                except:
                    # we know that k[0] is not surrendered because if it is, then it must be in h already
                    if k[0] not in self.conquered_kingdoms:
                        self.h[k[0]] = [k[1] + k[2],0,0]

        self.surrender(index)
        for q in topoplist:
            self.h.pop(q)
        for p in topoppath:
            self.h[p].pop()
    def surrender(self, current_index):
        nindex = 0
        for i in self.M[current_index]:
            if i == 'x' or nindex in self.surrendered:
                nindex += 1
                pass
            elif self.h[nindex][2] == 0:
                self.h[nindex][2] = 1
                self.surrendered += [nindex]
                nindex += 1
                self.ssize += 1
            else :
                nindex += 1

    def update_walk(self,index):
        if len(self.h[self.current_conquer]) == 4:
            self.closed_walk += self.parse_path(self.h[self.current_conquer][3])
        self.closed_walk += [self.current_conquer]


# make sure you reverse the order of returning list
    def parse_path(self, path):
        toreturn=[]
        sum = ''
        for i in path:
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
        neighbor=[]
        nindex = 0
        for i in self.M[index]:
            if i == 'x':
                nindex += 1
            elif nindex == index:
                nindex += 1
            else :
                neighbor+=[(nindex,i,self.M[nindex][nindex])]
                nindex += 1
        return neighbor

# return non-surrendered
    def getns(self, index):
        neighbor=[]
        nindex = 0
        for i in self.M[index]:
            if i == 'x':
                nindex += 1
            elif self.h.get(nindex):
                if self.h[nindex][2] == 1:
                    nindex += 1
                else:
                    neighbor += [nindex]
                    nindex +=1
            else :
                neighbor += [nindex]
                nindex += 1


        return neighbor


    # def dijkstra(edges, f, t):
    #     dic = {}
    #     dic[f] =


    #     g = defaultdict(list)
    #     for l,r,c in edges:
    #         g[l].append((c,r))

    #     q, seen = [(0,f,())], set()
    #     while q:
    #         (cost,v1,path) = heappop(q)
    #         if v1 not in seen:
    #             seen.add(v1)
    #             path = (v1, path)
    #             if v1 == t: return (cost, path)

    #             for c, v2 in g.get(v1, ()):
    #                 if v2 not in seen:
    #                     heappush(q, (cost+c, v2, path))

    #     return float("inf")

    # if __name__ == "__main__":
    #     edges = [
    #         ("A", "B", 7),
    #         ("A", "D", 5),
    #         ("B", "C", 8),
    #         ("B", "D", 9),
    #         ("B", "E", 7),
    #         ("C", "E", 5),
    #         ("D", "E", 15),
    #         ("D", "F", 6),
    #         ("E", "F", 8),
    #         ("E", "G", 9),
    #         ("F", "G", 11)
    #     ]





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
