import numpy as np
import math
from math import sqrt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# To change legend
# -------------------------------------------
class mylegend(pg.LegendItem):
	def addItem(self, item, name):
		label = pg.LabelItem(name)
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
	pass
	# doubleClicked = pyqtSignal()
	#
	#
	# def mousePressEvent(self, event):
		# self.__mousePressPos = None
		# self.__mouseMovePos = None
		# if event.button() == QtCore.Qt.LeftButton:
		# 	self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
		# 	self.__mousePressPos = event.globalPos()
		# 	self.__mouseMovePos = event.globalPos()
	#
		# # super(MyPW, self).mousePressEvent(event)
	#
	# def mouseMoveEvent(self, event):
		# if event.buttons() == QtCore.Qt.LeftButton:
		# 	# adjust offset from clicked point to origin of widget
	#
		# 	self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
		# 	currPos = self.mapToGlobal(self.pos())
		# 	globalPos = event.globalPos()
		# 	diff = globalPos - self.__mouseMovePos
		# 	newPos = self.mapFromGlobal(currPos + diff)
		# 	self.move(newPos)
	#
		# 	self.__mouseMovePos = globalPos
	#
		# # super(MyPW, self).mouseMoveEvent(event)
	#
	# def mouseReleaseEvent(self, event):
		# if self.__mousePressPos is not None:
		# 	moved = event.globalPos() - self.__mousePressPos
		# 	if moved.manhattanLength() > 3:
		# 		event.ignore()
		# 		return
	#
		# # super(MyPW, self).mouseReleaseEvent(event)

# ---------------------------------------
# class QDoublePushButton(QPushButton):
#     doubleClicked = pyqtSignal()
#     clicked = pyqtSignal()

#     def __init__(self, *args, **kwargs):
#         QPushButton.__init__(self, *args, **kwargs)
#         self.timer = QTimer()
#         self.timer.setSingleShot(True)
#         self.timer.timeout.connect(self.clicked.emit)
#         super().clicked.connect(self.checkDoubleClick)

#     @pyqtSlot()
#     def checkDoubleClick(self):
#         if self.timer.isActive():
#             self.doubleClicked.emit()
#             self.timer.stop()
#         else:
#             self.timer.start(250)


	# def mouseDragEvent(self, ev):
	#     if ev.isStart():
	#         #p = ev.pos()
	#         #if not self.isMoving and not self.shape().contains(p):
	#             #ev.ignore()
	#             #return        
	#         if ev.button() == QtCore.Qt.LeftButton:
	#             self.setSelected(True)
	#             if self.translatable:
	#                 self.isMoving = True
	#                 self.preMoveState = self.getState()
	#                 self.cursorOffset = self.pos() - self.mapToParent(ev.buttonDownPos())
	#                 self.sigRegionChangeStarted.emit(self)
	#                 ev.accept()
	#             else:
	#                 ev.ignore()

	#     elif ev.isFinish():
	#         if self.translatable:
	#             if self.isMoving:
	#                 self.stateChangeFinished()
	#             self.isMoving = False
	#         return

	#     if self.translatable and self.isMoving and ev.buttons() == QtCore.Qt.LeftButton:
	#         snap = True if (ev.modifiers() & QtCore.Qt.ControlModifier) else None
	#         newPos = self.mapToParent(ev.pos()) + self.cursorOffset
	#         self.translate(newPos - self.pos(), snap=snap, finish=False)

def setframe(p, width = 4):
	layout=QtGui.QHBoxLayout()
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