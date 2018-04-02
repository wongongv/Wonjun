from PyQt4 import QtCore, QtGui

class Widget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)

        self._images = [
            QtGui.QPixmap('Smiley.png'),
            QtGui.QPixmap('Smiley2.png')
        ]

        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        # max is the last index of the image list
        self.slider.setMaximum(len(self._images)-1)
        self.layout.addWidget(self.slider)

        # set it to the first image, if you want.
        self.sliderMoved(0)

        self.slider.sliderMoved.connect(self.sliderMoved)

    def sliderMoved(self, val):
        # print "Slider moved to:", val
        try:
            self.image.setPixmap(self._images[val])
        except IndexError:
            print('s')


if __name__ == "__main__":
    app = QtGui.QApplication([])
    w = Widget()
    w.show()
    w.raise_()
    app.exec_()