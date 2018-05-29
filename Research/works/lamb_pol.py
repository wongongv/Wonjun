
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from pyqtgraph import widgets


class myscat(pg.ScatterPlotItem):
	def receive(self, slid, lamb_po):
		self.slid = slid
		self.lamb_po = lamb_po
	def mouseClickEvent(self, ev):
		if ev.button() == QtCore.Qt.LeftButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0],self.ptsClicked[0]._data[1]])
				self.sigClicked.emit(self, self.ptsClicked)
				ev.accept()
			elif self.lamb_po.curve.mouseShape().contains(ev.pos()):
				self.ptsClicked = pts
				self.toadd = [ev.pos()[0],ev.pos()[1]]
				glo_var.lambdas += [self.toadd]
				glo_var.lambdas.sort()
				glo_var.lambdas_degree += 1
				self.slid.update_lamb_rh_add()
				self.lamb_po.lastClicked.resetPen()
				self.lamb_po.lastClicked=[]
				ev.accept()
			else:
				#print "no spots"
				self.lamb_po.lastClicked[0].resetPen()
				self.lamb_po.lastClicked=[]

				ev.ignore()
		
		elif ev.button() == QtCore.Qt.RightButton:
			pts = self.pointsAt(ev.pos())
			if len(pts) > 0:
				self.ptsClicked = pts
				self.index = glo_var.lambdas.index([self.ptsClicked[0]._data[0],self.ptsClicked[0]._data[1]])
				self.raisecontextmenu(pts, ev)
				ev.accept()
			else:
				self.lamb_po.lastClicked[0].resetPen()
				self.lamb_po.lastClicked=[]
				ev.ignore()
		else:
			ev.ignore()
	 
	def wheelEvent(self, ev, axis=None):
		if len(self.lamb_po.lastClicked) ==1:
			s = self.ptsClicked[0]._data[1]+ ev.delta() / 2000 # actual scaling factor
			# should say that I limited this number by 0.0001 to prevent zero division
			if s < 0.0001 :
				s = 0.0001
			self.set_yval(s)
			ev.accept()
	 
	def set_yval(self, value):
		self.ptsClicked[0]._data[1] = value
		self.slid.update_lamb_rh(self.index, value, 0)


	def remove_point(self):
		glo_var.lambdas.remove([self.ptsClicked[0]._data[0],self.ptsClicked[0]._data[1]])
		glo_var.lambdas_degree -= 1
		self.slid.update_lamb_rh(0,0,1)

	def raisecontextmenu(self, point, ev):
		self.menu = Menu(self, point)
		self.menu.popup(ev.screenPos().toQPoint())

class Menu(QtGui.QMenu):
	def __init__(self, item, point):
		QtGui.QMenu.__init__(self)
		self.point = point
		self.item = item
		self.removal = self.addAction("Remove point", lambda :self.item.remove_point())
		self.positionMenu = self.addMenu("Change \u03bb")
		self.w=QtGui.QWidget()
		self.l=QtGui.QGridLayout()

		self.w.setLayout(self.l)

		self.fracPosSpin = widgets.SpinBox.SpinBox()
		self.fracPosSpin.setOpts(value=point[0]._data[1], bounds=(0.0, None), step=0.01, decimals=2)
		self.l.addWidget(QtGui.QLabel("\u03bb(x) : "), 0,0)
		self.l.addWidget(self.fracPosSpin, 0, 1)
		self.a = QtGui.QWidgetAction(self)		
		self.a.setDefaultWidget(self.w)
		self.positionMenu.addAction(self.a)
		
		self.fracPosSpin.sigValueChanging.connect(self.fractionalValueChanged)
		
		
	def fractionalValueChanged(self, x):
		val = self.fracPosSpin.value()
		if val > self.item.lamb_po.lambda_max:
			self.item.lamb_po.lambda_max = val
			self.item.lamb_po.set_range()
		else:
			self.item.lamb_po.lambda_max=max(self.item.lamb_po.lambdas_ys)
			self.item.lamb_po.set_range()


		self.item.set_yval(val)

class lamb_pol:
	def __init__(self,dlamb) :
		self.dlamb = dlamb

		self.p1main = glo_var.MyPW()
		self.p1main._rescale = self.set_range
		self.p1=self.p1main.plotItem
		# self.viewbox = self.p1main.getPlotItem().getViewBox()
		# self.viewbox.setBackgroundColor('w')
		# self.item = self.p1main.getPlotItem()

		# self.win = win
		# self.p1main = pg.PlotWidget(title = '\u03bb')

		self.p1main.setLabel('bottom',"x",**glo_var.labelstyle)
		self.p1main.setLabel('left',"\u03bb",**glo_var.labelstyle)

# I didnt use it. Think about it.
		self.font = QtGui.QFont()
		self.font.setBold(True)



		self.viewbox=self.p1main.getViewBox()
		self.viewbox.setBackgroundColor('w')

		self.viewbox.setLimits(xMin = -0.02, yMin = -0.02, xMax = 1.02)



		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas))
		self.lambda_min=min(self.lambdas_ys)
		self.lambda_max=max(self.lambdas_ys)

		self.set_range()
		self.sp = myscat(size = 7, pen = pg.mkPen(None), brush=pg.mkBrush(100,200,200), symbolPen='w')
		self.lastClicked=[]
		# self.x, self.y = zip(*sorted(glo_var.lambdas.values()))
		# self.lambs = np.array([self.x,self.y])
		# self.spots = [{'pos':self.lambs[:,i], 'data': 1} for i in range(glo_var.lambdas_degree)]
		# self.sp.addPoints(self.spots)
		# self.p1main.addItem(self.sp)
		# self.viewbox.menu = None


		self.frame = glo_var.setframe(self.p1main, width = 1)
		self.dlamb.addWidget(self.frame)
		
		self.update()

	def set_range(self):
		self.viewbox.setRange(xRange=[-0.02,1.2*self.lambda_max],yRange=[-0.02,1.2*self.lambda_max],padding =0)
	def update(self):
		self.p1main.clear()


		self.x, self.y = zip(*sorted(glo_var.lambdas))
		# self.lambs = np.array([self.x,self.y])
		# self.spots = [{'pos':self.lambs[:,i], 'data': 1} for i in range(glo_var.lambdas_degree)]
		# self.sp.addPoints(self.spots)
		self.curve=pg.PlotCurveItem(np.array(self.x), np.array(self.y))
		self.curve.setPen(pg.mkPen('k',width = glo_var.line_width))
		self.p1main.addItem(self.curve)
		self.sp.setData(self.x,self.y)
		self.sp.sigClicked.connect(self.clicked)
		self.p1main.addItem(self.sp)


	def clicked(self, item, points):
		self.points=points
		for p in self.lastClicked:
			points[0].resetPen()
		points[0].setPen('b', width=2)
		self.lastClicked = points


	def receive(self, slid):
		self.sp.receive(slid, self)



		# glo_var.lambda_function = self.f
		# self.ax.clear()
		# self.ax.set_ylim(0,1)
		# self.ax.set_xlim(0,1)
		# self.pol_points=glo_var.lambdas
		# self.pol_x, self.pol_y = zip(*sorted(self.pol_points.values()))
		# self.pol_z = interp1maind(self.pol_x, self.pol_y)
		# # self.pol_z=CubicSpline(self.pol_x, self.pol_y) # Use the interactive widget! that receives input.
		# # self.pol_f=np.poly1d(self.pol_z)
		# self.x = np.linspace(0,1,glo_var.lambdas_degree * 10)							 # maybe need to change 50 according to the # of knobs
		# # self.y = self.pol_f(self.x)
		# self.initial_pol = self.ax.plot(self.pol_x, self.pol_y, 'o', self.x, self.pol_z(self.x))
	# def clear(self):
		# self.ax.remove()
	# def new_update(self):
	# 	self.p1main.setData