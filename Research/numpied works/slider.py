import sys
from pyqtgraph.Qt import QtCore, QtGui
# from PyQt4.QtCore import Qt
# from PyQt4.QtGui import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
# 	QVBoxLayout, QWidget,QStyleOptionSlider
import pyqtgraph as pg
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
		
		if label == "l":
			self.spin = pg.SpinBox(value = glo_var.l)
			self.spin.setRange(1,20)
			self.intspinargs = {'int':True,'step':1}
			self.spin.setOpts(**self.intspinargs)
		else:
			self.spin = pg.SpinBox(value=glo_var.alpha, bounds=[0, 1])


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

		# self.font = QtGui.QFont("?",30, QtGui.QFont.Bold) 

		# self.label2 = QtGui.QLabel(label)
		# self.label2.setFont(self.font)
		# self.horizontalLayout.addWidget(self.label2)
	

		self.horizontalLayout.addWidget(self.slider)


		spacerItem1 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.resize(self.sizeHint())
		self.minimum = minimum
		self.maximum = maximum
		self.x = None
		
		if label=='l':
			self.x = 1
			# self.slider.setValue(self.x)
			self.slider.setSingleStep(1)
			self.spin.sigValueChanging.connect(self.Intspinvalue)

			# self.slider.setTickInterval(1)
			# self.slider.valueChanged.connect(self.Intspinvalue)
		else :
			self.spin.sigValueChanging.connect(self.spinvalue)
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

	def Intspinvalue(self, sb, value):
		if sb.value()== 0:
			pass
		else:
			self.intsetLabelValue(sb.value(),fromsb=True)

	def spinvalue(self, sb, value):
		self.setLabelValue(sb.value(),fromsb=True)

# fromsb = from spinbox
	def setLabelValue(self, value,fromsb=False):
		# self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
		# self.maximum - self.minimum)
		# if fromsb:
		# 	self.x = value
		# 	print(self.x)
		if fromsb:
			self.x=value
			self.slider.setValue(self.x*glo_var.slid_precision)
		else:
			self.x = value/glo_var.slid_precision
			self.spin.setValue(self.x)
		
		# self.label.setText(self.text_label + " : " + "{0:.4g}".format(self.x))

	def intsetLabelValue(self, value, fromsb=False):
		if value == 0:
			pass
		else:
			if fromsb:
				self.x=value
				self.slider.setValue(self.x)
				print("fromsb",self.x)
			else:
				self.x = value
				self.spin.setValue(self.x)
				print("here",self.x)
		
		# self.label.setText(self.text_label + " : " + "{0:.2g}".format(self.x))
		# self.spin.setValue(self.x)

# class Widget(QWidget):
# 	def __init__(self, win, lamb_po, phas,rh,jalph,jbet, parent=None):
# 		super(Widget, self).__init__(parent=parent)
# 		self.horizontalLayout = QHBoxLayout(self)
# 		self.ws=[]
# 		for i in range(glo_var.lambdas_degree + 2) :
# 			self.ws += [Slider(0, 1)]
# 		self.ws += [Slider(1,10)]
# 		for i in range(glo_var.lambdas_degree + 3) :
# 			self.horizontalLayout.addWidget(self.ws[i])
# 		for i in range(glo_var.lambdas_degree):
# 			self.ws[i].slider.setMaximum(glo_var.slid_precision)
# 			self.ws[i].slider.setPageStep(0.01)
# 			self.ws[i].slider.setValue(glo_var.lambdas[i][1]*glo_var.slid_precision)
# 			self.ws[i].x = glo_var.lambdas[i][1]
# 			self.ws[i].setLabelValue(self.ws[i].x*glo_var.slid_precision)
# 			self.ws[i].slider.valueChanged.connect(self.ws[i].setLabelValue)
# # alpha,beta,l


# # =========================================================================
# 		self.ws[glo_var.lambdas_degree].slider.setMaximum(glo_var.slid_precision)
# 		self.ws[glo_var.lambdas_degree].x = glo_var.alpha
# 		self.ws[glo_var.lambdas_degree].setLabelValue(self.ws[glo_var.lambdas_degree].x*glo_var.slid_precision)
# 		self.ws[glo_var.lambdas_degree].slider.setValue(glo_var.alpha*glo_var.slid_precision)
# 		# self.ws[glo_var.lambdas_degree].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree].setLabelValue)
  
# 		self.ws[glo_var.lambdas_degree + 1].slider.setMaximum(glo_var.slid_precision)
# 		self.ws[glo_var.lambdas_degree + 1].x = glo_var.beta
# 		self.ws[glo_var.lambdas_degree + 1].setLabelValue(self.ws[glo_var.lambdas_degree+1].x*glo_var.slid_precision)
# 		self.ws[glo_var.lambdas_degree + 1].slider.setValue(glo_var.beta*glo_var.slid_precision)
# 		# self.ws[glo_var.lambdas_degree + 1].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree + 1].setLabelValue)
  

# 		self.ws[glo_var.lambdas_degree + 2].x = glo_var.l
# 		self.ws[glo_var.lambdas_degree + 2].slider.setPageStep(1)
# 		self.ws[glo_var.lambdas_degree + 2].intsetLabelValue(self.ws[glo_var.lambdas_degree + 2].x)
# 		self.ws[glo_var.lambdas_degree + 2].slider.setValue(glo_var.l)
# 		self.ws[glo_var.lambdas_degree + 2].slider.valueChanged.connect(self.ws[glo_var.lambdas_degree + 2].intsetLabelValue)       
		
		
# # =====================================================================================================================================
# 		self.update_alpha_slid(self.ws[glo_var.lambdas_degree])
# 		self.update_beta_slid(self.ws[glo_var.lambdas_degree + 1])



# 		[self.ws[i].slider.valueChanged.connect(self.update_lamb_rh) for i in range(glo_var.lambdas_degree)]
# 		[self.ws[i].slider.valueChanged.connect(self.update_ab_rh) for i in range(glo_var.lambdas_degree, glo_var.lambdas_degree + 2)]
# 		self.ws[glo_var.lambdas_degree + 2].slider.valueChanged.connect(self.update_lamb_rh)


# 		self.nwin = win
# 		self.phas=phas


# 		self.rh=rh
# 		self.jalph = jalph
# 		self.jbet = jbet
# 		self.lamb_po = lamb_po
# 		self.update_lamb_rh()
# 		self.update_ab_rh()

class Widget(QtGui.QWidget):
	def __init__(self, dcontrols, lamb_po, phas,rh,jalph,jbet, parent=None):
		super(Widget, self).__init__(parent=parent)

		self.dcontrols = dcontrols


		self.layout = pg.LayoutWidget()

		self.ws=np.array([])
		self.ws = np.append(self.ws, [Slider(0, 1,"\u03b1")])
		self.ws = np.append(self.ws, [Slider(0, 1,"\u03b2")])

		self.ws =np.append(self.ws, [Slider(1, 10, "l")])
		for i in range(3) :
			self.layout.addWidget(self.ws[i],row=0,col=i)
		self.dcontrols.addWidget(self.layout)

# on revision
		# self.horizontalLayout = QHBoxLayout(self)
		# self.ws=[]
		# for i in range(2) :
		# 	self.ws += [Slider(0, 1)]
		# self.ws += [Slider(1,10)]
		# for i in range(3) :
		# 	self.horizontalLayout.addWidget(self.ws[i])
		# self.dcontrols.addWidget
# alpha,beta,l




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
		self.ws[0 + 1].slider.valueChanged.connect(self.ws[1].setLabelValue)
  

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




		# self.layout.addWidget(self.ws[0],1,2)

		self.phas=phas


		self.rh=rh
		self.jalph = jalph
		self.jbet = jbet
		self.lamb_po = lamb_po
		self.phas.receive(self)
		# self.update_lamb_rh()
		self.update_ab_rh()

	# def update_lamb_rh(self):
	# 	glo_var.alpha = self.ws[glo_var.lambdas_degree].x
	# 	glo_var.beta = self.ws[glo_var.lambdas_degree + 1].x

	# 	glo_var.l = self.ws[glo_var.lambdas_degree + 2].x
	# 	self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas)) 
	# 	# pdb.set_trace()
	# 	for i in range(glo_var.lambdas_degree):
	# 		glo_var.lambdas[i]=[self.lambdas_xs[i],self.ws[i].x]

	# 	self.lamb_po.update()

	# 	self.rh.update()
	# 	self.update_alpha_slid(self.ws[glo_var.lambdas_degree])
	# 	self.update_beta_slid(self.ws[glo_var.lambdas_degree + 1])
	# 	self.phas.update()
	# 	self.jalph.update()
	# 	self.jbet.update()
	# 	self.show()

	# def update_ab_rh(self):
	# 	glo_var.alpha = self.ws[glo_var.lambdas_degree].x
	# 	glo_var.beta = self.ws[glo_var.lambdas_degree + 1].x

	# 	self.rh.update()
	# 	self.phas.update()
	# 	self.jalph.update()
	# 	self.jbet.update()
	# 	# a = self.w1.x
	# 	# b = self.w2.x
	# 	# c = self.w3.x
	# 	# d = self.w4.x
	# 	# x = np.linspace(0, 10, glo_var.slid_precision)
	# 	# data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
	# 	# self.curve.setData(data)
	# 	self.show()
	def update_lamb_rh_add(self):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		glo_var.l = self.ws[2].x
		# self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas)) 
		self.lamb_po.update()
		self.rh.update()
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()
		# self.show()

	def update_lamb_l(self):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		glo_var.l = self.ws[2].x
		# self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas)) 
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.lamb_po.update()
		self.rh.update()
		self.phas.update()
		self.jalph.update()
		self.jbet.update()

	def update_phas(self, a, b):
		glo_var.alpha = a
		glo_var.beta = b

		self.ws[0].setLabelValue(a*glo_var.slid_precision)
		self.ws[1].setLabelValue(b*glo_var.slid_precision)

		self.lamb_po.update()
		self.rh.update()
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()

	def update_lamb_rh(self, index, y, remove):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		glo_var.l = self.ws[2].x
		# self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas)) 
		if remove == 0:
			glo_var.lambdas[index][1] = y
		self.lamb_po.update()
		self.rh.update()
		self.update_alpha_slid(self.ws[0])
		self.update_beta_slid(self.ws[1])
		self.phas.update()
		self.jalph.update()
		self.jbet.update()
		# self.show()

	def update_ab_rh(self):
		glo_var.alpha = self.ws[0].x
		glo_var.beta = self.ws[1].x
		self.rh.update()
		self.phas.update()
		self.jalph.update()
		self.jbet.update()
		# a = self.w1.x
		# b = self.w2.x
		# c = self.w3.x
		# d = self.w4.x
		# x = np.linspace(0, 10, glo_var.slid_precision)
		# data = a + np.cos(x + c * np.pi / 180) * np.exp(-b * x) * d
		# self.curve.setData(data)
		# self.show()
		
	def update_l_slid(self,slid):
		slid.x = glo_var.l
		slid.spin.setValue(slid.x)
		slid.intsetLabelValue(slid.x*glo_var.slid_precision)
		slid.slider.setValue(glo_var.l)

	def update_alpha_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.alpha_star*glo_var.slid_precision)
		slid.spin.setRange(0,2*glo_var.alpha_star)
		# slid.slider.setMaximum(2*glo_var.alpha_star*glo_var.slid_precision)
		slid.x = glo_var.alpha
		slid.spin.setValue(slid.x)
		slid.setLabelValue(slid.x*glo_var.slid_precision)
		slid.slider.setValue(glo_var.alpha*glo_var.slid_precision)
		# slid.slider.valueChanged.connect(slid.setLabelValue)
		# self.show()

	def update_beta_slid(self,slid):
		slid.slider.setMaximum(2*glo_var.beta_star*glo_var.slid_precision)
		slid.spin.setRange(0,2*glo_var.beta_star)
		slid.x = glo_var.beta
		slid.spin.setValue(slid.x)
		slid.setLabelValue(slid.x*glo_var.slid_precision)
		slid.slider.setValue(glo_var.beta*glo_var.slid_precision)
		# slid.slider.valueChanged.connect(slid.setLabelValue)
		# self.show()
