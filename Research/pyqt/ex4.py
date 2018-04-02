# drag and drop
import pyqtgraph as pg
from PyQt4 import QtGui
app = pg.QtGui.QApplication([])

l = pg.QtGui.QListWidget()
l.addItem('Drag me')
l.setDragDropMode(l.DragOnly)
l.show()

win = pg.GraphicsWindow()
win.show()

def dragEnterEvent(ev):
    ev.accept()

win.dragEnterEvent = dragEnterEvent

plot = pg.PlotItem()
plot.setAcceptDrops(True)
win.addItem(plot)

def dropEvent(event):
    print("Got drop!")

plot.dropEvent = dropEvent

if __name__ == "__main__":
    # app = QtGui.QApplication([])
    # w = Widget()
    # w.show()
    # w.raise_()
    app.exec_()