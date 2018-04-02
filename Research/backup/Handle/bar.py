import numpy as np
import matplotlib.pyplot as plt

def setup_backend(backend='TkAgg'):
    import sys
    del sys.modules['matplotlib.backends']
    del sys.modules['matplotlib.pyplot']
    import matplotlib as mpl
    mpl.use(backend)  # do this before importing pyplot
    import matplotlib.pyplot as plt
    return plt

N = 5
width = 0.35       # the width of the bars: can also be len(x) sequence

def animate():
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    mu, sigma = 100, 15
    h = mu + sigma * np.random.randn((N*2))
    print(h)
    p1 = plt.bar(np.arange(N), h[:N], width, color='r')
    maxh = 0.
    for i in range(50):
        for rect1 in p1.patches:
            h = mu + sigma * np.random.randn(2)
            #Keep a record of maximum value of h
            maxh = max(h[0]+h[1],maxh)
            rect1.set_height(h[0])
        #Set y limits to maximum value
        ax.set_ylim((0,maxh))
        fig.canvas.draw()

plt = setup_backend()
fig, ax = plt.subplots(1,1)
win = fig.canvas.manager.window
win.after(10, animate)
plt.show()

