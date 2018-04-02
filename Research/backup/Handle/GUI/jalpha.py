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
from scipy.interpolate import interp1d

class jalpha:
	def __init__(self, fig):
		self.fig = fig
		self.ax = self.fig.add_subplot(45,1,41)
		self.ax.set_position([0.1,0.7,0.2,0.2])
		self.ax.set_ylim(0,1)
		self.ax.set_xlim(0,1)
		# self.ax.set_facecolor()
		self.update()
		self.update_alpha()
	def update(self):
		self.plot_j()

	def plot_j(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values()))
		self.lambda_min = min(self.lambdas_ys)
		self.j_c = self.lambda_min/pow(1 + sqrt(glo_var.l),2)
		self.lambda_1 = glo_var.lambdas[glo_var.lambdas_degree - 1][1]
		self.j_l=glo_var.alpha*(self.lambda_1-glo_var.alpha)/(self.lambda_1+(glo_var.l-1)*glo_var.alpha)
		self.alphas_pre = np.linspace(0,glo_var.alpha_star,10)
		self.j_l_values=[i*(self.lambda_1-i)/(self.lambda_1+(glo_var.l-1)*i) for i in self.alphas_pre]
		# self.alphas_post = np.linspace(glp_var.alpha, 1, 50)
		self.j_l_g = interp1d(self.alphas_pre,self.j_l_values)
		self.j_c_g = Line2D([glo_var.alpha_star,1],[self.j_c,self.j_c])
		self.ax.plot(self.alphas_pre,self.j_l_g(self.alphas_pre))
		self.ax.add_line(self.j_c_g)

		self.alpha_star_line = Line2D([glo_var.alpha_star,glo_var.alpha_star],[0,1],color = 'r')
		self.ax.add_line(self.alpha_star_line)
	def update_alpha(self):
		self.alpha_line = Line2D([glo_var.alpha,glo_var.alpha],[0,1],linestyle='dashed')
		self.ax.add_line(self.alpha_line)