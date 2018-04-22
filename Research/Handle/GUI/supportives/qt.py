
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import pyqtgraph as pg


class Gui(QtGui.QMainWindow, ui_test.Ui_MainWindow):


    def __init__(self):        
        super(self.__class__, self).__init__()        
        self.setupUi(self)  # This is defined in ui_pumptest.py file automatically   
        self.plot()

    def plot(self):       
        vb = pg.ViewBox()
        self.graphicsView.setCentralItem(vb)
def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = Gui()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the. app

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

