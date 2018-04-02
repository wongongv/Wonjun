import sys
from PyQt4 import QtCore, QtGui
from untitled import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
# import serial
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import datetime
#all turn off everything when exit
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.connectbut, QtCore.SIGNAL('clicked()'), self.connectarduino)
        self.ui.ctrl_MAX.toggled.connect(self.maxtoggle)
        self.ser=None #declare arduino
        #create a pyqtgraph for plotting
        self.p = pg.plot()
        self.p.setWindowTitle('live plot from serial')
        self.p.addLegend()
        self.p.setTitle('Python-Arduino Temp Controller')
        self.p.setLabel('bottom', text='Time', units='s')
        self.p.setLabel('left', text='Temp', units='oC')
        self.curve_max = self.p.plot(pen='r', name='MAX31855')
        self.curve_ds = self.p.plot(pen='g', name='DS18B20')
        #self.curve_mlx = self.p.plot(pen='b', name='MLX90614')
        #to do add a line for setpoint
        self.data_max =[]
        self.data_ds = []
        self.data_mlx = []
        self.data_time = []
        self.timer= QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updategraph)
        #declare factor of ctrl cmd
        self.ctrlsys = 'a'
        self.ctrlstate = '0'
        self.ctrltune = '0'
        self.ctrlsetpoint = 0.00
        self.ctrlkp = 0.00
        self.ctrlti= 0.00
        self.ctrltd = 0.00
        self.ctrlcmd = "a,0,0,0,0,0,0,"
        #declare factors for autotune
        self.t0temp=0
        self.t0=0
        self.t1temp=0
        self.t1=0
        self.t2temp=0
        self.t2=0
        #declare for xml
        self.xml_root=None



    @QtCore.pyqtSlot(bool)
    def maxtoggle(self, checked):
        if not checked:
            #send turn off on max pid to arduino
            try:
                self.ser.open()
            except:
                pass
            self.ctrlcmd = 'a,0,0'
            self.ser.write(self.ctrlcmd.encode())
            self.timer.stop()
            self.cleargraph()
            #print "turn off MAx"
        elif checked:
            #send turn on to max pid to arduino
            try:
                self.ser.open()
            except:
                #print "already open"
                pass
            self.ctrlcmd = 'a,1,0,%s,%s,%s,%s' % (str(self.ui.sp_MAX.value()), str(self.ui.MAX_kc.value()), str(self.ui.MAX_ti.value()), str(self.ui.MAX_td.value()))
            #print self.ctrlcmd
            #self.ctrlcmd = 'a,1,0,%s,%s,%s,%s' % (self.ui.sp_MAX.value(), self.ui.MAX_kc.value(), self.ui.MAX_ti.value(), self.ui.MAX_td.value())
            self.ser.write(self.ctrlcmd.encode())
            #start new plotting
            self.timer.stop()
            self.timer.start(100)

            #print "turn on MAX"


    def connectarduino(self):
        try:
            port = str(self.ui.comlisttext.toPlainText())
            self.ser = serial.Serial(port, 9600)
            self.ui.connectbut.setText("Connected")
            self.ui.connectbut.setEnabled(False)
            self.ui.groupBox.setEnabled(True)
            self.ui.groupBox_2.setEnabled(True)
            self.timer.start(1000)
        except:
            print ('failed')


    def updategraph(self):
        try:
            self.ser.open()
        except:
            #print "already open"
            pass
        #global curve_max, curve_dx, curve_mlx, data_max, data_ds, data_mlx, curve_time, data_time
        line = self.ser.readline().rstrip().split(",")
        #print line
        #update label in the gui
        self.ui.MAX_raw.setText(line[3])
        maxtemp = float(line[3])+self.ui.MAX_calib.value()
        self.ui.MAX_Temp.setText(str(maxtemp))
        self.ui.ds_raw.setText(line[5])
        dstemp = float(line[5])+self.ui.ds_calib.value()
        self.ui.ds_Temp.setText(str(dstemp))
        #plot the calibrated temperature
        self.data_time.append(float(line[1])/1000.0)
        self.data_max.append(maxtemp)
        self.data_ds.append(dstemp)
        #self.data_mlx.append(float(line[7]))
        ydata_time = np.array(self.data_time, dtype='float64')
        ydata_max = np.array(self.data_max, dtype='float64')
        ydata_ds = np.array(self.data_ds, dtype='float64')
        #ydata_mlx = np.array(self.data_mlx, dtype='float64')
        self.curve_max.setData(x=ydata_time, y=ydata_max)
        self.curve_ds.setData(x=ydata_time, y=ydata_ds)
        #self.curve_mlx.setData(x=ydata_time, y=ydata_mlx)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    # Log = Log()
    # Log.message.connect(myapp.on_Log_message)
    # sys.stdout=Log
    sys.exit(app.exec_())
