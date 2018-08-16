import numpy as np
import math
from math import sqrt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import pixmaps
from pyqtgraph.graphicsItems import ButtonItem

import os.path

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

	def __init__(self, x = None, y1 = None, y2 = None, set_range = None, num = None, set_range_byspbox = None):
		super(MyPW,self).__init__()
		self.plotItem.autoBtn = ButtonItem.ButtonItem(pixmaps.getPixmap('default'), 14, self.plotItem)
		self._rescale = lambda:None
		# self.plotItem.autoBtn.clicked.connect(self._rescale)
		self.plotItem.vb.menu.clear()
# to use clear_points in main.py
		self.num = num
		self.vmenu = QtGui.QMenu()
		defaultview = QtGui.QAction("Default View",self.vmenu)
		defaultview.triggered.connect(set_range)
		self.vmenu.addAction(defaultview)
		
		self.set_range_byspbox = set_range_byspbox
		view_range = QtGui.QAction("View Range",self.vmenu)
		view_range.triggered.connect(self.view_range)
		self.vmenu.addAction(view_range)



		self.rwindow = QtGui.QMainWindow()
		self.rwindow.setWindowIcon(QtGui.QIcon(logo))
		self.rwindow.setWindowTitle("View Range")
		boxeswidget=QtGui.QWidget(self.rwindow)
		spinbox_layout = QtGui.QGridLayout(boxeswidget)

		# change the name based on nums
		self.xrange = QtGui.QDoubleSpinBox()
		self.yrange = QtGui.QDoubleSpinBox()

		self.xrange_end = QtGui.QDoubleSpinBox()
		self.yrange_end = QtGui.QDoubleSpinBox()
		self.xrange.setDecimals(4)
		self.xrange_end.setDecimals(4)
		self.yrange.setDecimals(4)
		self.yrange_end.setDecimals(4)

		self.font = QtGui.QFont("",13)

		self.label_x = QtGui.QLabel()
		self.label_x.setAlignment(QtCore.Qt.AlignCenter)
		self.label_x.setFont(self.font)
		
		self.label_y = QtGui.QLabel()
		self.label_y.setAlignment(QtCore.Qt.AlignCenter)
		self.label_y.setFont(self.font)

		self.xrange.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
		self.xrange_end.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
		self.yrange.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
		self.yrange_end.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
		

		self.xrange.valueChanged.connect(self.range_handler_x)
		self.xrange_end.valueChanged.connect(self.range_handler_x_end)
		self.yrange.valueChanged.connect(self.range_handler_y)
		self.yrange_end.valueChanged.connect(self.range_handler_y_end)
		self.label_x.setText(x)
		self.label_y.setText(y1)
		if y2:
			self.y2range = QtGui.QDoubleSpinBox()
			self.y2range_end = QtGui.QDoubleSpinBox()
			self.label_y2 = QtGui.QLabel()
			self.label_y2.setAlignment(QtCore.Qt.AlignCenter)
			self.label_y2.setFont(self.font)
			self.label_y2.setText(y2)
			self.y2range.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
			self.y2range_end.setButtonSymbols(QtGui.QDoubleSpinBox.NoButtons)
			self.y2range.valueChanged.connect(self.range_handler_y2)
			self.y2range_end.valueChanged.connect(self.range_handler_y2_end)
			self.y2range.setDecimals(4)
			self.y2range_end.setDecimals(4)

			spinbox_layout.addWidget(self.label_x,0,0,1,1)
			spinbox_layout.addWidget(self.label_y,1,0,1,1)
			spinbox_layout.addWidget(self.label_y2,2,0,1,1)
			spinbox_layout.addWidget(self.xrange,0,1,1,1)
			spinbox_layout.addWidget(self.yrange,1,1,1,1)
			spinbox_layout.addWidget(self.y2range,2,1,1,1)
			spinbox_layout.addWidget(self.xrange_end,0,2,1,1)
			spinbox_layout.addWidget(self.yrange_end,1,2,1,1)
			spinbox_layout.addWidget(self.y2range_end,2,2,1,1)

		else:
			spinbox_layout.addWidget(self.label_x,0,0,1,1)
			spinbox_layout.addWidget(self.label_y,1,0,1,1)
			spinbox_layout.addWidget(self.xrange,0,1,1,1)
			spinbox_layout.addWidget(self.yrange,1,1,1,1)
			spinbox_layout.addWidget(self.xrange_end,0,2,1,1)
			spinbox_layout.addWidget(self.yrange_end,1,2,1,1)


		self.rwindow.setCentralWidget(boxeswidget)


		self.plotItem.ctrlMenu = [defaultview, view_range]
		self.main = main
# mouse tracking label
		self.x = x
		self.y1 = y1
		self.y2 = y2
# delete default view, get rid of Export
		self.plotItem.hideButtons()
		self.plotItem.scene().contextMenu = None  # get rid of 'Export'
		# print(dir(self.plotItem))
		# print(dir(self.plotItem.scene()))
		# print(dir(self.plotItem.scene()))
		self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
		# self.proxy2 = pg.SignalProxy(self.plotItem.scene().sigMouseHover, rateLimit=60, slot=self.mouseHover)

	def set_spbox_value(self):
		self.xrange.setValue(self.ranges[0][0])
		self.xrange_end.setValue(self.ranges[0][1])
		self.yrange.setValue(self.ranges[1][0])
		self.yrange_end.setValue(self.ranges[1][1])
		if len(self.ranges) == 3:
			self.y2range.setValue(self.ranges[2][0])
			self.y2range_end.setValue(self.ranges[2][1])

	def range_handler_x(self, value):
		print(self.ranges)
		print(type(self.ranges))
		print(self.ranges[0])
		print(type(self.ranges[0]))
		print(self.ranges[0][0])
		print(type(self.ranges[0][0]))
		self.ranges[0][0] = value
		self.set_range_byspbox()

	def range_handler_x_end(self, value):
		self.ranges[0][1] = value
		self.set_range_byspbox()

	def range_handler_y(self, value):
		self.ranges[1][0] = value
		self.set_range_byspbox()

	def range_handler_y_end(self, value):
		self.ranges[1][1] = value
		self.set_range_byspbox()

	def range_handler_y2(self, value):
		self.ranges[2][0] = value
		self.set_range_byspbox()

	def range_handler_y2_end(self, value):
		self.ranges[2][0] = value
		self.set_range_byspbox()


	def receive_range(self,rang):
		print(rang,"rang")
		print(type(rang),"rangtype")
		self.ranges = rang
		self.set_spbox_value()

	def mouseMoved(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		# if self.p1.sceneBoundingRect().contains(pos):
		

		if self.plotItem.vb.sceneBoundingRect().contains(pos):
			if not self.y2:
				mousePoint = self.plotItem.vb.mapSceneToView(pos)
				syntax = "<span style='font-size: 12pt'>"+self.x+" = %0.4f,   <span>"+self.y1+" = %0.4f</span>"
				self.coordinate_label.setText(syntax % (mousePoint.x(),  mousePoint.y()))
				self.main.clear_points(self.num)
			else:
				mousePoint = self.plotItem.vb.mapSceneToView(pos)
				mousePoint2 = self.tempplotitem.vb.mapSceneToView(pos)
				syntax = "<span style='font-size: 12pt'>"+self.x+" = %0.4f,   <span>"+self.y1+" = %0.4f</span>, <span>"+self.y2+" = %0.4f</span>"
				self.coordinate_label.setText(syntax % (mousePoint.x(),  mousePoint.y(), mousePoint2.y()))
				self.main.clear_points(self.num)
		else:
			self.coordinate_label.setText("")

	def view_range(self):
		self.rwindow.show()

	# def mouseHover(self,evt):
	# 	if not isinstance(evt[0],list):
	# 		print('h')
	# 		self.coordinate_label.setText("")

def setframe(p, width = 4, coordinate_label=None):
	layout=QtGui.QVBoxLayout()
	if coordinate_label:
		coord_layout = QtGui.QHBoxLayout()
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		spacer.setFixedHeight(20)
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

def pass_main(mai):
	global main
	main = mai

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)
logo = resource_path("logo.png")

l = 1
lambdas=[]
lambdas_degree=0
alpha = 0.1
beta = 0.1
labelstyle = {'font-size': '24px'}
line_width = 2
slid_precision = 1000000
main = 0
