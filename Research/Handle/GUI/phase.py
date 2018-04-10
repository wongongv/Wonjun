from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
import pdb
from math import sqrt
class phase:
	def __init__(self, win):
		self.win = win
		self.p5 =self.win.addPlot(title = 'Phase')
		self.viewbox=self.p5.getViewBox()
		self.viewbox.setLimits(xMin = -0.01, yMin = -0.01, xMax=1.01, yMax=1.01)
		self.viewbox.setRange(xRange=[0,2*glo_var.alpha_star],yRange=[0,2*glo_var.beta_star],padding=0)
		# self.scat = pg.ScatterPlotItem(size = 1, pen = pg.mkPen('r'), brush =pg.mkBrush(255,255,255,120))
		self.initiate()

	def initiate(self):
		self.p5.clear()

		
		bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		bounds3 = np.array([[0,0],[glo_var.alpha_star,glo_var.beta_star]])
		self.p5.plot(bounds1)
		self.p5.plot(bounds2)
		self.p5.plot(bounds3)

		self.p5.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	def update(self):
		self.p5.clear()
		self.ablim = 0.5/(1+sqrt(glo_var.l))
		self.viewbox.setRange(xRange=[0,self.ablim],yRange=[0,self.ablim],padding=0)	
		self.value_declaration()




		if glo_var.alpha > 2*glo_var.alpha_star:
			glo_var.alpha = 2*glo_var.alpha_star
		if glo_var.beta > 2*glo_var.beta_star:
			glo_var.beta = 2*glo_var.beta_star

		HD = pg.TextItem(html='HD', anchor=(glo_var.alpha_star,0.5*glo_var.beta_star), border='w', fill=(255, 0, 0, 250))
		self.p5.addItem(HD)
		HD.setPos(glo_var.alpha_star,0.5*glo_var.beta_star)
		LD = pg.TextItem(html='LD', anchor=(glo_var.alpha_star*0.3,glo_var.beta_star*1.3), border='w', fill=(0, 255, 0, 200))
		self.p5.addItem(LD)
		LD.setPos(glo_var.alpha_star*0.3,glo_var.beta_star*1.3)
		MC = pg.TextItem(html='MC', anchor=(glo_var.alpha_star*1.2,glo_var.beta_star*1.3), border='w', fill=(0, 0, 255, 200))
		MC.setPos(glo_var.alpha_star*1.2,glo_var.beta_star*1.3)
		self.p5.addItem(MC)
		
		bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		linspace=np.linspace(0,glo_var.alpha_star,20)
		trans_line_val=[]
		for i in linspace:
			trans_line_val += [self.trans_func(i)]
		self.p5.plot(bounds1)
		self.p5.plot(bounds2)
		self.p5.plot(linspace,trans_line_val)

		# self.point = np.array([glo_var.alpha,glo_var.beta])
		# self.spots = [{'pos': self.point, 'size':1e-6, 'pen':{'color':'w','width':2}}]
		# self.scat.addPoints(self.spots)	
		# self.p5.addItem(self.scat)
		self.p5.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	# def receive(self,slid):
	# 	self.slid = slid


	def value_declaration(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values()))
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[glo_var.lambdas_degree - 1][1]

	def trans_func(self, point):
		self.B = point*(self.lambda_0 - point)/(self.lambda_0 + (glo_var.l -1) * point)
		self.trans_b = - self.lambda_1 +(glo_var.l-1)*self.B
		self.trans_intercal = 0 if pow(self.trans_b,2) - 4*self.B*self.lambda_1 < 0.00001 else sqrt(pow(self.trans_b,2) - 4*self.B*self.lambda_1)
		self.trans = (-self.trans_b - self.trans_intercal)/2
		return self.trans
