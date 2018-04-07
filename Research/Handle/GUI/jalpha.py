from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt
import pdb
from scipy.interpolate import interp1d

class jalpha:
	def __init__(self, win, rh):
		self.win = win
		self.rh=rh
		self.p3 = self.win.addPlot(title = '\u03B1')
		self.viewbox=self.p3.getViewBox()
		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax = 1, yMax = 1)
		self.viewbox.setRange(xRange=[0,1],yRange=[0,1],padding =0)
		# self.ax.set_facecolor()
		self.p3.addLegend()
		self.update()
		self.legend()
		self.p3_2 = self.p3.getViewBox()
		self.p3.showAxis('right')
		self.p3.scene().addItem(self.p3_2)

	def update(self):
		self.p3.clear()
		self.value_declaration()


		self.trans_point = self.trans_func(glo_var.beta)
		
		self.alphas_pre_pre = np.linspace(0,self.trans_point,20)
		# explain here in the meeting
		self.alphas_to_add = np.array([self.trans_point-0.000001, self.trans_point, self.trans_point+0.000001]) 
		self.alphas_pre = np.concatenate((self.alphas_pre_pre[:-1],self.alphas_to_add))
		#  do I need to make sure that the last element of alphas_pre does not exceed first element of self.alphas_post? may be no?
		self.alphas_post=np.array([1])
		# self.alphas_post = np.linspace(self.trans_point,1,20)[1:]
		self.domain = np.concatenate((self.alphas_pre,self.alphas_post))
		self.j_l_values=np.array([i*(self.lambda_0-i)/(self.lambda_0 + (glo_var.l-1)*i) for i in self.alphas_pre])
		
		self.rho_avg = []
		for i in self.domain:
			self.rho_avg += [self.cal_rho(self.js(i,glo_var.beta))]

		self.j_l_g = interp1d(self.alphas_pre,self.j_l_values)


		self.num=30
		self.xs =np.linspace(0,self.trans_point, self.num)
	
		# minused 0.00000001 since it is not working
		
		self.p3.plot(self.alphas_pre,self.j_l_values)

		self.dash = pg.mkPen('y',style=QtCore.Qt.DashLine)

		# Can alpha_star be 0? then I need to add conner case
		if glo_var.beta >= glo_var.beta_star:
			self.jpost= self.j_c
		else:
			self.jpost= self.j_r
		
		self.p3.plot([self.trans_point,1],[self.jpost,self.jpost])
		self.trans_line = self.p3.plot([self.trans_point,self.trans_point],[0,1],pen=self.dash)
		self.alpha_line = self.p3.plot([glo_var.alpha,glo_var.alpha],[0,1])
		self.plot_rho()
		# self.plot_sum_rho()
		# self.sum_rho_dash = pg.mkPen('r',style=QtCore.Qt.DashLine)
		# self.p3.plot(self.domain ,self.rho_sum, pen=self.sum_rho_dash)
	def legend(self):
		self.p3.plot(pen='w', name='J')
		self.p3.plot(pen=self.rho_dash, name='\u03c1')

	def plot_rho(self):
		self.rho_dash = pg.mkPen('r',style=QtCore.Qt.DashLine)
		self.p3.plot(self.domain,self.rho_avg,pen=self.rho_dash)	


	def trans_func(self, point):
		if point >= glo_var.beta_star:
			return glo_var.alpha_star
		self.B = point*(self.lambda_1 - point)/(self.lambda_1 + (glo_var.l -1) * point)
		self.trans_b = - self.lambda_0 +(glo_var.l-1)*self.B
		self.trans_intercal = 0 if pow(self.trans_b,2) - 4*self.B*self.lambda_0 < 0.00001 else sqrt(pow(self.trans_b,2) - 4*self.B*self.lambda_0)
		self.trans = (-self.trans_b - self.trans_intercal)/2
		return self.trans

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
		self.plot_scat(self.rh.scat_step)
		return sum(self.scat_ys)/len(self.scat_ys)

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

	def plot_scat(self,steps):
		self.num_mins = self.check_two_mins()
		self.scat_ys = []
		self.scat_xs = []
		if self.region == 3:
			if self.num_mins > 1:
				self.index1 = self.minlocation[0]*self.xperlambdas
				self.scat_xs += self.getscatarray(self.rh.lambdas_xval[:self.index1],steps)
				self.scat_ys += self.getscatarray(self.rho_r[:self.index1],steps)
				for i in range(1, self.num_mins):
					self.index1 = self.minlocation[i - 1]*self.xperlambdas
					self.index2 = self.minlocation[i]*self.xperlambdas
					self.indexmax = self.maxlocation[i - 1]*self.xperlambdas
					self.scat_xs += self.getscatarray(self.rh.lambdas_xval[self.index1:self.indexmax],steps)
					self.scat_ys += self.getscatarray(self.rho_l[self.index1:self.indexmax],steps)
					self.scat_xs += self.getscatarray(self.rh.lambdas_xval[self.indexmax:self.index2],steps)
					self.scat_ys += self.getscatarray(self.rho_r[self.indexmax:self.index2],steps)
				self.scat_xs += self.getscatarray(self.rh.lambdas_xval[self.index2:],steps)
				self.scat_ys += self.getscatarray(self.rho_l[self.index2:],steps)

			else :
				self.index = self.minlocation[0]*self.xperlambdas
				self.scat_xs += self.getscatarray(self.rh.lambdas_xval[:self.index],steps) + self.getscatarray(self.rh.lambdas_xval[self.index:],steps)
				self.scat_ys += self.getscatarray(self.rho_r[:self.index],steps) + self.getscatarray(self.rho_l[self.index:],steps)

		elif self.region == 2:
			self.scat_xs = self.getscatarray(self.rh.lambdas_xval,steps)
			self.scat_ys = self.getscatarray(self.rho_r,steps)
		else:
			self.scat_xs = self.getscatarray(self.rh.lambdas_xval,steps)
			self.scat_ys = self.getscatarray(self.rho_l,steps)



	def getscatarray(self,array,step):
		return array[::step]

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
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas.values()))
		self.lambda_min = min(self.lambdas_ys)
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[glo_var.lambdas_degree - 1][1]
		self.j_c = self.lambda_min/pow(1 + sqrt(glo_var.l),2)
		self.j_r = glo_var.beta*(self.lambda_1-glo_var.beta)/(self.lambda_1 + (glo_var.l-1)*glo_var.beta)
		self.alpha_star = glo_var.alpha_star
		self.beta_star = glo_var.beta_star
		self.alpha=glo_var.alpha
		self.beta=glo_var.beta
		self.l=glo_var.l





	def plot_sum_rho(self):
		self.basic_1 = 1/(2*glo_var.l)
		self.basic_2 = (glo_var.l - 1)/pow((1+sqrt(glo_var.l)),2)
		# self.intercal = 1/(2*glo_var.l) + self.js()
		self.inter_sum = 0
		self.rho_sum=[]
		self.domain = np.concatenate((self.alphas_pre,self.alphas_post))
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
			
	def get_cross(self,upper_array,lower_array,start_position,end_position,steps):
		step_val=(upper_array[end_position] - lower_array[start_position])/steps
		self.cross_array=[]
		for i in range(steps + 1):
			self.cross_array += [lower_array[start_position] + i*step_val]
		return self.cross_array