import sys
from PyQt4.QtGui import *

filename = 'Screenshot.jpg'
app = QApplication(sys.argv)
widget = QWidget()
widget.setLayout(QVBoxLayout())
label = QLabel()
widget.layout().addWidget(label)

def take_screenshot():
    p = QPixmap.grabWindow(widget.winId())
    print(widget.winId())
    print(dir(widget.winId()))

    p.save(filename, 'jpg')

widget.layout().addWidget(QPushButton('take screenshot', clicked=take_screenshot))

widget.show()
app.exec_()