
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

class lamb_pol:
	def __init__(self,win) :
		self.win = win
		self.p1 = self.win.addPlot(title = '\u03bb')
		self.viewbox=self.p1.getViewBox()
		self.viewbox.setLimits(xMin = -0.02, yMin = -0.02, xMax = 1.02, yMax = 1.02)
		self.viewbox.setRange(xRange=[-0.02,1.02],yRange=[-0.02,1.02],padding =0)
		self.update()

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
		# self.f=interp1d(self.x,self.y, kind='quadratic')
		# self.linspace = np.linspace(0,1,100)
		# self.p1.plot(self.linspace, self.f(self.linspace))
		self.p1.plot(self.x, self.y, symbolBrush=(200,100,100), symbolPen='w')
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