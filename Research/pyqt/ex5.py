from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
mainwindow = QtGui.QMainWindow()
mainwindow.setWindowTitle('pyqtgraph example: PlotWidget')
mainwindow.resize(1000,800)
cw = QtGui.QWidget()
mainwindow.setCentralWidget(cw)

gridlayout = QtGui.QGridLayout()
cw.setLayout(gridlayout)

# define plot windows
signalgraph = pg.PlotWidget(name='Signalgraph')

# set position and size of plot windows
gridlayout.addWidget(signalgraph,0,0)

mainwindow.show()


# sample data
x = [0,1,2,3,4,5,6,7,8,9,10]
y = [0,0,0,8,8,8,9,9,9,0,0]

# plot 1
curve = pg.PlotCurveItem(x,y[:-1],pen='w',stepMode=True)
signalgraph.addItem(curve)

#cross hair in signalgraph
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
signalgraph.addItem(vLine, ignoreBounds=True)
signalgraph.addItem(hLine, ignoreBounds=True)

# Here I am not sure what to do ...
vb = signalgraph.plotItem.vb
##vb = pg.ViewBox()


def mouseMoved(evt):
    pos = evt[0]


if __name__ == "__main__":
    # app = QtGui.QApplication([])
    # w = Widget()
    # w.show()
    # w.raise_()
    app.exec_()	