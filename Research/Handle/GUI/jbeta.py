
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt
import pdb
from scipy.interpolate import interp1d
class jbeta:
	def __init__(self, win,rh):
		self.win = win
		self.rh=rh
		self.p4 = self.win.addPlot(title = '\u03b2')
		self.viewbox=self.p4.getViewBox()
		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax = 1, yMax = 1)
		# self.ax.set_facecolor()
		self.p4.addLegend()
		self.update()
		self.legend()
		self.p4_2 = self.p4.getViewBox()
		self.p4.showAxis('right')
		self.p4.scene().addItem(self.p4_2)
	def update(self):
		self.p4.clear()
		self.value_declaration()


		# self.j_r=glo_var.alpha*(self.lambda_1-glo_var.alpha)/(self.lambda_1+(glo_var.l-1)*glo_var.alpha)




		self.trans_point = self.trans_func(glo_var.alpha)
		
		self.betas_pre = np.linspace(0,self.trans_point,20)
		

		self.betas_post = np.linspace(self.trans_point,1,20)[1:]
		self.domain = np.concatenate((self.betas_pre,self.betas_post))


		self.j_r_values=np.array([i*(self.lambda_1-i)/(self.lambda_1 + (glo_var.l-1)*i) for i in self.betas_pre])
		
		self.rho_avg = []
		for i in self.domain:
			self.rho_avg += [self.cal_rho(self.js(glo_var.alpha,i))]



		self.j_r_g = interp1d(self.betas_pre,self.j_r_values)

		# minused 0.00000001 since it is not working
		
		self.p4.plot(self.betas_pre,self.j_r_values)
		self.dash = pg.mkPen('y',style=QtCore.Qt.DashLine)
		# Can alpha_star be 0? then I need to add conner case
		if glo_var.alpha >= glo_var.alpha_star:
			self.jpost= self.j_c
		else:
			self.jpost= self.j_l
		self.p4.plot([self.trans_point,1],[self.jpost,self.jpost])
		self.trans_line = self.p4.plot([self.trans_point,self.trans_point],[0,1],pen=self.dash)
		self.alpha_line = self.p4.plot([glo_var.beta,glo_var.beta],[0,1])
		self.make_right_axis()

		# self.plot_sum_rho()
		# self.sum_rho_dash = pg.mkPen('r',style=QtCore.Qt.DashLine)
		# self.p4.plot(self.rh.scat_xs,self.rho_sum)
	def legend(self):
		self.p4.plot(pen='w', name='J')
		self.p4.plot(pen=self.rho_dash, name='\u03c1')

	def make_right_axis(self):
		self.rho_dash = pg.mkPen('r',style=QtCore.Qt.DashLine)
		self.p4.plot(self.domain,self.rho_avg,pen=self.rho_dash)

	def value_declaration(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values()))
		self.lambda_min = min(self.lambdas_ys)
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[glo_var.lambdas_degree - 1][1]
		self.j_c = self.lambda_min/pow(1 + sqrt(glo_var.l),2)
		self.j_l = glo_var.alpha*(self.lambda_0-glo_var.alpha)/(self.lambda_0 + (glo_var.l-1)*glo_var.alpha)
		self.alpha_star = glo_var.alpha_star
		self.beta_star = glo_var.beta_star
		self.alpha=glo_var.alpha
		self.beta=glo_var.beta
		self.l=glo_var.l

	def cal_rho(self,jval):
		self.xperlambdas = round(150/glo_var.lambdas_degree)
		self.rhointercal=[]
		self.rho_l = []
		self.rho_r = []
		# np.seterr(all='warn')
		for lambda_x in self.rh.lambdas_yval:
			if lambda_x !=0:
				self.intercal1 = 1/(2*self.l) + jval*(self.l-1)/(2*self.l*lambda_x)
				self.intercal2 = pow(1/(2*self.l) + jval*(self.l-1)/(2*self.l*lambda_x),2) - jval/(self.l*lambda_x)
				self.rhointercal+=[(self.intercal1,self.intercal2)]
			else:
				print('lambda_x cannot be 0')
		for x,y in self.rhointercal:
			self.inter_y=sqrt(0 if y < 0.000001 else y)
			self.rho_l += [x - self.inter_y] 
			self.rho_r += [x + self.inter_y]
		self.plot_scat(self.rh.scat_step,self.rh.scat_cross_step)
		return sum(self.scat_ys)/len(self.scat_ys)


	def trans_func(self, point):
		if point >= glo_var.alpha_star:
			return glo_var.beta_star
		self.B = point*(self.lambda_0 - point)/(self.lambda_0 + (glo_var.l -1) * point)
		self.trans_b = - self.lambda_1 +(glo_var.l-1)*self.B
		self.trans_intercal = 0 if pow(self.trans_b,2) - 4*self.B*self.lambda_1 < 0.00001 else sqrt(pow(self.trans_b,2) - 4*self.B*self.lambda_1)
		self.trans = (-self.trans_b - self.trans_intercal)/2
		return self.trans

	def getscatarray(self,array,step):
		return array[::step]
	
	def check_two_mins(self):
		self.min_location_1 = -1
		self.min_location_2 = -1
		self.max_location_1 = -1
		counter=0
		num=0
		for i in self.lambdas_ys:
			if i == self.lambda_min:
				if self.min_location_1 != -1 :
					self.min_location_2 = counter
					num += 1
				else:
					self.min_location_1 = counter
					num += 1
			counter +=1;
		if self.min_location_2 != -1:
			local_max_1 = max(self.lambdas_ys[self.min_location_1:self.min_location_2 + 1])
			counter = 0
			for i in self.lambdas_ys[self.min_location_1:self.min_location_2 + 1]:
				if i == local_max_1:
					self.max_location_1 = self.min_location_1 + counter
				counter +=1
		if self.min_location_2 - self.min_location_1 == 1:
			num = 1
		return num

	def plot_scat(self,steps,cross_steps):
		self.num_mins = self.check_two_mins()
		if self.region == 3:
			if self.num_mins == 1 :
				self.scat_xs = self.getscatarray(self.rh.lambdas_xs[:self.min_location_1*self.xperlambdas],steps) + self.getscatarray(self.rh.lambdas_xs[self.min_location_1*self.xperlambdas:],steps)
				self.scat_ys = self.getscatarray(self.rho_r[:self.min_location_1*self.xperlambdas],steps) + self.getscatarray(self.rho_l[self.min_location_1*self.xperlambdas:],steps)
			elif self.num_mins == 2:
				self.scat_xs =  self.getscatarray(self.rh.lambdas_xs[:self.min_location_1*self.xperlambdas],steps) \
								+ self.getscatarray(self.rh.lambdas_xs[self.min_location_1*self.xperlambdas:self.max_location_1*self.xperlambdas-cross_steps],steps) \
								+ self.getscatarray(self.rh.lambdas_xs[self.max_location_1*self.xperlambdas-cross_steps:self.max_location_1*self.xperlambdas+cross_steps + 1],1) \
								+ self.getscatarray(self.rh.lambdas_xs[self.max_location_1*self.xperlambdas+cross_steps + 1:self.min_location_2*self.xperlambdas],steps) \
								+ self.getscatarray(self.rh.lambdas_xs[self.min_location_2*self.xperlambdas:],steps)
				self.scat_ys = self.getscatarray(self.rho_r[:self.min_location_1*self.xperlambdas],steps) \
								+ self.getscatarray(self.rho_l[self.min_location_1*self.xperlambdas:self.max_location_1*self.xperlambdas-cross_steps],steps) \
								+ self.get_cross(self.rho_r,self.rho_l,self.max_location_1*self.xperlambdas-cross_steps ,self.max_location_1*self.xperlambdas+cross_steps + 1,cross_steps*2) \
								+ self.getscatarray(self.rho_r[self.max_location_1*self.xperlambdas+cross_steps + 1:self.min_location_2*self.xperlambdas],steps) \
								+ self.getscatarray(self.rho_l[self.min_location_2*self.xperlambdas:], steps)

	#  what if num_mins is 3?
		elif self.region == 2:
			self.scat_xs = self.getscatarray(self.rh.lambdas_xs,steps)
			self.scat_ys = self.getscatarray(self.rho_r,steps)

		else:
			self.scat_xs = self.getscatarray(self.rh.lambdas_xs,steps)
			self.scat_ys = self.getscatarray(self.rho_l,steps)



	def plot_sum_rho(self):
		self.basic_1 = 1/(2*glo_var.l)
		self.basic_2 = (glo_var.l - 1)/pow((1+sqrt(glo_var.l)),2)
		# self.intercal = 1/(2*glo_var.l) + self.js()
		self.inter_sum = 0
		self.rho_sum=[]
		self.domain = np.concatenate((self.beta_pre,self.betas_post))
		for i in self.domain:
			self.j_inter=self.js(i,glo_var.beta)
			if self.region == 1:
				for j in range(self.rh.min_location_1):
					self.inter_cal =  pow((self.basic_1 + self.j_inter*self.basic_2),2) - self.j_inter/(glo_var.l*self.lambdas_ys[j]) 
					self.inter_sum -=  0 if self.inter_cal < 0.0001 else sqrt(self.inter_cal) 
				
				for q in range(self.rh.min_location_1,glo_var.lambdas_degree):
					self.inter_cal =  pow((self.basic_1 + self.j_inter*self.basic_2),2) - self.j_inter/(glo_var.l*self.lambdas_ys[q]) 
					self.inter_sum +=  0 if self.inter_cal < 0.0001 else sqrt(self.inter_cal) 
			else :
				for j in range(self.rh.min_location_1):
					self.inter_cal =  pow((self.basic_1 + self.j_inter*self.basic_2),2) - self.j_inter/(glo_var.l*self.lambdas_ys[j]) 
					self.inter_sum +=  0 if self.inter_cal < 0.0001 else sqrt(self.inter_cal) 
				
				for q in range(self.rh.min_location_1,glo_var.lambdas_degree):
					self.inter_cal =  pow((self.basic_1 + self.j_inter*self.basic_2),2) - self.j_inter/(glo_var.l*self.lambdas_ys[q]) 
					self.inter_sum -=  0 if self.inter_cal < 0.0001 else sqrt(self.inter_cal)

			self.rho_sum += [self.basic_1 + self.j_inter*self.basic_2 +pow(-1,self.region == 1) * self.inter_sum/glo_var.lambdas_degree]
			self.inter_sum = 0

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
			if alpha <= self.alpha_star:
				self.jl = alpha*(self.lambda_0-alpha)/(self.lambda_0+(self.l-1)*alpha)
				self.jr = beta*(self.lambda_1-beta)/(self.lambda_1+(self.l-1)*beta)
				if self.jl < self.jr:
					self.region = 1 
					return self.jl
				else :
					self.region = 2
					return self.jr
			else :
				self.region = 2
				return beta*(self.lambda_1-beta)/(self.lambda_1+(self.l-1)*beta)
