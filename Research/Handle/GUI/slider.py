import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
	QVBoxLayout, QWidget,QStyleOptionSlider

import pyqtgraph as pg
import numpy as np
import glo_var
import pdb
class Slider(QWidget):
	def __init__(self, minimum, maximum, tick=0, parent=None):
		super(Slider, self).__init__(parent=parent)
		self.verticalLayout = QVBoxLayout(self)
		self.label = QLabel(self)
		self.verticalLayout.addWidget(self.label)
		self.horizontalLayout = QHBoxLayout()
		spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.slider = QSlider(self)
		self.slider.setOrientation(Qt.Vertical)
		self.horizontalLayout.addWidget(self.slider)
		spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.resize(self.sizeHint())
		self.minimum = minimum
		self.maximum = maximum
		self.x = None
		
		if tick == 1:
			self.x = 1
			self.slider.setValue(1)
			self.slider.setSingleStep(1)
			# self.slider.setTickInterval(1)
			self.slider.valueChanged.connect(self.intsetLabelValue)
		else :
			pass
			# self.x = None
			# self.slider.valueChanged.connect(self.setLabelValue)


		self.slider.minimumSizeHint()
		self.slider.setTickPosition(3)
		# self.slider.setSliderPosition(2)
		# self.setLabelValue(self.slider.value())
		# self.opt = QStyleOptionSlider()
		# pdb.set_trace()
		# self.slider.initStyleOption(self.opt)

# check whether the value is exact

	def setLabelValue(self, value):
		# self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
		# self.maximum - self.minimum)
		self.x = value/100
		self.label.setText("{0:.4g}".format(self.x))

	def intsetLabelValue(self, value):
		self.x = value

		self.label.setText("{0:.1g}".format(self.x))

class Widget(QWidget):
	def __init__(self, win, lamb_po, phas,rh,jalph,jbet, parent=None):
		super(Widget, self).__init__(parent=parent)
		self.horizontalLayout = QHBoxLayout(self)
		self.ws=[]
		for i in range(glo_var.lambdas_degree + 2) :
			self.ws += [Slider(0, 1)]
		self.ws += [Slider(1,10)]
		for i in range(glo_var.lambdas_degree + 3) :
			self.horizontalLayout.addWidget(self.ws[i])
		for i in range(glo_var.lambdas_degree):
			self.ws[i].slider.setMaximum(100)
			self.ws[i].slider.setPageStep(0.01)
			self.ws[i].slider.setValue(glo_var.lambdas[i][1]*100)
			self.ws[i].x = glo_var.lambdas[i][1]
			self.ws[i].setLabelValue(self.ws[i].x*100)
			self.ws[i].slider.valueChanged.connect(self.ws[i].setLabelValue)
# alpha,beta,l


# =========================================================================
		self.ws[glo_var.lambdas_degree].slider.setMaximum(100)
		self.ws[glo_var.lambdas_degree].x = glo_var.alpha
		self.ws[glo_var.lambdas_degree].setLabelValue(self.ws[glo_var.lambdas_degree].x*100)
		self.ws[glo_var.lambdas_degree].slider.setValue(glo_var.alpha*100)
		# self.ws[glo_var.lambdas_degree].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree].setLabelValue)
  
		self.ws[glo_var.lambdas_degree + 1].slider.setMaximum(100)
		self.ws[glo_var.lambdas_degree + 1].x = glo_var.beta
		self.ws[glo_var.lambdas_degree + 1].setLabelValue(self.ws[glo_var.lambdas_degree+1].x*100)
		self.ws[glo_var.lambdas_degree + 1].slider.setValue(glo_var.beta*100)
		# self.ws[glo_var.lambdas_degree + 1].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree + 1].setLabelValue)
  

		self.ws[glo_var.lambdas_degree + 2].x = glo_var.l
		self.ws[glo_var.lambdas_degree + 2].slider.setPageStep(1)
		self.ws[glo_var.lambdas_degree + 2].intsetLabelValue(self.ws[glo_var.lambdas_degree + 2].x)
		self.ws[glo_var.lambdas_degree + 2].slider.setValue(glo_var.l)
		self.ws[glo_var.lambdas_degree + 2].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree + 2].intsetLabelValue)       
		
		
# =====================================================================================================================================
		self.update_alpha_slid(self.ws[glo_var.lambdas_degree])
		self.update_beta_slid(self.ws[glo_var.lambdas_degree + 1])



		[self.ws[i].slider.valueChanged.connect(self.update_lamb_rh) for i in range(glo_var.lambdas_degree)]
		[self.ws[i].slider.valueChanged.connect(self.update_ab_rh) for i in range(glo_var.lambdas_degree, glo_var.lambdas_degree + 2)]
		self.ws[glo_var.lambdas_degree + 2].slider.valueChanged.connect(self.update_lamb_rh)


		self.nwin = win
		self.phas=phas


		self.rh=rh
		self.jalph = jalph
		self.jbet = jbet
		self.lamb_po = lamb_po
		self.update_lamb_rh()
		self.update_ab_rh()



	def update_lamb_rh(self):
		glo_var.alpha = self.ws[glo_var.lambdas_degree].x
		glo_var.beta = self.ws[glo_var.lambdas_degree + 1].x

		glo_var.l = self.ws[glo_var.lambdas_degree + 2].x
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values())) 
		# pdb.set_trace()
		for i in range(glo_var.lambdas_degree):
			glo_var.lambdas[i]=[self.lambdas_xs[i],self.ws[i].x]

		self.lamb_po.update()

		self.rh.update()
		self.update_alpha_slid(self.ws[glo_var.lambdas_degree])
		self.update_beta_slid(self.ws[glo_var.lambdas_degree + 1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()
		self.show()

	def update_ab_rh(self):
		glo_var.alpha = self.ws[glo_var.lambdas_degree].x
		glo_var.beta = self.ws[glo_var.lambdas_degree + 1].x

		self.rh.update()
		self.phas.update()
		self.jalph.update()
		self.jbet.update()
		# a = self.w1.x
		# b = self.w2.x
		# c = self.w3.x
		# d = self.w4.x
		# x = np.linspace(0, 10, 100)
		# data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
		# self.curve.setData(data)
		self.show()
		
	def update_alpha_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.alpha_star*100)
		slid.x = glo_var.alpha

		slid.setLabelValue(slid.x*100)
		slid.slider.setValue(glo_var.alpha*100)
		slid.slider.valueChanged.connect(slid.setLabelValue)
		self.show()		
	def update_beta_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.beta_star*100)
		slid.x = glo_var.beta

		slid.setLabelValue(slid.x*100)
		slid.slider.setValue(glo_var.beta*100)
		slid.slider.valueChanged.connect(slid.setLabelValue)
		self.show()
