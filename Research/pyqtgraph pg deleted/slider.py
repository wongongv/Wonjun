import sys
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph import SpinBox, LayoutWidget
import numpy as np
import glo_var

class Slider(QtGui.QWidget):
	def __init__(self, minimum, maximum, label, tick=0, parent=None):
		super(Slider, self).__init__(parent=parent)
		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.label = QtGui.QLabel(self)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.font = QtGui.QFont("?",18)
		self.label.setFont(self.font)
		
		if label == "\u2113":
			self.spin = SpinBox(value = glo_var.l, bounds=[1, 20],parent = self)
			self.spin.setRange(1,20)
			self.intspinargs = {"int":True, "step":1}
			self.spin.setOpts(**self.intspinargs)
		elif label == "\u03b1":
			self.spin = SpinBox(value=glo_var.alpha, bounds=[0, 1],parent=self)
		else:
			self.spin = SpinBox(value=glo_var.beta, bounds=[0, 1],parent =self)


		self.verticalLayout.addWidget(self.label)

		self.verticalLayout.addWidget(self.spin)
		
		self.horizontalLayout = QtGui.QHBoxLayout()
		spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.slider = QtGui.QSlider(self)
		self.slider.setOrientation(QtCore.Qt.Vertical)
		
# check!
		self.text_label = label
		self.label.setText(self.text_label)


		self.horizontalLayout.addWidget(self.slider)


		spacerItem1 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.resize(self.sizeHint())
		self.minimum = minimum
		self.maximum = maximum
		self.x = None
		
		if label=="\u2113":
			self.x = 1
			# self.slider.setSingleStep(1)
			self.spin.sigValueChanging.connect(self.Intspinvalue)

		else :
			self.spin.sigValueChanging.connect(self.spinvalue)

		self.slider.minimumSizeHint()
		self.slider.setTickPosition(3)

# check whether the value is exact

	def Intspinvalue(self, sb, value):
		if sb.value()== 0:
			pass
		else:
			self.intsetLabelValue(sb.value(),fromsb=True)

	def spinvalue(self, sb, value):
		self.setLabelValue(sb.value(),fromsb=True)

	def setLabelValue(self, value,fromsb=False):

		if fromsb:
			self.x=value
			self.slider.setValue(self.x*glo_var.slid_precision)
		else:
			self.x = value/glo_var.slid_precision
			self.spin.setValue(self.x)
		
	def intsetLabelValue(self, value, fromsb=False):
		if value == 0:
			pass
		else:
			if fromsb:
				self.x=value
				self.slider.setValue(self.x)
			else:
				self.x = value
				print(self.x)
				self.spin.setValue(self.x)
		


class Widget(QtGui.QWidget):
	def __init__(self, dcontrols, lamb_po, phas,rh,jalph,jbet, parent=None):
		super(Widget, self).__init__(parent=parent)
		self.initiate(dcontrols, lamb_po, phas,rh,jalph,jbet)

	def initiate(self, dcontrols, lamb_po, phas,rh,jalph,jbet):
		self.dcontrols = dcontrols


		self.layout = LayoutWidget()

		self.ws=[]
		self.ws += [Slider(0, 1,"\u03b1")]
		self.ws += [Slider(0, 1,"\u03b2")]
# be careful, the label below affects creation of slide(int or float)
		self.ws += [Slider(1, 10, "\u2113")]
		print(self.ws[2].x)
		for i in range(3) :
			self.layout.addWidget(self.ws[i],row=0,col=i)
		self.dcontrols.addWidget(self.layout)

# =========================================================================
		self.ws[0].slider.setMaximum(glo_var.slid_precision)
		self.ws[0].x = glo_var.alpha
		self.ws[0].setLabelValue(self.ws[0].x*glo_var.slid_precision)
		self.ws[0].slider.setValue(glo_var.alpha*glo_var.slid_precision)
		self.ws[0].slider.valueChanged.connect(self.ws[0].setLabelValue)
  
		self.ws[1].slider.setMaximum(glo_var.slid_precision)
		self.ws[1].x = glo_var.beta
		self.ws[1].setLabelValue(self.ws[1].x*glo_var.slid_precision)
		self.ws[1].slider.setValue(glo_var.beta*glo_var.slid_precision)
		self.ws[1].slider.valueChanged.connect(self.ws[1].setLabelValue)
  

		self.ws[2].x = glo_var.l
		self.ws[2].slider.setPageStep(1)
		self.ws[2].intsetLabelValue(self.ws[2].x)
		self.ws[2].slider.setValue(glo_var.l)
		self.ws[2].slider.valueChanged.connect(self.ws[2].intsetLabelValue)       
		
		self.ws[2].slider.setMaximum(20)
		self.ws[2].slider.setMinimum(1)
# =====================================================================================================================================
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.update_l_slid(self.ws[2])



		[self.ws[i].slider.valueChanged.connect(self.update_ab_rh) for i in range(2)]
		self.ws[2].slider.valueChanged.connect(self.update_lamb_l)

		self.phas=phas
		self.rh=rh
		self.jalph = jalph
		self.jbet = jbet
		self.lamb_po = lamb_po
		self.phas.receive(self)
		self.update_ab_rh()


# Updates
	def update_lamb_rh(self, index, y, remove):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		glo_var.l = self.ws[2].x
		if remove == 0:
			glo_var.lambdas[index][1] = y
		self.lamb_po.update()
		self.rh.update()
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()


	def update_lamb_l(self):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		glo_var.l = self.ws[2].x

		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		# self.lamb_po.update()
		self.rh.update()
		self.phas.update()
		self.jalph.update()
		self.jbet.update()

	def update_phas(self, a, b):
		glo_var.alpha = a
		glo_var.beta = b

		self.rh.update()
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()


	def update_ab_rh(self):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		self.rh.update()
		self.phas.update()
		self.jalph.update()
		self.jbet.update()


	def update_l_slid(self,slid):
		slid.x = glo_var.l
		slid.spin.setValue(slid.x)
		slid.intsetLabelValue(slid.x)
		slid.slider.setValue(glo_var.l)

	def update_alpha_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.alpha_star*glo_var.slid_precision)
		slid.spin.setRange(0,2*glo_var.alpha_star)
		slid.x = glo_var.alpha
		temp=glo_var.beta
		slid.spin.setValue(slid.x)
		glo_var.beta = temp
		slid.setLabelValue(slid.x*glo_var.slid_precision)
		slid.slider.setValue(glo_var.alpha*glo_var.slid_precision)

	def update_beta_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.beta_star*glo_var.slid_precision)
		slid.spin.setRange(0,2*glo_var.beta_star)
		slid.x = glo_var.beta
		temp = glo_var.beta	
		slid.spin.setValue(slid.x)
		glo_var.beta = temp
		slid.setLabelValue(slid.x*glo_var.slid_precision)
		slid.slider.setValue(glo_var.beta*glo_var.slid_precision)