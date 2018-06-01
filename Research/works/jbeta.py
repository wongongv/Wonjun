
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
from math import sqrt

class jbeta:
# dock version
	def __init__(self, dbeta,rh):


		self.dbeta = dbeta
		self.p4main = glo_var.MyPW(x="\u03b2",y1="J",y2= "\u27e8\U0001d780\u27e9", set_range = self.set_range)
		# self.p4main._rescale = self.set_range
		self.p4 = self.p4main.plotItem
		self.viewbox = self.p4.getViewBox()
		# self.viewbox.setBackgroundColor('w')
		self.item = self.p4

		self.p4main.tempplotitem = pg.PlotItem()
		self.p4_2 = self.p4main.tempplotitem.vb

		self.p4.setLabel('left',"J",**glo_var.labelstyle)

		self.p4.setLabel('bottom',"\u03b2",**glo_var.labelstyle)

		self.p4.setLabel('right',"\u27e8\U0001d780\u27e9",**glo_var.labelstyle)
		# self.p4main.set_range = self.set_range

		self.rh=rh
		self.rho_dash = pg.mkPen(color=(16,52,166),width=glo_var.line_width,style=QtCore.Qt.DashLine)
		self.dash = pg.mkPen('r',width=glo_var.line_width,style=QtCore.Qt.DashLine)
		self.jpen = pg.mkPen('k',width=glo_var.line_width)
		self.beta_pen = pg.mkPen('k',width=glo_var.line_width)

		self.p4.addLegend = glo_var.myaddLegend
		self.p4.addLegend(self.p4,offset=(20,20))

		self.p4.showAxis('right')
		self.p4.scene().addItem(self.p4_2)
		self.p4.getAxis('right').linkToView(self.p4_2)
		self.p4_2.setXLink(self.p4)
		self.p4_2.setBackgroundColor('w')
		
		self.p4main.coordinate_label = QtGui.QLabel()
		self.frame = glo_var.setframe(self.p4main, width = 1, coordinate_label = self.p4main.coordinate_label)
		self.dbeta.addWidget(self.frame)

		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax = 1, yMax = 1)
		self.p4_2.setLimits(xMin = 0, yMin = 0, xMax = 1, yMax = 1)

		self.p4.vb.sigResized.connect(self.updateview)
		
		self.update()
		self.legend()

	def set_range(self):
		self.uplim1 = min(self.jpost * 1.3, 1)
		self.lolim1 = 0
		# self.viewbox.setRange(xRange=[0,self.vlim],yRange=[self.lolim1,self.uplim1],padding =0)
		self.uplim2 = min(1, max(max(self.rho_avg_pre)*1.4,max(self.rho_avg_post)*1.4))
		self.lolim2 = max(0, min(min(self.rho_avg_pre)*0.6,min(self.rho_avg_post)*0.6))
		# self.p4_2.setRange(xRange=[0,self.vlim],yRange=[self.lolim2,self.uplim2], padding = 0)

		self.viewbox.setRange(xRange=[0,3*self.trans_point],yRange=[self.lolim1,self.uplim1],padding =0)
		self.p4_2.setRange(xRange=[0,3*self.trans_point],yRange=[self.lolim2,self.uplim2], padding = 0)

	def update(self):
		self.p4.clear()
		self.p4_2.clear()
		self.value_declaration()
		self.vlim = 1/pow(1+sqrt(glo_var.l),2)


		self.trans_point = self.trans_func(glo_var.alpha)
		

		self.betas_pre = np.linspace(0,self.trans_point - 0.000001,20)
		# # explain here in the meeting
		# self.betas_to_add_pre = np.array([self.trans_point-0.000001]) 
		# self.betas_to_add_post = np.array([self.trans_point+0.000001]) 
		
		# self.betas_pre = np.concatenate((self.betas_pre_pre[:-1],self.betas_to_add_pre))
		self.betas_post = np.array([self.trans_point+0.000001, 1])

		# self.domain = np.concatenate((self.betas_pre,self.betas_post))


		self.j_r_values=np.array([i*(self.lambda_1-i)/(self.lambda_1 + (glo_var.l-1)*i) for i in self.betas_pre])
		
		self.rho_avg_pre = []
		self.rho_avg_post = []

		for i in self.betas_pre:
			self.rho_avg_pre += [self.cal_rho(self.js(glo_var.alpha,i))]
		for i in self.betas_post:
			self.rho_avg_post += [self.cal_rho(self.js(glo_var.alpha,i))]

		if self.betacheck == 1:
			self.text = pg.TextItem(html='<span style="color: #1034A6; font-size: 16pt;">\u03b2</span></div>', anchor=(0.5,1.5))
			self.p4.addItem(self.text)
			self.arrow = pg.ArrowItem(pos=(glo_var.beta,0),angle=-90)
			self.p4.addItem(self.arrow)
			self.betacheck=0
		self.text.setPos(glo_var.beta,0)
		self.arrow.setPos(glo_var.beta,0)

		# minused 0.00000001 since it is not working
		
		self.p4.plot(self.betas_pre,self.j_r_values, pen = self.jpen)

		# Can alpha_star be 0? then I need to add conner case
		if glo_var.alpha >= glo_var.alpha_star:
			self.jpost= self.j_c
		else:
			self.jpost= self.j_l
		self.p4.plot([self.trans_point,1],[self.jpost,self.jpost], pen = self.jpen)
		self.trans_line = self.p4.plot([self.trans_point,self.trans_point],[0,1],pen=self.dash)
		self.make_right_axis()
		self.set_range()

	def legend(self):
		self.p4.plot(pen=self.jpen, name='J')
		self.p4.plot(pen=self.rho_dash, name='\u27e8\U0001d780\u27e9')

	def updateview(self):
		self.p4_2.setGeometry(self.p4.vb.sceneBoundingRect())
		self.p4_2.linkedViewChanged(self.p4.vb, self.p4_2.XAxis)
		
	def make_right_axis(self):
		# self.p4.plot(self.domain,self.rho_avg,pen=self.rho_dash)
		self.p4_2.addItem(pg.PlotCurveItem(self.betas_pre,self.rho_avg_pre,pen=self.rho_dash))
		self.p4_2.addItem(pg.PlotCurveItem(self.betas_post,self.rho_avg_post,pen=self.rho_dash))

		# self.p4.plot(self.betas_pre,self.rho_avg_pre,pen=self.rho_dash)
		# self.p4.plot(self.betas_post,self.rho_avg_post,pen=self.rho_dash)

	def value_declaration(self):
		self.lambdas_xs, self.lambdas_ys = zip(*sorted(glo_var.lambdas))
		self.lambda_min = min(self.lambdas_ys)
		self.lambda_0 = glo_var.lambdas[0][1]
		self.lambda_1 = glo_var.lambdas[-1][1]
		self.j_c = self.lambda_min/pow(1 + sqrt(glo_var.l),2)
		self.j_l = glo_var.alpha*(self.lambda_0-glo_var.alpha)/(self.lambda_0 + (glo_var.l-1)*glo_var.alpha)
		self.alpha_star = glo_var.alpha_star
		self.beta_star = glo_var.beta_star
		self.alpha=glo_var.alpha
		self.beta=glo_var.beta
		self.l=glo_var.l
		self.betacheck=1

	def cal_rho(self,jval):
		self.xperlambdas = round(150/glo_var.lambdas_degree)
		self.rhointercal=[]
		self.rho_l = []
		self.rho_r = []
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


	def plot_sum_rho(self):
		self.basic_1 = 1/(2*glo_var.l)
		self.basic_2 = (glo_var.l - 1)/pow((1+sqrt(glo_var.l)),2)
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

	def get_cross(self,upper_array,lower_array,start_position,end_position,steps):
		step_val=(upper_array[end_position] - lower_array[start_position])/steps
		self.cross_array=[]
		for i in range(steps + 1):
			self.cross_array += [lower_array[start_position] + i*step_val]
		return self.cross_array