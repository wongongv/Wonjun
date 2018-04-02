import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from math import sqrt
from matplotlib.widgets import AxesWidget
from matplotlib.widgets import Button
import six
import pdb
import vert_slider
import glo_var
import lamb_pol
import slide
import rho
import gc
import jbeta
import jalpha


# fig = plt.figure()
# fig.set_size_inches(18.5, 10.5, forward=True)


# # vert_slider
# vs = vert_slider.make_vs(fig)

# # lambda polynomial
# lambda_poly = lamb_pol.lamb_pol(fig)

# vs.receive(lambda_poly)


# # rho

# rhos = rho.rho(fig)
# # slider
# slider = slide.make_slide(fig, vs.vslides[glo_var.lambdas_degree],vs.vslides[glo_var.lambdas_degree + 1], rhos)





# buttons
class main_class(object):
	ind = 0

	def __init__(self):
# button varaibles
		self.lam=1
		self.r=1
# figure
		self.fig = plt.figure(facecolor = 'gray')
		self.fig.set_size_inches(18.5, 10.5, forward=True)
		
# vert slider
		self.vs = vert_slider.make_vs(self.fig)
# lambda poly
		self.lambda_poly = lamb_pol.lamb_pol(self.fig)


# rho
		self.rhos = rho.rho(self.fig)
# slider
		self.slider = slide.make_slide(self.fig, self.vs.vslides[glo_var.lambdas_degree],self.vs.vslides[glo_var.lambdas_degree + 1], self.rhos)
# receive
		self.vs.receive(self.lambda_poly, self.rhos)

		self.jbet = jbeta.jbeta(self.fig)
		self.jalph = jalpha.jalpha(self.fig)
	def reset_lamb(self, event):

		if self.lam == 1:
			self.lam = 0
			self.lambda_poly.clear()
			self.lambda_poly = None
			self.vs.delete('lambda_poly')
			gc.collect()

		else :
			self.lam = 1
			self.lambda_poly = lamb_pol.lamb_pol(self.fig)
			self.vs.receive(self.lambda_poly, self.rhos)

	def reset_rhos(self, event):
		if self.r == 1:
			self.r = 0
			self.rhos.clear()
			self.rhos = None
			self.vs.delete('rhos')
			gc.collect()
		else :
			self.r = 1
			self.rhos = rho.rho(self.fig)
			self.vs.receive(self.lambda_poly,self.rhos)

	def update_all(self):
		self.rhos.update()


	def increment_l(self,event):
		glo_var.l += 1
		self.update_all()
		print(glo_var.l)
	def decrement_l(self,event):
		if glo_var.l >= 1:
			glo_var.l -= 1
			self.update_all()
		print(glo_var.l)
main = main_class()
lamb_pol_bup = plt.axes([0.7,0.05,0.1,0.075])
Increase_l_bup = plt.axes([0.1,0.05,0.1,0.075])
Decrease_l_bup = plt.axes([0.3,0.05,0.1,0.075])

# sli_bup =
rhos_bup = plt.axes([0.4,0.05,0.1,0.075])
# vs_bup =
# sli_button = Button
rhos_button = Button(rhos_bup,r'$\rho$ Graph')
lamb_pol_button = Button(lamb_pol_bup, r'$\lambda$ Graph')
Increase_l_button = Button(Increase_l_bup, 'Increment l')
Decrease_l_button = Button(Decrease_l_bup, 'Decrement l')
# vs_button = 
rhos_button.on_clicked(main.reset_rhos)
lamb_pol_button.on_clicked(main.reset_lamb)
Increase_l_button.on_clicked(main.increment_l)
Decrease_l_button.on_clicked(main.decrement_l)

# executing
plt.show()



#  To Do  : cursor move -> alpha beta switch update. Think about it. 