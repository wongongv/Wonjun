'''
Simple Cosine Wave UI using PyQt4 and pyqtgraph
Copyright 2015 Anthony Torlucci
Distributed under the terms of the GNU General Public License (see gpl.txt for more information)
    This file is part of Simple Cosine Wave UI.
    Simple Cosine Wave UI is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Simple Cosine Wave UI is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Simple Cosine Wave UI.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = 'Anthony Torlucci'
__version__ = '0.0.1'

# import python standard modules

# import 3rd party libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np
import sys
# import local python

class Window(QMainWindow):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Simple Cosine Wave')
        self.window = pg.GraphicsWindow()
        self.setCentralWidget(self.window)
        self.window.setBackground('w')
        self.p1 = self.window.addPlot(labels={'left' : 'amplitude'}, title='Phase and Frequency')
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True, alpha=0.5)
        self.p1.setYRange(-1, 1)
        #
        self.phi = 0.0 # initialize the phase value
        self.freq = 0.0 # initialize frequency
        #
        self.phiLabel = QLabel('Phase (degrees): 0.0')
        self.phaseSlider = QSlider(Qt.Horizontal)
        self.freqLabel = QLabel('Frequency (Hz): 0.0')
        self.freqSlider = QSlider(Qt.Horizontal)
        self.resetButton = QPushButton('RESET')
        self.fillCheckBox = QCheckBox('Add Fill')
        #
        self.label = QLabel()
        #
        self.createMenuBar()
        self.createDockWindows()
        self.showCurve()

    def createMenuBar(self):
        # file menu actions:
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(self.close)
        # create instance of menuBar
        menubar = self.menuBar()
        # add file menu and file menu actions
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def createDockWindows(self):
        controlPanelDockWidget = QDockWidget('controls', self)
        controlPanelDockWidget.setObjectName('ControlPanelDockWidget')
        controlPanelDockWidget.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        # create a widget to house checkbox and list widget with QVBoxLayout
        houseWidget = QWidget(self) # self?
        # add a slider for phase
        layout = QVBoxLayout()
        #self.phiLabel = QLabel('Phase: 0.0')
        layout.addWidget(self.phiLabel)
        #self.phaseSlider = QSlider(Qt.Horizontal)
        self.phaseSlider.setRange(-180, 180)
        self.phaseSlider.setValue(self.phi)
        #

        QObject.connect(self.phaseSlider, SIGNAL('valueChanged(int)'), self.changePhi)
        QObject.connect(self.phaseSlider, SIGNAL('valueChanged(int)'), self.showCurve)
        #
        layout.addWidget(self.phaseSlider)

        #self.freqLabel = QLabel('Frequency: 0.0')
        layout.addWidget(self.freqLabel)
        #self.freqSlider = QSlider(Qt.Horizontal)
        self.freqSlider.setRange(0, 100)
        self.freqSlider.setValue(self.freq)
        #
        QObject.connect(self.freqSlider, SIGNAL('valueChanged(int)'), self.changeFreq)
        QObject.connect(self.freqSlider, SIGNAL('valueChanged(int)'), self.showCurve)
        #
        layout.addWidget(self.freqSlider)

        #self.resetButton = QPushButton('RESET')

        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.resetValues)
        QObject.connect(self.resetButton, SIGNAL('clicked()'), self.showCurve)
        #
        layout.addWidget(self.resetButton)

        #self.fillCheckBox = QCheckBox('Add Fill')

        #QObject.connect(self.fillCheckBox, SIGNAL('stateChanged(int)'), self.fillCheckBoxChanged)
        QObject.connect(self.fillCheckBox, SIGNAL('stateChanged(int)'), self.showCurve)
        layout.addWidget(self.fillCheckBox)
        #

        layout.addWidget(self.label)
        #
        houseWidget.setLayout(layout)
        controlPanelDockWidget.setWidget(houseWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, controlPanelDockWidget)



    def changePhi(self, value):
        self.phi = value * np.pi / 180
        self.phiLabel.setText('Phase (degrees): ' + str(value))

    def changeFreq(self, value):
        self.freq = value
        self.freqLabel.setText('Frequency (Hz): ' + str(value))

    def resetValues(self):
        self.changePhi(0.0)
        self.changeFreq(0.0)
        self.phaseSlider.setValue(0.0)
        self.freqSlider.setValue(0.0)


    @pyqtSlot()
    def showCurve(self):
        # Clear plot
        self.p1.clear()
        t = np.linspace(0.0, 1.0, num=1000, endpoint=True)
        curve = np.cos(2*np.pi*self.freq*t+self.phi)
        c = pg.PlotCurveItem(pen='k')
        self.p1.addItem(c)
        c.setData(t, curve)
        if self.fillCheckBox.isChecked():
            c.setBrush('k')
            c.setFillLevel(0.0)

        # crosshairs
        vLine = pg.InfiniteLine(angle=90, movable=False, pen='b')
        hLine = pg.InfiniteLine(angle=0, movable=False, pen='b')
        self.p1.addItem(vLine, ignoreBounds=True)
        self.p1.addItem(hLine, ignoreBounds=True)
        self.p1vb = self.p1.vb

        def mouseMoved(mousePoint):
            #
            curvePoint = self.p1vb.mapSceneToView(mousePoint)
            if self.p1.sceneBoundingRect().contains(mousePoint):
                index = int((curvePoint.x() - t[0]) * 1000)
                #print "curvePointY is: ", curvePoint.y()
                #print "curve is:      ", curve[index]
                if index > 0 and index < len(curve):
                    self.label.setText("<span style='font-size: 12pt'>time=%0.5f,   \
                    <span style='color: blue'>curve=%0.5f</span>" % (t[index], curve[index]))
                vLine.setPos(curvePoint.x())
                hLine.setPos(curvePoint.y())
        self.p1.scene().sigMouseMoved.connect(mouseMoved)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = pg.QtGui.QApplication([])
        app.exec_()
# =============== END OF SCRIPT =================