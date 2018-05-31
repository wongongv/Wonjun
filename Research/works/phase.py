from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt



class Cursor_Point(pg.GraphItem):
	def __init__(self, phas):
		self.dragPoint = None
		self.dragOffset = None
		self.textItems = []
		self.region_bef = None
		self.region_aft = None
		self.phas= phas
		pg.GraphItem.__init__(self)


	def setData(self, **kwds):
		self.text = kwds.pop('text', [])
		self.data = kwds
		if 'pos' in self.data:
			npts = self.data['pos'].shape[0]
			self.data['data'] = np.empty(npts, dtype=[('index', int)])
			self.data['data']['index'] = np.arange(npts)
		self.setTexts(self.text)
		self.updateGraph()
		
	def setTexts(self, text):
		for i in self.textItems:
			i.scene().removeItem(i)
		self.textItems = []
		for t in text:
			item = pg.TextItem(t)
			self.textItems.append(item)
			item.setParentItem(self)
		
	def updateGraph(self):

		pg.GraphItem.setData(self, **self.data)
		for i,item in enumerate(self.textItems):
			item.setPos(*self.data['pos'][i])
		

	

	def mouseDragEvent(self, ev):
		if ev.button() != QtCore.Qt.LeftButton:
			ev.ignore()
			return
		
		if ev.isStart():
			# We are already one step into the drag.
			# Find the point(s) at the mouse cursor when the button was first 
			# pressed:
			pos = ev.buttonDownPos()
			pts = self.scatter.pointsAt(pos)
			if len(pts) == 0:
				ev.ignore()
				return
			self.dragPoint = pts[0]
			ind = pts[0].data()[0]
			self.dragOffset = self.data['pos'][ind] - pos
		elif ev.isFinish():
			self.dragPoint = None
			return
		else:
			if self.dragPoint is None:
				ev.ignore()
				return
		
		self.dat = self.scatter.getData() 
		if len(self.dat) > 0 :
			a,b = self.dat
			self.slid.update_phas(a[0], b[0])
			self.legend(a,b)

		ind = self.dragPoint.data()[0]
		self.data['pos'][ind] = ev.pos() + self.dragOffset
		self.updateGraph()
		ev.accept()
		


	def legend(self, a, b, changed = False):
		if not changed:
			if a > glo_var.alpha_star and b > glo_var.beta_star:
				self.region_aft = 'MC'
				# penn = self.phas.purple
			elif a> glo_var.alpha_star:
				self.region_aft = 'HD  ' + '\u2161'
				# penn = self.phas.red
			elif b> glo_var.beta_star:
				self.region_aft = 'LD  ' + '\u2161'
				# penn = self.phas.blue
			elif b > self.phas.trans_func(a):
				self.region_aft = 'LD  ' + '\u2160'
				# penn = self.phas.blue
			else:
				# penn = self.phas.red
				self.region_aft = 'HD  ' + '\u2160'
		else:
			pass
		if self.region_bef != self.region_aft:
			self.region_bef=self.region_aft
			self.legend(a, b, changed = True)
		if changed:
			self.phas.pointer.setPen(None)	
			self.phas.leg.items = []
			self.phas.p5main.plot(pen=None, name=self.region_aft)

	def receive(self, slid, phase):
		self.slid = slid
		# don't need phase



# class MyROI(pg.ROI):
# 	def __init__(self, pos, size=[0.03,0.03], angle=0.0, invertible=False, maxBounds=None, snapSize=1.0, scaleSnap=False, translateSnap=False, rotateSnap=False, parent=None, pen=None, movable=True, removable=False):
# 		super().__init__(pos, size)

# 	def paint(self, p, opt, widget):
# 		# Note: don't use self.boundingRect here, because subclasses may need to redefine it.
# 		r = QtCore.QRectF(0, 0, self.state['size'][0], self.state['size'][1]).normalized()
# 		p.setRenderHint(QtGui.QPainter.Antialiasing)
# 		p.setPen(self.currentPen)
# 		p.translate(r.left(), r.top())
# 		p.scale(r.width(), r.height())
# 		p.drawEllipse(0, 0, 1, 1)

# 	def mouseDragEvent(self, ev):
# 		super().mouseDragEvent(ev)
# 		self.posi = self.pos()
# 		a = self.posi[0]
# 		b = self.posi[1]
# 		self.slid.update_phas(a, b)
# 		self.legend(a,b)
# 	def receive(self, slid, phas):
# 		self.slid = slid
# 		self.phas = phas

# 	def legend(self, a, b):

# 		if a > glo_var.alpha_star and b > glo_var.beta_star:
# 			region = 'MC'
# 			# penn = self.phas.purple
# 		elif a> glo_var.alpha_star:
# 			region = 'HD  ' + '\u2161'
# 			# penn = self.phas.red
# 		elif b> glo_var.beta_star:
# 			region = 'LD  ' + '\u2161'
# 			# penn = self.phas.blue
# 		elif b > self.phas.trans_func(a):
# 			region = 'LD  ' + '\u2160'
# 			# penn = self.phas.blue
# 		else:
# 			# penn = self.phas.red
# 			region = 'HD  ' + '\u2160'
# 		self.phas.pointer.setPen(None)
# 		self.phas.leg.items = []
# 		self.phas.p5main.plot(pen=None, name=region)
		
# class myscat(pg.ScatterPlotItem):

# 	def mouseClickEvent(self, ev):
# 		if ev.button() == QtCore.Qt.LeftButton:
# 			pts = self.pointsAt(ev.pos())
# 			if len(pts) > 0:
# 				self.ptsClicked = pts
# 				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
# 				self.sigClicked.emit(self, self.ptsClicked)
# 				ev.accept()
# 			elif self.lamb_po.curve.mouseShape().contains(ev.pos()):
# 				self.ptsClicked = pts
# 				self.toadd = [ev.pos()[0], ev.pos()[1]]
# 				glo_var.lambdas += [self.toadd]
# 				glo_var.lambdas.sort()
# 				glo_var.lambdas_degree += 1
# 				self.slid.update_lamb_rh_add()
# 				self.lamb_po.lastClicked.resetPen()
# 				self.lamb_po.lastClicked = []
# 				ev.accept()
# 			else:
# 				# print "no spots"
# 				self.lamb_po.lastClicked[0].resetPen()
# 				self.lamb_po.lastClicked = []

# 				ev.ignore()

# 		elif ev.button() == QtCore.Qt.RightButton:
# 			pts = self.pointsAt(ev.pos())
# 			if len(pts) > 0:
# 				self.ptsClicked = pts
# 				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
# 				self.raisecontextmenu(pts, ev)
# 				ev.accept()
# 			else:
# 				self.lamb_po.lastClicked[0].resetPen()
# 				self.lamb_po.lastClicked = []
# 				ev.ignore()
# 		else:
# 			ev.ignore()



# 	def mouseMoveEvent(self, ev):
# 		pts = self.pointsAt(ev.pos())
# 		if len(pts) > 0 :
# 			self.ptsClicked = pts
# 			self.sigClicked.emit(self, self.ptsClicked)
# 			ev.accept()


class myscat(pg.ScatterPlotItem):

	def __init__(self, *args, **kargs):
		pg.ScatterPlotItem.__init__(self, *args, **kargs)
		self.dragPoint = None
		self.dragOffset = None

	# def mouseClickEvent(self, ev):
	# 	if ev.button() == QtCore.Qt.LeftButton:
	# 		pts = self.pointsAt(ev.pos())
	# 		if len(pts) > 0:
	# 			self.ptsClicked = pts
	# 			self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
	# 			self.sigClicked.emit(self, self.ptsClicked)
	# 			ev.accept()
	# 		elif self.lamb_po.curve.mouseShape().contains(ev.pos()):
	# 			self.ptsClicked = pts
	# 			self.toadd = [ev.pos()[0], ev.pos()[1]]
	# 			glo_var.lambdas += [self.toadd]
	# 			glo_var.lambdas.sort()
	# 			glo_var.lambdas_degree += 1
	# 			self.slid.update_lamb_rh_add()
	# 			self.lamb_po.lastClicked.resetPen()
	# 			self.lamb_po.lastClicked = []
	# 			ev.accept()
	# 		else:
	# 			# print "no spots"
	# 			self.lamb_po.lastClicked[0].resetPen()
	# 			self.lamb_po.lastClicked = []

	# 			ev.ignore()

	# 	elif ev.button() == QtCore.Qt.RightButton:
	# 		pts = self.pointsAt(ev.pos())
	# 		if len(pts) > 0:
	# 			self.ptsClicked = pts
	# 			self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0], self.ptsClicked[0]._data[1]])
	# 			self.raisecontextmenu(pts, ev)
	# 			ev.accept()
	# 		else:
	# 			self.lamb_po.lastClicked[0].resetPen()
	# 			self.lamb_po.lastClicked = []
	# 			ev.ignore()
	# 	else:
	# 		ev.ignore()

	def mouseDragEvent(self, ev):
		if ev.button() != QtCore.Qt.LeftButton:
			ev.ignore()
			return
		
		if ev.isStart():
			# We are already one step into the drag.
			# Find the point(s) at the mouse cursor when the button was first 
			# pressed:
			pos = ev.buttonDownPos()
			pts = self.pointsAt(pos)
			if len(pts) == 0:
				ev.ignore()
				return
			self.dragPoint = pts[0]
			
			print(pts[0])
			print(self.getData())

			ind = pts[0].data()[0]
			print(pts[0].data())
			self.dragOffset = self.data['pos'][ind] - pos
		elif ev.isFinish():
			self.dragPoint = None
			return
		else:
			if self.dragPoint is None:
				ev.ignore()
				return
		
		ind = self.dragPoint.data()[0]
		self.data['pos'][ind] = ev.pos() + self.dragOffset
		self.updateGraph()
		ev.accept()

	def updateGraph(self):
		pg.GraphItem.setData(self, **self.data)
		for i,item in enumerate(self.textItems):
			item.setPos(*self.data['pos'][i])
		

	def receive(self, slid, phase):
		self.slid = slid
		self.phas = self


	# def mouseMoveEvent(self, ev):
	# 	pts = self.pointsAt(ev.pos())
	# 	if len(pts) > 0 :
	# 		self.ptsClicked = pts
	# 		self.sigClicked.emit(self, self.ptsClicked)
	# 		ev.accept()



class phase:
	def __init__(self, dphase):
		self.purple = pg.mkPen(QtGui.QColor(20,20,140,255))
		self.red = pg.mkPen(QtGui.QColor(180,0,0,255))
		self.blue = pg.mkPen(QtGui.QColor(20,20,140,255))
		self.roicolor = QtGui.QPen()
		self.roicolor.setBrush(QtGui.QColor(20,20,140,255))


		# self.roicolor = QtGui.QPen.brush(QtGui.QColor(20,20,140,255))
		self.dphase = dphase
		self.p5main = glo_var.MyPW(x="\u03b1",y1="\u03b2",set_range = self.set_range)
		# self.p5main._rescale=self.set_range
		self.p5=self.p5main.plotItem
		# self.p5main=pg.PlotWidget()

		# self.point = myscat([glo_var.alpha_star], [glo_var.beta_star])
		# self.p5main.plot([glo_var.alpha],[glo_var.beta],pen='r', symbol='o')

		self.viewbox = self.p5main.getPlotItem().getViewBox()
		self.viewbox.setBackgroundColor('w')
		# self.p5main.set_range = self.set_range
		self.p5main.coordinate_label = QtGui.QLabel()
		self.frame = glo_var.setframe(self.p5main, width = 1, coordinate_label = self.p5main.coordinate_label)

		self.dphase.addWidget(self.frame)
		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax=1, yMax=1)
		self.set_range()
		# self.viewbox.setRange(xRange=[0,2*max(glo_var.alpha,glo_var.alpha_star)],yRange=[0,2*max(glo_var.beta, glo_var.beta_star)],padding=0)





		self.p5main.plotItem.addLegend = glo_var.myaddLegend
		self.p5main.addLegend(self.p5main.plotItem, offset=(0,0.0000001))


		# self.p5main.plot(pen=None, name='LD  '+"\u2160")
		self.leg = self.p5main.plotItem.legend

		self.p5main.setLabel('bottom',"\u03b1",**glo_var.labelstyle)
		self.p5main.setLabel('left',"\u03b2",**glo_var.labelstyle)
		# self.scat = pg.ScatterPlotItem(size = 1, pen = pg.mkPen('r'), brush =pg.mkBrush(255,255,255,120))
		self.initiate()
	def set_range(self):
		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax=1, yMax=1)
		# self.viewbox.setRange(xRange=[0,2*max(glo_var.alpha,glo_var.alpha_star)],yRange=[0,2*max(glo_var.beta, glo_var.beta_star)],padding=0)
		self.viewbox.setRange(xRange=[0,2*glo_var.alpha_star],yRange=[0,2*glo_var.beta_star],padding=0.1)

	def initiate(self):
		# self.p5main.clear()

		self.value_declaration()
		self.pointer = Cursor_Point(self)

		self.pointer.legend(glo_var.alpha,glo_var.beta)
		# self.pointer = myscat([glo_var.alpha_star], [glo_var.beta_star])
		# self.curve=pg.PlotCurveItem(np.array(self.x), np.array(self.y))
		# self.curve.setPen(pg.mkPen('k'))
		# self.p1.addItem(self.curve)
		# self.sp.setData(self.x,self.y)
		# self.sp.sigClicked.connect(self.clicked)
		# self.p1.addItem(self.sp)

		self.ablim = 0.5/(1+sqrt(glo_var.l))

		# self.bounds1 = pg.PlotCurveItem(np.array([glo_var.alpha_star,1]),np.array([1,glo_var.beta_star]))
		# self.bounds1.setPen(pg.mkPen('k'))
		self.bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		self.bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		self.bounds3 = np.array([[0,0],[glo_var.alpha_star,glo_var.beta_star]])
		self.p5main.plot(self.bounds1)
		self.p5main.plot(self.bounds2)
		self.p5main.plot(self.bounds3)



		# self.pointer = myscat(np.array([glo_var.alpha]),np.array([glo_var.beta]))

		# self.viewbox.addItem(self.pointer)
		# self.ini_pos= np.array([[glo_var.alpha,glo_var.beta]], dtype=float)		
		# self.pointer.setData(pos = self.ini_pos, size = 1,symbol = ['o'], pxMode=False, text = ["MC"])
	# def initiate(self):
	# 	self.p5main.clear()

	# 	# self.pointer = myscat([glo_var.alpha_star], [glo_var.beta_star])

	# 	# self.curve=pg.PlotCurveItem(np.array(self.x), np.array(self.y))
	# 	# self.curve.setPen(pg.mkPen('k'))
	# 	# self.p1.addItem(self.curve)
	# 	# self.sp.setData(self.x,self.y)
	# 	# self.sp.sigClicked.connect(self.clicked)
	# 	# self.p1.addItem(self.sp)

	# 	self.ablim = 0.5/(1+sqrt(glo_var.l))
	# 	self.pointer = MyROI([glo_var.alpha_star, glo_var.beta_star], size = [glo_var.alpha_star/10,glo_var.beta_star/10])
	# 	self.pointer.setPen(self.roicolor)
	# 	# self.bounds1 = pg.PlotCurveItem(np.array([glo_var.alpha_star,1]),np.array([1,glo_var.beta_star]))
	# 	# self.bounds1.setPen(pg.mkPen('k'))
	# 	self.bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
	# 	self.bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
	# 	self.bounds3 = np.array([[0,0],[glo_var.alpha_star,glo_var.beta_star]])
	# 	self.p5main.plot(self.bounds1)
	# 	self.p5main.plot(self.bounds2)
	# 	self.p5main.plot(self.bounds3)

# cross hair
	# 	self.vLine = pg.InfiniteLine(angle=90, movable=False)
	# 	self.hLine = pg.InfiniteLine(angle=0, movable=False)
	# 	self.proxy = pg.SignalProxy(self.p5main.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)


	# def mouseMoved(self,evt):
	# 	print(evt)
	# 	print(evt[0])
	# 	pos = evt[0]  # using signal proxy turns original arguments into a tuple
	# 	self.pos_label = pg.LabelItem(justify='right')
	# 	self.p5main.addItem(self.pos_label)
	# 	if self.p5.sceneBoundingRect().contains(pos):
	# 		mousePoint = self.p5.vb.mapSceneToView(pos)
	# 		index = int(mousePoint.x())
	# 		if index >= 0 and index <= 1:
	# 			self.pos_label.setText("<span style='font-size: 12pt'>x=%0.2f,   <span style='font-size: 12pt'>y=%0.2f</span>" % (mousePoint.x(), mousePoint.y()))
			

	# 		self.vLine.setPos(mousePoint.x())
	# 		self.hLine.setPos(mousePoint.y())



		# self.p5main.plot([glo_var.alpha],[glo_var.beta],pen='r', symbol='o')
		# self.p5main.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	def update(self):
		self.p5main.clear()

		self.p5main.addItem(self.pointer)
		self.pointer.setData(pos = np.array([[glo_var.alpha,glo_var.beta]],dtype=float))
		self.pointer.legend(glo_var.alpha,glo_var.beta)


		# r = pg.PolyLineROI([(glo_var.alpha_star, glo_var.beta_star)])
		


		
		# self.pointer.setPos(np.array([glo_var.alpha]),np.array([glo_var.beta]))



		# self.ablim = 0.5/(1+sqrt(glo_var.l))
		# self.viewbox.setRange(xRange=[0,self.ablim],yRange=[0,self.ablim],padding=0)	

		self.value_declaration()


		if glo_var.alpha > 2*glo_var.alpha_star:
			glo_var.alpha = 2*glo_var.alpha_star
		if glo_var.beta > 2*glo_var.beta_star:
			glo_var.beta = 2*glo_var.beta_star

		HD = pg.TextItem(html='HD', anchor=(glo_var.alpha_star,0.5*glo_var.beta_star), border='w', fill=(255, 0, 0, 250))
		# self.p5main.addItem(HD)
		HD.setPos(glo_var.alpha_star,0.5*glo_var.beta_star)
		LD = pg.TextItem(html='LD', anchor=(glo_var.alpha_star*0.3,glo_var.beta_star*1.3), border='w', fill=(0, 255, 0, 200))
		# self.p5main.addItem(LD)
		LD.setPos(glo_var.alpha_star*0.3,glo_var.beta_star*1.3)
		MC = pg.TextItem(html='MC', anchor=(glo_var.alpha_star*1.2,glo_var.beta_star*1.3), border='w', fill=(0, 0, 255, 200))
		MC.setPos(glo_var.alpha_star*1.2,glo_var.beta_star*1.3)
		# self.p5main.addItem(MC)
		
		# self.bounds1.setData(np.array([glo_var.alpha_star,glo_var.beta_star]),np.array([1,glo_var.beta_star]))


		# self.pointer = self.MyROI([self.ablim/2, self.ablim/2], size = [glo_var.alpha_star/10,glo_var.beta_star/10])


		# self.pointer = myscat([glo_var.alpha],[glo_var.beta], size = 10)

		self.bounds1 = np.array([[glo_var.alpha_star,glo_var.beta_star],[1,glo_var.beta_star]])
		self.bounds2 = np.array([[glo_var.alpha_star,glo_var.beta_star],[glo_var.alpha_star,1]])
		linspace=np.linspace(0,glo_var.alpha_star,20)
		trans_line_val=[]
		for i in linspace:
			trans_line_val += [self.trans_func(i)]
		self.p5main.plot(self.bounds1, pen = 'k')
		self.p5main.plot(self.bounds2, pen = 'k')
		self.p5main.plot(linspace,trans_line_val, pen = 'k')


		self.set_range()

		# self.pointer = Cursor_Point()
		# self.viewbox.addItem(self.pointer)
		# self.ini_pos= np.array([[0.01,0.01]], dtype=float)		
		# self.pointer.setData(pos = self.ini_pos, pxMode=False, text = ["MC"])
		
		# self.point = np.array([glo_var.alpha,glo_var.beta])
		# self.spots = [{'pos': self.point, 'size':1e-6, 'pen':{'color':'w','width':2}}]
		# self.scat.addPoints(self.spots)	
		# self.p5main.addItem(self.scat)
		# self.p5main.plot([glo_var.alpha],[glo_var.beta],pen=None, symbol='o')

	# def receive(self,slid):
	# 	self.slid = slid


	def value_declaration(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas))
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[ - 1][1]

	def trans_func(self, point):
		self.B = point*(self.lambda_0 - point)/(self.lambda_0 + (glo_var.l -1) * point)
		self.trans_b = - self.lambda_1 +(glo_var.l-1)*self.B
		self.trans_intercal = 0 if pow(self.trans_b,2) - 4*self.B*self.lambda_1 < 0.0000001 else sqrt(pow(self.trans_b,2) - 4*self.B*self.lambda_1)
		self.trans = (-self.trans_b - self.trans_intercal)/2
		return self.trans

	def receive(self, slid):
		self.slid = slid
		self.pointer.receive(slid, self)