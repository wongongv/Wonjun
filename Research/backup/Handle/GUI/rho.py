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

# required variables alhpha, beta, lambdas
class rho:
	def __init__(self,fig):

		self.fig = fig
		self.axes = self.fig.add_subplot(40,1,3)
		self.axes.set_position([0.1,0.7,0.3,0.2],which='both')

		self.update()

	def update(self):

		
		self.lambda_0=glo_var.lambdas[0][1]
		self.lambda_1=glo_var.lambdas[glo_var.lambdas_degree - 1][1]
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values()))

		self.lambda_min=min(self.lambdas_ys)
		self.l = glo_var.l
		self.alpha = glo_var.alpha
		self.beta = glo_var.beta

		self.intercall=pow(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_0*self.lambda_min/pow(1+sqrt(self.l),2)
		self.intercalr=pow(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_1*self.lambda_min/pow(1+sqrt(self.l),2)
		self.alpha_star=0.5*(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt( 0 if self.intercall < 0.0000001 else self.intercall))
		self.beta_star=0.5*(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt(0 if self.intercalr < 0.0000001 else self.intercalr))

		self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
		self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
		self.rhointercall=[(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),2) - self.j_l/(self.l*lambda_x)) for lambda_x in self.lambdas_ys]
		self.rhointercalr=[(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),2) - self.j_r/(self.l*lambda_x)) for lambda_x in self.lambdas_ys] 
		self.rho_l=[x - sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercall]
		self.rho_r=[x + sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercalr]

		glo_var.j_l = self.j_l
		glo_var.j_r = self.j_r
		glo_var.alpha_star=self.alpha_star
		glo_var.beta_star=self.beta_star

		self.axes.clear()
		self.axes.set_xlim(0,1)
		self.axes.set_ylim(0,1)
		# think about make it polynomial

		# self.xs = np.linspace(0,1, glo_var.lambdas_degree * 10)
		# self.csl = CubicSpline(self.lambdas_xs, self.rho_l)
		# self.csr = CubicSpline(self.lambdas_xs, self.rho_r)
		# self.axes.plot(self.lambdas_xs, self.rho_l, 'o')
		# self.axes.plot(self.lambdas_xs, self.rho_r, 'o')
		# self.axes.plot(self.xs, self.csl(self.xs))
		# self.axes.plot(self.xs, self.csr(self.xs))
		self.pol_l = interp1d(self.lambdas_xs, self.rho_l, kind = 'quadratic')
		self.pol_r = interp1d(self.lambdas_xs, self.rho_r, kind = 'quadratic')
		self.x = np.linspace(0,1, glo_var.lambdas_degree * 10)
		self.pol_l_plot = self.axes.plot(self.lambdas_xs, self.rho_l, 'o', self.x, self.pol_l(self.x))
		self.pol_r_plot = self.axes.plot(self.lambdas_xs, self.rho_r, 'o', self.x, self.pol_r(self.x))


		# self.linel=Line2D(self.lambdas_xs, self.rho_l, color = 'b')
		# self.liner=Line2D(self.lambdas_xs, self.rho_r, color = 'r')
		# self.rholup = self.axes.add_line(self.linel)
		# self.rhorup = self.axes.add_line(self.liner)
		# self.rholup.set_ydata(self.rho_l)
		# self.rhorup.set_ydata(self.rho_r)

	def clear(self):
		self.axes.remove()