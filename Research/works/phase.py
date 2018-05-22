from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt


import pdb
class MyROI(pg.ROI):
	def __init__(self, pos, size=[0.03,0.03], angle=0.0, invertible=False, maxBounds=None, snapSize=1.0, scaleSnap=False, translateSnap=False, rotateSnap=False, parent=None, pen=None, movable=True, removable=False):
		super().__init__(pos, size)

	def paint(self, p, opt, widget):
		# Note: don't use self.boundingRect here, because subclasses may need to redefine it.
		r = QtCore.QRectF(0, 0, self.state['size'][0], self.state['size'][1]).normalized()
		p.setRenderHint(QtGui.QPainter.Antialiasing)
		p.setPen(self.currentPen)
		p.translate(r.left(), r.top())
		p.scale(r.width(), r.height())
		p.drawEllipse(0, 0, 1, 1)

	def mouseDragEvent(self, ev):
		super().mouseDragEvent(ev)
		self.posi = self.pos()
		a = self.posi[0]
		b = self.posi[1]
		self.slid.update_phas(a, b)
		self.legend(a,b)
	def receive(self, slid, phas):
		self.slid = slid
		self.phas = phas
	def legend(self, a, b):

		if a > glo_var.alpha_star and b > glo_var.beta_star:
			region = 'MC'
			penn = self.phas.purple
		elif a> glo_var.alpha_star:
			region = 'HD ||'
			penn = self.phas.red
		elif b> glo_var.beta_star:
			region = 'LD ||'
			penn = self.phas.blue
		elif b > self.phas.trans_func(a):
			region = 'LD |'
			penn = self.phas.blue
		else:
			penn = self.phas.red
			region = 'HD |'
		self.phas.pointer.setPen(penn)
		self.phas.leg.items = []
		self.phas.p5.plot(pen=penn, name=region)
		
class myscat(pg.ScatterPlotItem):

	def mouseClickEvent(self, ev):
		if ev.button() == QtCore.Qt.LeftButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
				self.sigClicked.emit(self, self.ptsClicked)
				ev.accept()
			elif self.lamb_po.curve.mouseShape().contains(ev.pos()):
				self.ptsClicked = pts
				self.toadd = [ev.pos()[0], ev.pos()[1]]
				glo_var.lambdas += [self.toadd]
				glo_var.lambdas.sort()
				glo_var.lambdas_degree += 1
				self.slid.update_lamb_rh_add()
				self.lamb_po.lastClicked.resetPen()
				self.lamb_po.lastClicked = []
				ev.accept()
			else:
				# print "no spots"
				self.lamb_po.lastClicked[0].resetPen()
				self.lamb_po.lastClicked = []

				ev.ignore()

		elif ev.button() == QtCore.Qt.RightButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
				self.raisecontextmenu(pts, ev)
				ev.accept()
			else:
				self.lamb_po.lastClicked[0].resetPen()
				self.lamb_po.lastClicked = []
				ev.ignore()
		else:
			ev.ignore()



	def mouseMoveEvent(self, ev):
		pts = self.pointsAt(ev.pos())
		if len(pts) > 0 :
			self.ptsClicked = pts
			self.sigClicked.emit(self, self.ptsClicked)
			ev.accept()




class phase:
	def __init__(self, dphase):
		self.purple = pg.mkPen(QtGui.QColor(20,20,140,255))
		self.red = pg.mkPen(QtGui.QColor(180,0,0,255))
		self.blue = pg.mkPen(QtGui.QColor(20,20,140,255))
		self.roicolor = QtGui.QPen()
		self.roicolor.setBrush(QtGui.QColor(20,20,140,255))

		# self.roicolor = QtGui.QPen.brush(QtGui.QColor(20,20,140,255))
		self.dphase = dphase
		self.p5 = glo_var.MyPW()
		# self.p5=pg.PlotWidget()

		# self.point = myscat([glo_var.alpha_star], [glo_var.beta_star])
		# self.p5.plot([glo_var.alpha],[glo_var.beta],pen='r', symbol='o')

		self.viewbox = self.p5.getPlotItem().getViewBox()
		self.viewbox.setBackgroundColor('w')

		self.frame = glo_var.setframe(self.p5, width = 1)
		self.dphase.addWidget(self.frame)
		self.viewbox.setLimits(xMin = -0.01, yMin = -0.01, xMax=1.01, yMax=1.01)
		self.viewbox.setRange(xRange=[0,2*max(glo_var.alpha,glo_var.alpha_star)],yRange=[0,2*max(glo_var.beta, glo_var.beta_star)],padding=0)
		self.viewbox.menu = None

		self.p5.plotItem.addLegend = glo_var.myaddLegend
		self.p5.addLegend(self.p5.plotItem)


		self.p5.plot(pen=self.blue, name='LD |')
		self.leg = self.p5.plotItem.legend

		self.p5.setLabel('bottom',"\u03b1",**glo_var.labelstyle)
		self.p5.setLabel('left',"\u03b2",**glo_var.labelstyle)
		# self.scat = pg.ScatterPlotItem(size = 1, pen = pg.mkPen('r'), brush =pg.mkBrush(255,255,255,120))
		self.initiate()

	def initiate(self):
		self.p5.clear()

		# self.pointer = myscat([glo_var.alpha_star], [glo_var.beta_star])

		# self.curve=pg.PlotCurveItem(np.array(self.x), np.array(self.y))
		# self.curve.setPen(pg.mkPen('k'))
		# self.p1.addItem(self.curve)
		# self.sp.setData(self.x,self.y)
		# self.sp.sigClicked.connect(self.clicked)
		# self.p1.addItem(self.sp)

		self.ablim = 0.5/(1+sqrt(glo_var.l))
		self.pointer = MyROI([glo_var.alpha, glo_var.beta], size = [glo_var.alpha_star/10,glo_var.beta_star/10])
		self.pointer.setPen(self.roicolor)
		# self.bounds1 = pg.PlotCurveItem(np.array([glo_var.alpha_star,1]),np.array([1,glo_var.beta_star]))
		# self.bounds1.setPen(pg.mkPen('k'))
		self.bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		self.bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		self.bounds3 = np.array([[0,0],[glo_var.alpha_star,glo_var.beta_star]])
		self.p5.plot(self.bounds1)
		self.p5.plot(self.bounds2)
		self.p5.plot(self.bounds3)
		# self.p5.plot([glo_var.alpha],[glo_var.beta],pen='r', symbol='o')
		# self.p5.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	def update(self):
		self.p5.clear()


		# r = pg.PolyLineROI([(glo_var.alpha_star, glo_var.beta_star)])
		self.p5.addItem(self.pointer)

		
		self.pointer.setPos(glo_var.alpha,glo_var.beta)
		# self.ablim = 0.5/(1+sqrt(glo_var.l))
		# self.viewbox.setRange(xRange=[0,self.ablim],yRange=[0,self.ablim],padding=0)	

		self.value_declaration()



		if glo_var.alpha > 2*glo_var.alpha_star:
			glo_var.alpha = 2*glo_var.alpha_star
		if glo_var.beta > 2*glo_var.beta_star:
			glo_var.beta = 2*glo_var.beta_star

		HD = pg.TextItem(html='HD', anchor=(glo_var.alpha_star,0.5*glo_var.beta_star), border='w', fill=(255, 0, 0, 250))
		# self.p5.addItem(HD)
		HD.setPos(glo_var.alpha_star,0.5*glo_var.beta_star)
		LD = pg.TextItem(html='LD', anchor=(glo_var.alpha_star*0.3,glo_var.beta_star*1.3), border='w', fill=(0, 255, 0, 200))
		# self.p5.addItem(LD)
		LD.setPos(glo_var.alpha_star*0.3,glo_var.beta_star*1.3)
		MC = pg.TextItem(html='MC', anchor=(glo_var.alpha_star*1.2,glo_var.beta_star*1.3), border='w', fill=(0, 0, 255, 200))
		MC.setPos(glo_var.alpha_star*1.2,glo_var.beta_star*1.3)
		# self.p5.addItem(MC)
		
		# self.bounds1.setData(np.array([glo_var.alpha_star,glo_var.beta_star]),np.array([1,glo_var.beta_star]))


		# self.pointer = self.MyROI([self.ablim/2, self.ablim/2], size = [glo_var.alpha_star/10,glo_var.beta_star/10])

		self.bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		self.bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		linspace=np.linspace(0,glo_var.alpha_star,20)
		trans_line_val=[]
		for i in linspace:
			trans_line_val += [self.trans_func(i)]
		self.p5.plot(self.bounds1, pen = 'k')
		self.p5.plot(self.bounds2, pen = 'k')
		self.p5.plot(linspace,trans_line_val, pen = 'k')

		# self.point = np.array([glo_var.alpha,glo_var.beta])
		# self.spots = [{'pos': self.point, 'size':1e-6, 'pen':{'color':'w','width':2}}]
		# self.scat.addPoints(self.spots)	
		# self.p5.addItem(self.scat)
		# self.p5.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	# def receive(self,slid):
	# 	self.slid = slid


	def value_declaration(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas))
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[ - 1][1]

	def trans_func(self, point):
		self.B = point*(self.lambda_0 - point)/(self.lambda_0 + (glo_var.l -1) * point)
		self.trans_b = - self.lambda_1 +(glo_var.l-1)*self.B
		self.trans_intercal = 0 if pow(self.trans_b,2) - 4*self.B*self.lambda_1 < 0.00001 else sqrt(pow(self.trans_b,2) - 4*self.B*self.lambda_1)
		self.trans = (-self.trans_b - self.trans_intercal)/2
		return self.trans

	def receive(self, slid):
		self.pointer.receive(slid, self)