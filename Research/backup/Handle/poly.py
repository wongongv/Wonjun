import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np

points=np.array([(1,1),(2,4),(3,1),(9,3)])

print(points)

x=points[:,0]
y=points[:,1]
print(type(x))
print(y)

z=np.polyfit(x,y,5)
print(z)
f=np.poly1d(z)
print(f)

x_new=np.linspace(x[0],x[-1],50)
print(x_new)
print(x[0])
y_new=f(x_new)
print(y_new)

plt.plot(x,y,'*',x_new,y_new)
pylab.title('Poly')
ax=plt.gca()
print('ax',ax)
ax.set_facecolor((0.898,0.898,0.898))
fig=plt.gcf()
print('fig',fig)
plt.show()
