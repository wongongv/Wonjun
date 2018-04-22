import os
import sys
import sip
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#----------------------------------------------------------------------
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

#----------------------------------------------------------------------
#----------------------------------------------------------------------


class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__(getMayaWindow())
        self.setGeometry(50,50,600,600)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QGridLayout()
        widget.setLayout(layout)

        mdiArea = QMdiArea()
        layout.addWidget(mdiArea)

        newItem1 = vrayRectWidget(mdiArea, 'aaaa')
        newItem2 = vrayRectWidget(mdiArea, 'bbbb')

        newItem1.setMouseTracking(True)
        newItem2.setMouseTracking(True)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
class vrayRectWidget(QMdiSubWindow):
    def __init__(self, parent, name):
        super(vrayRectWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(name)

        self.view = MyView()
        self.view.setMouseTracking(True)
        self.setWidget(self.view)


#----------------------------------------------------------------------
#----------------------------------------------------------------------
class MyView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)

        self.setGeometry(QRect(100, 100, 600, 400))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.setMouseTracking(True)

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(QRectF())
        self.setScene(self.scene)
        self.setInteractive(True)

        for i in range(5):
            item = QGraphicsEllipseItem(i*75, 10, 60, 40)

            item.setFlag(QGraphicsItem.ItemIsMovable, True)
            item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.scene.addItem(item)

    def mousePressEvent(self, event):
        print('mousePressEvent')

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# window
def cacheWnd():
    wnd = MainForm()
    wnd.show()

cacheWnd()