import numpy as np
import random
import math
import scipy
from student_utils_sp18 import *

a = 3000000
b = 4000000
c = 5000000

amount = 50
G = nx.Graph()

G.add_node(0)
G.add_edge(0, 0, weight = 100000000)

start = 0

for i in range(1, amount - 3, 3):
    r = random.random()
    s = random.random()
    t = random.random()
    G.add_edge(start, i, weight = 3)
    G.add_edge(i, i, weight = 10000000)
    G.add_edge(i + 1 , i + 1, weight = 1000000)
    G.add_edge(i + 2 , i + 2, weight = 1000000)
    G.add_edge(i, i + 1, weight=a )
    G.add_edge(i + 1, i + 2, weight = c )
    G.add_edge(i + 2, i, weight = b )
    start = i + 2


A = nx.to_numpy_matrix(G).tolist()
print(A)
p = amount - 1
file = open(str(amount) + ".in", "w")
file.write(str(p) + "\n")
for i in range(0,p):
    file.write("city")
    if i == a-1:
        file.write(str(i))
    else:
        file.write(str(i) + ' ')

file.write("\ncity0\n")

for i in A:
    for x in i:
        if x == 0:
            file.write("x ")
        else:
            file.write(str(int(x)) + " ")

    file.write('\n')
