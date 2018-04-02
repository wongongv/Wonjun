import sys

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
# import six
import pdb
# import vert_slider
import glo_var
import lamb_pol
import slider
import rho
# import gc
import jbeta
import jalpha
import phase

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



# dependencies
# l -> j
# alpha -> j
# beta -> j
# alphastar ->
# betastar ->
# lambda -> a,b_stars, 

# buttons
class main_class(object):
	ind = 0

	def __init__(self):

		# for i in range(24):
		# 	glo_var.lambdas[i]=[i/23,0.8]
		self.read_file()
		self.app1 = QtGui.QApplication([])
		self.win = pg.GraphicsWindow(title = "TASEP")
		self.win.setWindowIcon(QtGui.QIcon('berkeleylogo1.png'))
		self.win.resize(1200,720)
		self.win.setWindowTitle('TASEP')

		pg.setConfigOptions(antialias=True)

		self.lamb_po = lamb_pol.lamb_pol(self.win)
		self.rh=rho.rho(self.win)

# button varaibles
		# self.lam=1
		# self.r=1
# figure
		# self.fig = plt.figure(facecolor = 'gray')
		# self.fig.set_size_inches(18.5, 10.5, forward=True)
		
# vert slider
		# self.vs = vert_slider.make_vs(self.fig)
# lambda poly
		# self.lambda_poly = lamb_pol.lamb_pol(self.fig)


# rho
		# self.rhos = rho.rho(self.fig)
# slider
		# self.slider = slide.make_slide(self.fig, self.vs.vslides[glo_var.lambdas_degree],self.vs.vslides[glo_var.lambdas_degree + 1], self.rhos)
# receive
		# self.vs.receive(self.lambda_poly, self.rhos)

		self.win.nextRow()
		self.jbet = jbeta.jbeta(self.win, self.rh)
		self.jalph = jalpha.jalpha(self.win, self.rh)
		self.phas=phase.phase(self.win)
		# self.win.nextRow()
		self.slid=slider.Widget(self.win, self.lamb_po,self.phas, self.rh, self.jbet,self.jalph)

	def read_file(self):
		f = open('data.txt','r')
		N = int(f.readline().strip())	

		while(N>3):
			T = f.readline().strip()
			glo_var.lambdas[glo_var.lambdas_degree]=[eval(T)[0],eval(T)[1]]
			glo_var.lambdas_degree+=1
			N-=1

		glo_var.alpha = float(f.readline().strip())
		glo_var.beta = float(f.readline().strip())
		glo_var.l = int(f.readline().strip())
		
main = main_class()
# lamb_pol_bup = plt.axes([0.7,0.05,0.1,0.075])
# Increase_l_bup = plt.axes([0.1,0.05,0.1,0.075])
# Decrease_l_bup = plt.axes([0.3,0.05,0.1,0.075])

# sli_bup =
# rhos_bup = plt.axes([0.4,0.05,0.1,0.075])
# # vs_bup =
# # sli_button = Button
# rhos_button = Button(rhos_bup,r'$\rho$ Graph')
# lamb_pol_button = Button(lamb_pol_bup, r'$\lambda$ Graph')
# Increase_l_button = Button(Increase_l_bup, 'Increment l')
# Decrease_l_button = Button(Decrease_l_bup, 'Decrement l')
# # vs_button = 
# rhos_button.on_clicked(main.reset_rhos)
# lamb_pol_button.on_clicked(main.reset_lamb)
# Increase_l_button.on_clicked(main.increment_l)
# Decrease_l_button.on_clicked(main.decrement_l)

# executing
# plt.show()



#  To Do  : cursor move -> alpha beta switch update. Think about it. 
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
