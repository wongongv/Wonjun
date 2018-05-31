import numpy as np
import math
from math import sqrt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import pixmaps
from pyqtgraph.graphicsItems import ButtonItem

class mylegend(pg.LegendItem):
	def addItem(self, item, name):
		legendLabelStyle = {'size': '14pt', 'bold': True}
		
		label = pg.LabelItem(name)
		
		label.setText(name,**legendLabelStyle)
		if isinstance(item, MyItem):
			sample = item
		else:
			sample = MyItem(item)        
		row = self.layout.rowCount()
		self.items.append((sample, label))
		self.layout.addItem(sample, row, 0)
		self.layout.addItem(label, row, 1)
		self.updateSize()

class MyItem(pg.GraphicsWidget):
	def __init__(self, item):
		pg.GraphicsWidget.__init__(self)
		self.item = item
	
	def paint(self, p, *args):
		#p.setRenderHint(p.Antialiasing)  # only if the data is antialiased.
		opts = self.item.opts
		
		if opts.get('fillLevel',None) is not None and opts.get('fillBrush',None) is not None:
			p.setBrush(pg.mkBrush(opts['fillBrush']))
			p.setPen(pg.mkPen(None))
			p.drawPolygon(QtGui.QPolygonF([QtCore.QPointF(2,18), QtCore.QPointF(18,2), QtCore.QPointF(18,18)]))
		
		if not isinstance(self.item, pg.ScatterPlotItem):
			p.setPen(pg.mkPen(opts['pen']))
			p.drawLine(2, 2, 18, 2)
		
		symbol = opts.get('symbol', None)
		if symbol is not None:
			if isinstance(self.item, pg.PlotDataItem):
				opts = self.item.scatter.opts
				
			pen = pg.mkPen(opts['pen'])
			brush = pg.mkBrush(opts['brush'])
			size = opts['size']

			p.translate(10,10)
			path = drawSymbol(p, symbol, size, pen, brush)

# To set addlegend method of plotitem to below.
def myaddLegend(self, size=None, offset=(30, 30)):
	if self.legend is None:
		self.legend = mylegend(size, offset)
		self.legend.setParentItem(self.vb)
	return self.legend
# --------------------------------------------------------------

class MyPW(pg.PlotWidget):
	def __init__(self, x = None, y1 = None, y2 = None, set_range = None):
		super(MyPW,self).__init__()
		self.plotItem.autoBtn = ButtonItem.ButtonItem(pixmaps.getPixmap('default'), 14, self.plotItem)
		self._rescale = lambda:None
		# self.plotItem.autoBtn.clicked.connect(self._rescale)
		self.plotItem.vb.menu.clear()
		
		self.vmenu = QtGui.QMenu()
		defaultview = QtGui.QAction("Default View",self.vmenu)
		defaultview.triggered.connect(set_range)
		self.vmenu.addAction(defaultview)
		
		self.plotItem.ctrlMenu = [defaultview]
		
# mouse tracking label
		self.x = x
		self.y1 = y1
		self.y2 = y2
# delete default view, get rid of Export
		self.plotItem.hideButtons()
		self.plotItem.scene().contextMenu = None  # get rid of 'Export'
		self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

	def mouseMoved(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		# if self.p1.sceneBoundingRect().contains(pos):
		if self.plotItem.vb.sceneBoundingRect().contains(pos):
			if not self.y2:
				mousePoint = self.plotItem.vb.mapSceneToView(pos)
				syntax = "<span style='font-size: 12pt'>"+self.x+" = %0.4f,   <span>"+self.y1+" = %0.4f</span>"
				self.coordinate_label.setText(syntax % (mousePoint.x(),  mousePoint.y()))
			else:
				mousePoint = self.plotItem.vb.mapSceneToView(pos)
				mousePoint2 = self.tempplotitem.vb.mapSceneToView(pos)
				syntax = "<span style='font-size: 12pt'>"+self.x+" = %0.4f,   <span>"+self.y1+" = %0.4f</span>, <span>"+self.y2+" = %0.4f</span>"
				self.coordinate_label.setText(syntax % (mousePoint.x(),  mousePoint.y(), mousePoint2.y()))
		else:
			self.coordinate_label.setText("")

def setframe(p, width = 4, coordinate_label=None):
	layout=QtGui.QVBoxLayout()
	if coordinate_label:
		coord_layout = QtGui.QHBoxLayout()
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		coord_layout.addWidget(spacer)
		coord_layout.addWidget(coordinate_label)
		layout.addLayout(coord_layout)
	layout.addWidget(p)
	frame = QtGui.QFrame()
	frame.setLayout(layout)
	frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
	frame.setLineWidth(width)
	return frame

def initialize():
	global l, lambdas, lambdas_degree, alpha, beta
	l = 1
	lambdas=[]
	lambdas_degree=0
	alpha = 0.1
	beta = 0.1

l = 1
lambdas=[]
lambdas_degree=0
alpha = 0.1
beta = 0.1
labelstyle = {'font-size': '24px'}
line_width = 2
slid_precision = 1000000