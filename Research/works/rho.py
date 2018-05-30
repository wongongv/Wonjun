
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt


# required variables alhpha, beta, lambdas
class rho:
	def __init__(self,drho):

		self.drho = drho
		self.p2main = glo_var.MyPW()
		self.viewbox = self.p2main.getPlotItem().getViewBox()
		self.viewbox.setBackgroundColor('w')
		self.p2 = self.p2main.plotItem

		self.frame = glo_var.setframe(self.p2main, width = 1)
		self.drho.addWidget(self.frame)

		self.p2.addLegend = glo_var.myaddLegend
		self.p2.addLegend(self.p2, offset=(-10,50))
		
		self.initiating = 1

		self.p2main.setLabel('left',"\u03c1",**glo_var.labelstyle)
		self.p2main.setLabel('bottom',"x",**glo_var.labelstyle)


		# self.viewbox=self.p2main.getViewBox()
		self.p2main._rescale=self.set_range
		self.rpen=pg.mkPen('r', width=glo_var.line_width, style=QtCore.Qt.DashLine)  
		self.lpen=pg.mkPen(color=(16,52,166), width=glo_var.line_width, style=QtCore.Qt.DashLine)
		self.realpen=pg.mkPen('k', width=2)
		self.update()
		self.legend()

	def legend(self):
		self.p2.plot(pen=self.realpen, name='\u03c1')
		self.p2.plot(pen=self.rpen, name='\u03c1+')
		self.p2.plot(pen=self.lpen, name='\u03c1-')
	
	def set_range(self):
		self.viewbox.setLimits(xMin = -0.01, yMin = -0.01, xMax = 1.01, yMax = 1.01)
		self.viewbox.setRange(xRange=[0,1],yRange=[0,1/glo_var.l])
		
	def update(self):
		# self.p2main.clear()
		# self.linspace=np.linspace(0,1,100)
		# self.lambda_ys=glo_var.lambda_function(self.linspace)

		# self.lambda_0=glo_var.lambdas[0][1]
		# self.lambda_1=glo_var.lambdas[glo_var.lambdas_degree - 1][1]
		# self.lambda_min=min(self.lambda_ys)
		# self.l = glo_var.l
		# self.alpha = glo_var.alpha
		# self.beta = glo_var.beta

		# self.intercall=pow(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_0*self.lambda_min/pow(1+sqrt(self.l),2)
		# self.intercalr=pow(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_1*self.lambda_min/pow(1+sqrt(self.l),2)
		# self.alpha_star=0.5*(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt( 0 if self.intercall < 0.0000001 else self.intercall))
		# self.beta_star=0.5*(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt(0 if self.intercalr < 0.0000001 else self.intercalr))


		# self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
		# self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
		# self.rhointercall=[(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),2) - self.j_l/(self.l*lambda_x)) for lambda_x in self.lambda_ys]
		# self.rhointercalr=[(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),2) - self.j_r/(self.l*lambda_x)) for lambda_x in self.lambda_ys] 
		# self.rho_l=[x - sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercall]
		# self.rho_r=[x + sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercalr]

		# glo_var.j_l = self.j_l
		# glo_var.j_r = self.j_r
		# glo_var.alpha_star=self.alpha_star
		# glo_var.beta_star=self.beta_star

		# self.p2main.plot(self.linspace, self.rho_l, name = r'\rho_L',pen='r')
		# self.p2main.plot(self.linspace, self.rho_r, name = r'\rho_R',pen='b')

# should care about when there is no lambda? division by zero error.

		self.p2.clear()
		self.viewbox.setRange(xRange=[0,1],yRange=[0,1/glo_var.l])
		self.value_declaration()
		self.cal_stars()
		if self.initiating:
			glo_var.alpha = 1.5 * self.alpha_star
			glo_var.beta = 1.5 * self.beta_star
			self.initiating = 0
		# self.cal_lamb_fun()
		self.calculation()
# assign values
		glo_var.j_l = self.j_l
		glo_var.j_r = self.j_r
		glo_var.alpha_star=self.alpha_star
		glo_var.beta_star=self.beta_star



		self.p2main.plot(self.lambdas_xval, self.rho_l, pen=self.lpen)
		self.p2main.plot(self.lambdas_xval, self.rho_r, pen=self.rpen)
		self.plot_scat(self.scat_step)
		# self.p2main.plot(self.scat_xs, self.scat_ys, pen=None, symbol='o', symbolPen='r')

		if self.num_mins > 1:
			c = np.rec.fromarrays([self.scat_xs,self.scat_ys])
			c.sort()
			self.p2main.plot(c.f0,c.f1, pen=self.realpen)
		else:
			self.p2main.plot(self.scat_xs, self.scat_ys, pen=self.realpen)
		# until here.
# calculating transition line
		# self.al_func = lambda x : x*(self.lambda_0-x)/(self.lambda_0 + (self.l - 1)*x)
		# self.beta_func = lambda x : x*x +x*(-self.lambda_1 + (self.l - 1)*self.al_term) + self.lambda_1*self.al_term 


		# self.axes.clear()
		# self.axes.set_xlim(0,1)
		# self.axes.set_ylim(0,1)
		# think about make it polynomial

		# self.xs = np.linspace(0,1, glo_var.lambdas_degree * 10)
		# self.csl = CubicSpline(self.lambdas_xs, self.rho_l)
		# self.csr = CubicSpline(self.lambdas_xs, self.rho_r)
		# self.axes.plot(self.lambdas_xs, self.rho_l, 'o')
		# self.axes.plot(self.lambdas_xs, self.rho_r, 'o')
		# self.axes.plot(self.xs, self.csl(self.xs))
		# self.axes.plot(self.xs, self.csr(self.xs))
		# self.pol_l = interp1d(self.lambdas_xs, self.rho_l, kind = 'quadratic')
		# self.pol_r = interp1d(self.lambdas_xs, self.rho_r, kind = 'quadratic')
		# self.x = np.linspace(0,1, glo_var.lambdas_degree * 10)
		# self.pol_l_plot = self.axes.plot(self.lambdas_xs, self.rho_l, 'o', self.x, self.pol_l(self.x))
		# self.pol_r_plot = self.axes.plot(self.lambdas_xs, self.rho_r, 'o', self.x, self.pol_r(self.x))


		# self.linel=Line2D(self.lambdas_xs, self.rho_l, color = 'b')
		# self.liner=Line2D(self.lambdas_xs, self.rho_r, color = 'r')
		# self.rholup = self.axes.add_line(self.linel)
		# self.rhorup = self.axes.add_line(self.liner)
		# self.rholup.set_ydata(self.rho_l)
		# self.rhorup.set_ydata(self.rho_r)

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
		# np.seterr(all='warn')
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
	#  what if num_mins is 3?
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

	# def plot_scat(self,steps,cross_steps):
	# 	self.num_mins = self.check_two_mins()
	# 	if self.region == 3:
	# 		if self.num_mins == 1 :
	# 			self.scat_xs = self.getscatarray(self.lambdas_xval[:self.min_location_1*self.xperlambdas],steps) + self.getscatarray(self.lambdas_xval[self.min_location_1*self.xperlambdas:],steps)
	# 			self.scat_ys = self.getscatarray(self.rho_r[:self.min_location_1*self.xperlambdas],steps) + self.getscatarray(self.rho_l[self.min_location_1*self.xperlambdas:],steps)
	# 			self.p2main.plot(self.scat_xs, self.scat_ys, pen=None, symbol='o', symbolPen='r')
	# 		elif self.num_mins == 2:
	# 			self.scat_xs =  self.getscatarray(self.lambdas_xval[:self.min_location_1*self.xperlambdas],steps) \
	# 							+ self.getscatarray(self.lambdas_xval[self.min_location_1*self.xperlambdas:self.max_location_1*self.xperlambdas-cross_steps],steps) \
	# 							+ self.getscatarray(self.lambdas_xval[self.max_location_1*self.xperlambdas-cross_steps:self.max_location_1*self.xperlambdas+cross_steps + 1],1) \
	# 							+ self.getscatarray(self.lambdas_xval[self.max_location_1*self.xperlambdas+cross_steps + 1:self.min_location_2*self.xperlambdas],steps) \
	# 							+ self.getscatarray(self.lambdas_xval[self.min_location_2*self.xperlambdas:],steps)
	# 			self.scat_ys = self.getscatarray(self.rho_r[:self.min_location_1*self.xperlambdas],steps) \
	# 							+ self.getscatarray(self.rho_l[self.min_location_1*self.xperlambdas:self.max_location_1*self.xperlambdas-cross_steps],steps) \
	# 							+ self.get_cross(self.rho_r,self.rho_l,self.max_location_1*self.xperlambdas-cross_steps ,self.max_location_1*self.xperlambdas+cross_steps + 1,cross_steps*2) \
	# 							+ self.getscatarray(self.rho_r[self.max_location_1*self.xperlambdas+cross_steps + 1:self.min_location_2*self.xperlambdas],steps) \
	# 							+ self.getscatarray(self.rho_l[self.min_location_2*self.xperlambdas:], steps)

	# #  what if num_mins is 3?
	# 	elif self.region == 2:
	# 		self.scat_xs = self.getscatarray(self.lambdas_xval,steps)
	# 		self.scat_ys = self.getscatarray(self.rho_r,steps)

	# 	else:
	# 		self.scat_xs = self.getscatarray(self.lambdas_xval,steps)
	# 		self.scat_ys = self.getscatarray(self.rho_l,steps)



	# def calculation(self):

	# 	self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
	# 	self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
		
	# 	self.lamb_func = []
	# 	for i in range(glo_var.lambdas_degree - 1):
	# 		self.lamb_func += [ lambda x : ((self.lambdas_ys[i + 1] - self.lambdas_ys[i])/(self.lambdas_xs[i + 1] - self.lambdas_xs[i])) * ( x - self.lambdas_xs[i]) + self.lambdas_ys[i] ] 

	# 	self.xperlambdas = round(150/glo_var.lambdas_degree)
	# 	self.lambdas_yval = []
	# 	self.lambdas_xval = []
	# 	for i in range(glo_var.lambdas_degree - 1):
	# 		for j in np.linspace(self.lambdas_xs[i],self.lambdas_xs[i + 1], self.xperlambdas):
	# 			self.lambdas_xval+= [j]
	# 			self.lambdas_yval+= [self.lamb_func[i](j)]


	# 	self.j=self.js(glo_var.alpha,glo_var.beta)
	# 	self.rhointercal=[]
	# 	self.rho_l = []
	# 	self.rho_r = []
	# 	# np.seterr(all='warn')
	# 	for lambda_x in self.lambdas_yval:
	# 		if lambda_x !=0:
	# 			self.intercal1 = 1/(2*self.l) + self.j*(self.l-1)/(2*self.l*lambda_x)
	# 			self.intercal2 = pow(1/(2*self.l) + self.j*(self.l-1)/(2*self.l*lambda_x),2) - self.j/(self.l*lambda_x)
	# 			self.rhointercal+=[(self.intercal1,self.intercal2)]
	# 		else:
	# 			print('lambda_x cannot be 0')
	# 	for x,y in self.rhointercal:
	# 		self.inter_y=sqrt(0 if y < 0.000001 else y)
	# 		self.rho_l += [x - self.inter_y] 
	# 		self.rho_r += [x + self.inter_y]


