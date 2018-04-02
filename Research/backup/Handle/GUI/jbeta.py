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

class jbeta:
	def __init__(self, fig):
		self.fig = fig
		self.ax = self.fig.add_subplot(40,1,40)
		self.ax.set_position([0.4,0.7,0.2,0.2])
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
		self.lambda_1 = glo_var.lambdas[0][1]
		self.j_r=glo_var.beta*(self.lambda_1-glo_var.beta)/(self.lambda_1+(glo_var.l-1)*glo_var.beta)
		self.betas_pre = np.linspace(0,glo_var.beta_star,10)
		self.j_r_values=[i*(self.lambda_1-i)/(self.lambda_1+(glo_var.l-1)*i) for i in self.betas_pre]
		# self.betas_post = np.linspace(glp_var.beta, 1, 50)
		self.j_r_g = interp1d(self.betas_pre,self.j_r_values)
		self.j_c_g = Line2D([glo_var.alpha_star,1],[self.j_c,self.j_c])
		self.ax.plot(self.betas_pre,self.j_r_g(self.betas_pre))
		self.ax.add_line(self.j_c_g)

		self.alpha_star_line = Line2D([glo_var.alpha_star,glo_var.alpha_star],[0,1],color = 'r')
		self.ax.add_line(self.alpha_star_line)
	def update_alpha(self):
		self.alpha_line = Line2D([glo_var.alpha,glo_var.alpha],[0,1],linestyle='dashed')
		self.ax.add_line(self.alpha_line)