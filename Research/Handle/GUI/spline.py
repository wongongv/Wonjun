from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
import pdb
x = np.arange(10)
y = np.sin(x)
cs = CubicSpline(x, y)
pdb.set_trace()
xs = np.arange(-0.5, 9.6, 0.1)
plt.figure(figsize=(6.5, 4))
plt.plot(x, y, 'o', label='data')
plt.plot(xs, np.sin(xs), label='true')
plt.plot(xs, cs(xs), label="S")
plt.plot(xs, cs(xs, 1), label="S'")
plt.plot(xs, cs(xs, 2), label="S''")
plt.plot(xs, cs(xs, 3), label="S'''")
plt.xlim(-0.5, 9.5)
plt.legend(loc='lower left', ncol=2)
plt.show()