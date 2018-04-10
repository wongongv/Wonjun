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
import csv
import mawin
import pyqtgraph.widgets.RemoteGraphicsView
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

	def __init__(self,app):

		# for i in range(24):
		# 	glo_var.lambdas[i]=[i/23,0.8]
		# self.read_file()
# 		# self.app1 = QtGui.QApplication([])
# # to pdb
# 		glo_var.lambdas=[[0.1,0.5],[0.2,0.7]]
# 		glo_var.lambdas_degree = 2
# 		glo_var.alpha =0.1
# 		glo_var.beta = 0.2
# 		glo_var.l =1
# # delete it!

		self.app1 = app
		
# 

		# self.win = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()

		# self.win.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 
# 


		self.win = pg.GraphicsWindow(title = "TASEP")
		self.win.setWindowIcon(QtGui.QIcon('berkeleylogo1.png'))
		self.win.resize(1200,720)
		self.win.setWindowTitle('TASEP')


		
		pg.setConfigOptions(antialias=True)

		self.lamb_po = lamb_pol.lamb_pol(self.win)
		self.rh=rho.rho(self.win)



		self.phas=phase.phase(self.win)
		self.win.nextRow()
		self.jalph = jalpha.jalpha(self.win, self.rh)
		self.jbet = jbeta.jbeta(self.win, self.rh)

		# self.win.nextRow()
		self.slid=slider.Widget(self.win, self.lamb_po,self.phas, self.rh, self.jbet,self.jalph)
		self.lamb_po.receive(self.slid)
		self.layout = pg.LayoutWidget()
		# self.checkboxes()

	def checkboxes(self):
		self.alphacheck()

	def alphacheck(self):
		self.alphline = QtGui.QCheckBox('\u03B1 line')
		self.alproxy=QtGui.QGraphicsProxyWidget()
		self.alproxy.setWidget(self.alphline)
		self.win.addItem(self.alphline)
		self.alphline.stateChanged.connect(self.alphstate)




# view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
# pg.setConfigOptions(antialias=True)  ## this will be expensive for the local plot
# view.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process! 
# view.setWindowTitle('pyqtgraph example: RemoteSpeedTest')

# label = QtGui.QLabel()
# rcheck = QtGui.QCheckBox('plot remote')
# rcheck.setChecked(True)
# lcheck = QtGui.QCheckBox('plot local')
# lplt = pg.PlotWidget()
# layout = pg.LayoutWidget()
# layout.addWidget(rcheck)
# layout.addWidget(lcheck)
# layout.addWidget(label)
# layout.addWidget(view, row=1, col=0, colspan=3)
# layout.addWidget(lplt, row=2, col=0, colspan=3)
# layout.resize(800,800)
# layout.show()
	def alphstate(self):
		self.alph.alphacheck * (-1)
		self.alph.update()
	def betacheck(self):
		return
	def rhocheck(self):
		return
	def phasecheck(self):
		return


	# def read_file(self, input):
	
	# 	if input[-3:] == csv:
	# 		with open('input1.csv', newline='') as csvfile:
	# 			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	# 			lis = []
	# 			for j in spamreader:
	# 				lis += j
	# 			glo_var.lambdas_degree = int(len(lis)/2)
	# 			for i in range(glo_var.lambdas_degree):
	# 				glo_var.lambdas[i] = [eval(lis[i])/100, eval(lis[i + glo_var.lambdas_degree])]
	# 		glo_var.alpha = 0.1
	# 		glo_var.beta = 0.1
	# 		glo_var.l = 1

	# 	elif input[-3:] === txt:
	# 		f = open(input,'r')
	# 		N = int(f.readline().strip())	
	# 		while(N>3):
	# 			T = f.readline().strip()
	# 			glo_var.lambdas[glo_var.lambdas_degree]=[eval(T)[0],eval(T)[1]]
	# 			glo_var.lambdas_degree+=1
	# 			N-=1
	# 		glo_var.alpha = float(f.readline().strip())
	# 		glo_var.beta = float(f.readline().strip())
	# 		glo_var.l = int(f.readline().strip())
		

		# f = open('data.txt','r')
		# N = int(f.readline().strip())	

		# while(N>3):
		# 	T = f.readline().strip()
		# 	glo_var.lambdas[glo_var.lambdas_degree]=[eval(T)[0],eval(T)[1]]
		# 	glo_var.lambdas_degree+=1
		# 	N-=1

		# glo_var.alpha = float(f.readline().strip())
		# glo_var.beta = float(f.readline().strip())
		# glo_var.l = int(f.readline().strip())

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

# # executing
# # # plt.show()
# main = main_class(QtGui.QApplication(sys.argv))


# # #  To Do  : cursor move -> alpha beta switch update. Think about it. 
# if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     QtGui.QApplication.instance().exec_()
