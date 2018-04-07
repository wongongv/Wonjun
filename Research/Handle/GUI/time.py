import timeit
import numpy

pylist=timeit.timeit('[a[i]+1 for i in range(1000000)]',setup = 'a=[i for i in range(1000000)]',number =10)
testc='''
import numpy
b=numpy.array([i for i in range(1000000)])
'''
numlist=timeit.timeit('[b[i]+1 for i in range(1000000)]', setup=testc,number =10)


print('pylist:', pylist)
print('numlist:', numlist)
