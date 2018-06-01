
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt


# required variables alhpha, beta, lambdas
class rho:
	def __init__(self,drho):

		self.drho = drho
		self.p2main = glo_var.MyPW(x="x", y1= "\U0001d780", set_range = self.set_range)
		self.viewbox = self.p2main.getPlotItem().getViewBox()
		self.viewbox.setBackgroundColor('w')
		self.p2 = self.p2main.plotItem
		self.p2main.coordinate_label = QtGui.QLabel()
		self.frame = glo_var.setframe(self.p2main, width = 1, coordinate_label = self.p2main.coordinate_label)
		self.drho.addWidget(self.frame)
		self.p2.addLegend = glo_var.myaddLegend
		self.p2.addLegend(self.p2, offset=(0,0.0000001))
		self.initiating = 1
		self.p2main.setLabel('left',"\U0001d780",**glo_var.labelstyle)
		self.p2main.setLabel('bottom',"x",**glo_var.labelstyle)
		self.set_range()
		self.rpen=pg.mkPen('r', width=glo_var.line_width, style=QtCore.Qt.DashLine)  
		self.lpen=pg.mkPen(color=(16,52,166), width=glo_var.line_width, style=QtCore.Qt.DashLine)
		self.realpen=pg.mkPen('k', width=2)
		self.update()
		self.legend()

	def legend(self):
		self.p2.plot(pen=self.realpen, name='\U0001d780')
		self.p2.plot(pen=self.rpen, name='\U0001d780+')
		self.p2.plot(pen=self.lpen, name='\U0001d780-')
	
	def set_range(self):
		self.viewbox.setLimits(xMin = -0.03, yMin = -0.03, xMax = 1.03, yMax = 1.03)
		self.viewbox.setRange(xRange=[0,1],yRange=[0,1/glo_var.l],padding=0.1)
		
	def update(self):
# should care about when there is no lambda? division by zero error.

		self.p2.clear()
		self.viewbox.setRange(xRange=[0,1],yRange=[0,1/glo_var.l])
		self.value_declaration()
		self.cal_stars()
		if self.initiating:
			glo_var.alpha = 1.2 * self.alpha_star
			glo_var.beta = 1.2 * self.beta_star
			self.initiating = 0

		self.calculation()
# assign values
		glo_var.j_l = self.j_l
		glo_var.j_r = self.j_r
		glo_var.alpha_star=self.alpha_star
		glo_var.beta_star=self.beta_star



		self.p2main.plot(self.lambdas_xval, self.rho_l, pen=self.lpen)
		self.p2main.plot(self.lambdas_xval, self.rho_r, pen=self.rpen)
		self.plot_scat(self.scat_step)

		if self.num_mins > 1:
			c = np.rec.fromarrays([self.scat_xs,self.scat_ys])
			c.sort()
			self.p2main.plot(c.f0,c.f1, pen=self.realpen)
		else:
			self.p2main.plot(self.scat_xs, self.scat_ys, pen=self.realpen)

	def calculation(self):

		self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
		self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
		
		self.lamb_func = []
		for i in range(glo_var.lambdas_degree - 1):
			self.lamb_func += [ lambda x : ((self.lambdas_ys[i + 1] - self.lambdas_ys[i])/(self.lambdas_xs[i + 1] - self.lambdas_xs[i])) * ( x - self.lambdas_xs[i]) + self.lambdas_ys[i] ] 

		self.xperlambdas = 1 if round(149/glo_var.lambdas_degree) == 0 else round(149/glo_var.lambdas_degree)
		self.lambdas_yval = []
		self.lambdas_xval = []
		for i in range(glo_var.lambdas_degree - 1):
			for j in np.linspace(self.lambdas_xs[i],self.lambdas_xs[i + 1], self.xperlambdas):
				self.lambdas_xval+= [j]
				self.lambdas_yval+= [self.lamb_func[i](j)]


		self.j=self.js(glo_var.alpha,glo_var.beta)
		self.rhointercal=[]
		self.rho_l = []
		self.rho_r = []
		for lambda_x in self.lambdas_yval:
			if lambda_x !=0:
				self.intercal1 = 1/(2*self.l) + self.j*(self.l-1)/(2*self.l*lambda_x)
				self.intercal2 = pow(1/(2*self.l) + self.j*(self.l-1)/(2*self.l*lambda_x),2) - self.j/(self.l*lambda_x)
				self.rhointercal+=[(self.intercal1,self.intercal2)]
			else:
				print('lambda_x cannot be 0')
		for x,y in self.rhointercal:
			self.inter_y=sqrt(0 if y < 0.000001 else y)
			self.rho_l += [x - self.inter_y] 
			self.rho_r += [x + self.inter_y]



	def get_cross(self,upper_array,lower_array,start_position,end_position,steps):
		step_val=(upper_array[end_position] - lower_array[start_position])/steps
		self.cross_array=[]
		for i in range(steps + 1):
			self.cross_array += [lower_array[start_position] + i*step_val]
		return self.cross_array

	def js(self, alpha, beta):
		# LD 1, HD 2, MC 3 
		if beta >= self.beta_star:
			if alpha <= self.alpha_star:
				self.region = 1
				return alpha*(self.lambda_0-alpha)/(self.lambda_0+(self.l-1)*alpha)
			else :
				self.region = 3
				return self.lambda_min/pow((1+sqrt(self.l)),2)
		elif beta < self.beta_star:
			if alpha < self.alpha_star:
				self.jl = alpha*(self.lambda_0-alpha)/(self.lambda_0+(self.l-1)*alpha)
				self.jr = beta*(self.lambda_1-beta)/(self.lambda_1+(self.l-1)*beta)
				if self.jl <= self.jr:
					self.region = 1 
					return self.jl
				else :
					self.region = 2
					return self.jr
			else :
				self.region = 2
				return beta*(self.lambda_1-beta)/(self.lambda_1+(self.l-1)*beta)



	def value_declaration(self):
		self.l = glo_var.l
		self.alpha = glo_var.alpha
		self.beta = glo_var.beta
		self.linspace=np.linspace(0,1,100)
		self.lambda_0=glo_var.lambdas[0][1]
		self.lambda_1=glo_var.lambdas[-1][1]
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas))
		self.lambda_min=min(self.lambdas_ys)
		self.lambda_max=max(self.lambdas_ys)
		self.scat_step = 3
		self.scat_cross_step = 0

		# notice, actual cross_steps will be twice + 1 of it.

	def cal_stars(self):
		self.intercall=pow(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_0*self.lambda_min/pow(1+sqrt(self.l),2)
		self.intercalr=pow(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_1*self.lambda_min/pow(1+sqrt(self.l),2)
		self.alpha_star=0.5*(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt( 0 if self.intercall < 0.0000001 else self.intercall))
		self.beta_star=0.5*(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt(0 if self.intercalr < 0.0000001 else self.intercalr))

	def check_two_mins(self):
		self.minlocation = []
		self.maxlocation = []
		counter=0
		
		for i in self.lambdas_ys:
			if i == self.lambda_min:
				self.minlocation+=[counter]
			counter += 1
		num=len(self.minlocation)
		if num > 1:
			for j in range(num - 1):
				val = max(self.lambdas_ys[self.minlocation[j]:self.minlocation[j+1]])
				self.maxlocation += [self.lambdas_ys.index(val,self.minlocation[j])]
		return num

		
	def clear(self):
		self.axes.remove()

	def getscatarray(self,array,step):
		return array[::step]

	def plot_scat(self,steps):
		self.num_mins = self.check_two_mins()
		self.scat_ys = []
		self.scat_xs = []
		if self.region == 3:
			if self.num_mins > 1:
				self.index1 = self.minlocation[0]*self.xperlambdas
				self.scat_xs += self.getscatarray(self.lambdas_xval[:self.index1],self.xperlambdas)
				self.scat_ys += self.getscatarray(self.rho_r[:self.index1],self.xperlambdas)
				for i in range(1, self.num_mins):
					self.index1 = self.minlocation[i - 1]*self.xperlambdas
					self.index2 = self.minlocation[i]*self.xperlambdas
					self.indexmax = self.maxlocation[i - 1]*self.xperlambdas
					self.scat_xs += self.getscatarray(self.lambdas_xval[self.index1:self.indexmax],self.xperlambdas)
					self.scat_ys += self.getscatarray(self.rho_l[self.index1:self.indexmax],self.xperlambdas)
					self.scat_xs += self.getscatarray(self.lambdas_xval[self.indexmax:self.index2],self.xperlambdas)
					self.scat_ys += self.getscatarray(self.rho_r[self.indexmax:self.index2],self.xperlambdas)
					difference = self.rho_r[self.indexmax] - self.rho_l[self.indexmax]
					lb=self.rho_l[self.indexmax]
					self.dist = 2 if round(difference*10) == 0 else int(round(difference*10)) 
					for j in range(self.dist):
						self.scat_xs += [self.lambdas_xval[self.indexmax]]
						self.scat_ys += [lb + j*difference/self.dist]
				self.scat_xs += self.getscatarray(self.lambdas_xval[self.index2:],self.xperlambdas)
				self.scat_ys += self.getscatarray(self.rho_l[self.index2:],self.xperlambdas)
				
				self.scat_xs += [self.lambdas_xval[-1]]
				self.scat_ys += [self.rho_l[-1]]
			else :
				self.index = self.minlocation[0]*self.xperlambdas
				self.scat_xs += self.getscatarray(self.lambdas_xval[:self.index],self.xperlambdas) + self.getscatarray(self.lambdas_xval[self.index:],self.xperlambdas)
				self.scat_ys += self.getscatarray(self.rho_r[:self.index],self.xperlambdas) + self.getscatarray(self.rho_l[self.index:],self.xperlambdas)

				self.scat_xs += [self.lambdas_xval[-1]]
				self.scat_ys += [self.rho_l[-1]]
		elif self.region == 2:
			self.scat_xs = self.getscatarray(self.lambdas_xval,self.xperlambdas)
			self.scat_ys = self.getscatarray(self.rho_r,self.xperlambdas)

			self.scat_xs += [self.lambdas_xval[-1]]
			self.scat_ys += [self.rho_r[-1]]
		else:
			self.scat_xs = self.getscatarray(self.lambdas_xval,self.xperlambdas)
			self.scat_ys = self.getscatarray(self.rho_l,self.xperlambdas)

			self.scat_xs += [self.lambdas_xval[-1]]
			self.scat_ys += [self.rho_l[-1]]

