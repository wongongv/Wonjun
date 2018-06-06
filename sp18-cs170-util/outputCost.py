import fileinput
import numpy as np

fin = open('50.in')
lineOne = fin.readline()
lineTwo = fin.readline()
lineThree = fin.readline()
lineRest = fin.readlines()

a = int(lineOne)
lineTwo = lineTwo.split()
lineTwo = np.asarray(lineTwo)


dictionary = {}
for i in range (0,a):
    dictionary[lineTwo[i]] = i

for i in range (0,a):
    lineRest[i] = lineRest[i].split()
    lineRest[i] = np.asarray(lineRest[i])

fin.close()

for i in range(0,a):
    for j in range(0,a):
        if lineRest[i][j] != 'x':
            lineRest[i][j] = float(lineRest[i][j])

fout = open('50.out')

firstLine = fout.readline()
firstLine = firstLine.split()
firstLine = np.asarray(firstLine)
firstInt = [0]*len(firstLine)

for i in range(0, len(firstLine)):
    firstLine[i] = dictionary.get(firstLine[i])
    firstInt[i] = int(firstLine[i])

secondLine = fout.readline()
secondLine = secondLine.split()
secondLine = np.asarray(secondLine)
secondInt = [0]*len(secondLine)

for i in range(0, len(secondLine)):
    secondLine[i] = dictionary.get(secondLine[i])
    secondInt[i] = int(secondLine[i])
fout.close()

cost = 0
for i in range(0, len(secondLine)):
    cost += float(lineRest[secondInt[i]][secondInt[i]])
    
for i in range(0, len(firstLine)-1):
    if lineRest[firstInt[i]][firstInt[i+1]] == 'x':
        print (firstInt[i])
    else:
       cost += float(lineRest[firstInt[i]][firstInt[i+1]])
print(cost)
