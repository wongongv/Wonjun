
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
import pdb
from scipy.interpolate import interp1d

# from scipy.interpolate import CubicSpline
# from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
# import math
# from matplotlib.backend_bases import MouseEvent
# from matplotlib.lines import Line2D
# from math import sqrt
# from matplotlib.widgets import AxesWidget
# import six
# import pdb

class myscat(pg.ScatterPlotItem):
	def mouseClickEvent(self, ev):
		if ev.button() == QtCore.Qt.LeftButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.sigClicked.emit(self, self.ptsClicked)
				ev.accept()
			else:
				#print "no spots"
				ev.ignore()
		
		elif ev.button() == QtCore.Qt.RightButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.raisecontextmenu(pts, ev)
				self.sigClicked.emit(self,self.ptsClicked)
				ev.accept()
			else:
				ev.ignore()
		else:
			ev.ignore()
	def set_yval(self, value):
		self.ptsClicked._data[1] = value

	def raisecontextmenu(self, point, ev):
		self.menu = Menu(self, point)
		self.menu.popup(ev.screenPos().toQPoint())

class Menu(QtGui.QMenu):
	def __init__(self, item, point):
		QtGui.QMenu.__init__(self)
		self.point = point
		self.item = item
		# self.removal = self.addAction("Remove point", lambda)

class lamb_pol:
	def __init__(self,win) :
		self.win = win
		self.p1 = self.win.addPlot(title = '\u03bb')
		self.viewbox=self.p1.getViewBox()
		self.viewbox.setLimits(xMin = -0.02, yMin = -0.02, xMax = 1.02, yMax = 1.02)
		self.viewbox.setRange(xRange=[-0.02,1.02],yRange=[-0.02,1.02],padding =0)
		self.sp = myscat(size = 10, pen = pg.mkPen(None), brush=pg.mkBrush(200,100,100))
		self.lastClicked=[]
		# self.x, self.y = zip(*sorted(glo_var.lambdas.values()))
		# self.lambs = np.array([self.x,self.y])
		# self.spots = [{'pos':self.lambs[:,i], 'data': 1} for i in range(glo_var.lambdas_degree)]
		# self.sp.addPoints(self.spots)
		# self.p1.addItem(self.sp)

		self.viewbox.menu = None
		self.update()

## create four areas to add plots
# w1 = view.addPlot()
# w2 = view.addViewBox()
# w2.setAspectLocked(True)
# view.nextRow()
# w3 = view.addPlot()
# w4 = view.addPlot()
# print("Generating data, this takes a few seconds...")

## There are a few different ways we can draw scatter plots; each is optimized for different types of data:


## 1) All spots identical and transform-invariant (top-left plot). 
## In this case we can get a huge performance boost by pre-rendering the spot 
## image and just drawing that image repeatedly.

# n = 300
# s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
# pos = np.random.normal(size=(2,n), scale=1e-5)
# spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
# s1.addPoints(spots)
# w1.addItem(s1)

# ## Make all plots clickable
# lastClicked = []
# def clicked(plot, points):
#     global lastClicked
#     for p in lastClicked:
#         p.resetPen()
#     print("clicked points", points)
#     for p in points:
#         p.setPen('b', width=2)
#     lastClicked = points
# s1.sigClicked.connect(clicked)



	# def update(self):
	# 	self.ax.clear()
	# 	self.ax.set_ylim(0,1)
	# 	self.ax.set_xlim(0,1)
	# 	self.pol_points=glo_var.lambdas
	# 	self.pol_x, self.pol_y = zip(*sorted(self.pol_points.values()))
	# 	self.pol_z=np.polyfit(self.pol_x, self.pol_y, glo_var.lambdas_degree-1) # Use the interactive widget! that receives input.
	# 	self.pol_f=np.poly1d(self.pol_z)
	# 	self.x = np.linspace(0,1,glo_var.lambdas_degree * 10)							 # maybe need to change 50 according to the # of knobs
	# 	self.y = self.pol_f(self.x)
	# 	self.initial_pol = self.ax.plot(self.pol_x, self.pol_y, 'o', self.x, self.y)
	def update(self):
		self.p1.clear()
		self.x, self.y = zip(*sorted(glo_var.lambdas.values()))
		# self.lambs = np.array([self.x,self.y])
		# self.spots = [{'pos':self.lambs[:,i], 'data': 1} for i in range(glo_var.lambdas_degree)]
		# self.sp.addPoints(self.spots)


		self.p1.plot(self.x, self.y)
		self.sp.setData(self.x,self.y)
		self.sp.sigClicked.connect(self.clicked)		
		self.p1.addItem(self.sp)

	def clicked(self, item, points):
		self.points=points
		for p in self.lastClicked:
			p.resetPen()
		for p in points:
			p.setPen('b', width=2)
			glo_var.lambdas.remove((p._data[0],p._data[1]))
		self.lastClicked = points


		




		# glo_var.lambda_function = self.f
		# self.ax.clear()
		# self.ax.set_ylim(0,1)
		# self.ax.set_xlim(0,1)
		# self.pol_points=glo_var.lambdas
		# self.pol_x, self.pol_y = zip(*sorted(self.pol_points.values()))
		# self.pol_z = interp1d(self.pol_x, self.pol_y)
		# # self.pol_z=CubicSpline(self.pol_x, self.pol_y) # Use the interactive widget! that receives input.
		# # self.pol_f=np.poly1d(self.pol_z)
		# self.x = np.linspace(0,1,glo_var.lambdas_degree * 10)							 # maybe need to change 50 according to the # of knobs
		# # self.y = self.pol_f(self.x)
		# self.initial_pol = self.ax.plot(self.pol_x, self.pol_y, 'o', self.x, self.pol_z(self.x))
	# def clear(self):
		# self.ax.remove()
	# def new_update(self):
	# 	self.p1.setData