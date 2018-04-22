import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from math import sqrt
from matplotlib.widgets import AxesWidget
import six
import pdb
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

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

l = 1
lambdas=[]
lambdas_degree=0
alpha = 0.1
beta = 0.1
