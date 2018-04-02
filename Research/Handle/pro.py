import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


# alpha, beta handle 1

class axes:

	def __init__(self, line):
		canvas = line.figure.canvas
		self.canvas = canvas
		self.line = line
		self.axes = line.axes
		self.xs = list(self.line.get_xdata())
		self.ys = list(self.line.get_ydata())

		self.ind = None

		canvas.mpl_connect('button_press_event', self.button_press_callback)
		canvas.mpl_connect('button_release_event', self.button_release_callback)
		canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)


	def get_ind(self, event):
		x = np.array(self.line.get_xdata())
		y = np.array(self.line.get_ydata())
		d = np.sqrt((x-event.xdata)**2 + (y - event.ydata)**2)
		if min(d) > self.epsilon:
			return None
		if d[0] < d[1]:
			return 0
		else:
			return 1

	def button_press_callback(self, event):
		if event.button != 1:
			return
		self.ind = self.get_ind(event)
		print(self.ind)

		self.line.set_animated(True)
		self.canvas.draw()
		self.background = self.canvas.copy_from_bbox(self.line.axes.bbox)

		self.axes.draw_artist(self.line)
		self.canvas.blit(self.axes.bbox)

	def button_release_callback(self, event):
		if event.button != 1:
			return
		self.ind = None
		self.line.set_animated(False)
		self.background = None
		self.line.figure.canvas.draw()

	def motion_notify_callback(self, event):
		if event.inaxes != self.line.axes:
			return
		if event.button != 1:
			return
		if self.ind is None:
			return
		self.xs[self.ind] = event.xdata
		self.ys[self.ind] = event.ydata
		self.line.set_data(self.xs, self.ys)

		self.canvas.restore_region(self.background)
		self.axes.draw_artist(self.line)
		self.canvas.blit(self.axes.bbox)

fig=plt.figure()
ax1=fig.add_subplot(311)
x=[2,2]
y=[1,1]
ax1.set_ylim(0,1)
line=Line1D(x,y, marker = 'o', markerfacecolor = 'red')
ax1.add_line(line)









#result. bar plot
ax3=fig.add_subplot(3,1,3)
x=['Lambda','J']
y=[1,2]
ax3.bar(x,y,animated=True)
plt.show()