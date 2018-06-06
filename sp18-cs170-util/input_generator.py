import numpy as np
import random
import math

a = 50

matrix = np.random.randint(1, 1000000,(a, a))


select=[set() for i in range(a)]

for i in range(0, a - 2):
    while len(select[i]) < 3:
        rand = random.randint(i+1, a)
        if rand not in select[i]:
            select[i].add(rand)
            
final = [[0]*a for i in range(a)]


for i in range(0,a):
    for j in range(0,a):
        if i == j:
            final[i][j] = matrix[i][j]
        else:
            sum = 0
            for k in range(a):
                sum += (matrix[i][k] - matrix[j][k]) **2
                
            sqrt = math.sqrt(sum)
            final[i][j] = round(sqrt, 5)


for i in range(0, a):
    for j in range(0,a):
        if i < j:
            if j not in select[i]:
                final[i][j] = 'x'

for i in range(0, a):
    for j in range(0, a):
        if i > j:
            if final[j][i] == 'x':
                final[i][j] = 'x'           

file = open("50.in", "w")
file.write("50\n")
for i in range(0,a):
    file.write("city")
    if i == a-1:
        file.write(str(i))
    else:
        file.write(str(i) + ' ')
    
file.write("\ncity0\n")
for i in range(0,a):
    for j in range(0,a):
        if j == a-1:
            file.write(str(final[i][j]))
        else:
            file.write(str(final[i][j]) + ' ')
    if i != a-1:
        file.write("\n")
file.close()
