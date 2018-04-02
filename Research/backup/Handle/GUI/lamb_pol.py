import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from math import sqrt
from matplotlib.widgets import AxesWidget
import six
import pdb
import glo_var
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d

class lamb_pol:
	def __init__(self,fig) :
		self.fig = fig
		self.ax = self.fig.add_subplot(40,1,5)
		self.ax.set_position([0.35,0.4,0.53,0.2],which='both')
		self.degree = len(glo_var.lambdas)
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
		self.ax.clear()
		self.ax.set_ylim(0,1)
		self.ax.set_xlim(0,1)
		self.pol_points=glo_var.lambdas
		self.pol_x, self.pol_y = zip(*sorted(self.pol_points.values()))
		self.pol_z = interp1d(self.pol_x, self.pol_y)
		# self.pol_z=CubicSpline(self.pol_x, self.pol_y) # Use the interactive widget! that receives input.
		# self.pol_f=np.poly1d(self.pol_z)
		self.x = np.linspace(0,1,glo_var.lambdas_degree * 10)							 # maybe need to change 50 according to the # of knobs
		# self.y = self.pol_f(self.x)
		self.initial_pol = self.ax.plot(self.pol_x, self.pol_y, 'o', self.x, self.pol_z(self.x))
	def clear(self):
		self.ax.remove()
