
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import glo_var
import pdb

class slide:
	def __init__(self,win):
		self.win=win
		self.p5 = self.win.addPlot(title='alpha, beta')
		self.viewbox=self.p5.getViewBox()
		self.viewbox.setLimits(xMin = 0, yMin = 0, xMax = 1, yMax = 1)
		self.app = pg.mkQApp()
		# self.p5.plot(x=(0.5), y=(0.5), symbolBrush='r', symbolPen='w')
		# cross hair
		self.vLine = pg.InfiniteLine(angle=90, movable=False)
		self.hLine = pg.InfiniteLine(angle=0, movable=False)
		self.p5.addItem(self.vLine, ignoreBounds=True)
		self.p5.addItem(self.hLine, ignoreBounds=True)
		self.vb = self.p5.vb
		self.p5.setMouseEnabled(x=False, y=False)
		
	def mouseMoved(evt):
		self.pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.p5.sceneBoundingRect().contains(self.pos):
			self.mousePoint = self.vb.mapSceneToView(self.pos)
			self.index = int(self.mousePoint.x())
			if self.index >= 0 and self.index <= 1:
				label.setText("<span style='font-size: 12pt'>alpha=%0.1f,   <span style='color: red'>beta=%0.1f</span>" % (mousePoint.x(), mousePoint.y()))
			self.vLine.setPos(self.mousePoint.x())
			self.hLine.setPos(self.mousePoint.y())
			self.proxy = pg.SignalProxy(self.p5.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)


	
# class slide:
# 	def __init__(self, fig, axes, vs_alpha, vs_beta, rho):
# # start
# 		self.fig=fig
# 		self.axes = axes
# 		self.axes.set_xlim(0, 1)
# 		self.axes.set_ylim(0, 1)
# 		self._dragging_point = None
# 		self.points = {0.5:0.5}
# 		self.initial_point, =self.axes.plot(0.5,0.5,"b", marker="o", markersize=10) 

# 		self.vs_alpha = vs_alpha
# 		self.vs_beta = vs_beta

# 		self.line_1 = Line2D([0,glo_var.alpha_star], [0,glo_var.beta_star])
# 		self.line_2 = Line2D([glo_var.alpha_star,1], [glo_var.beta_star],glo_var.beta_star)
# 		self.line_3 = Line2D([glo_var.alpha_star,glo_var.alpha_star], [glo_var.beta_star,1])
# 		self.axes.add_line(self.line_1)
# 		self.axes.add_line(self.line_2)
# 		self.axes.add_line(self.line_3)

# 		self.rho = rho
# 		self._init_plot()

# 	def _init_plot(self):
# 		# self.draw_rho()
# 		self.fig.canvas.mpl_connect('button_press_event', self._on_click)
# 		self.fig.canvas.mpl_connect('button_release_event', self._on_release)
# 		self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)



# 	def _remove_point(self, x, _):
# 		if x in self.points:
# 			self.points.pop(x)

# 	def pol_remove_point(self, x, _):
# 		if x in self.pol_points:
# 			self.pol_points.pop(x)

# 	def update_variables(self,al,be):
# 		self.alpha=al
# 		self.beta=be

# 	def update_result(self):
# 		x, y = zip(*sorted(self.points.items()))
# 		new_x=x[0]
# 		new_y=y[0]
# 		self.update_variables(new_x,new_y)
# 		glo_var.alpha = self.alpha
# 		glo_var.beta = self.beta
# 		self.vs_alpha.update_ab(self.alpha)
# 		self.vs_beta.update_ab(self.beta)
# 		self.rho.update()
	   

# 	def _update_plot(self):

# 		x, y = zip(*sorted(self.points.items()))
# 		# Add new plot
# 		# Update current plot
# 		self.initial_point.set_data(x, y)
# 		self.fig.canvas.draw()
		
# 	def _find_neighbor_point(self, event):
# 		u""" Find point around mouse position
# 		:rtype: ((int, int)|None)
# 		:return: (x, y) if there are any point around mouse else None
# 		"""
# 		distance_threshold = 3.0
# 		nearest_point = None
# 		min_distance = math.sqrt(2 * (100 ** 2))
# 		for x, y in self.points.items():
# 			distance = math.hypot(event.xdata - x, event.ydata - y)
# 			if distance < min_distance:
# 				min_distance = distance
# 				nearest_point = (x, y)
# 		if min_distance < distance_threshold:
# 			return nearest_point
# 		return None
# 	def pol_find_neighbor_point(self, event):
# 		u""" Find point around mouse position
# 		:rtype: ((int, int)|None)
# 		:return: (x, y) if there are any point around mouse else None
# 		"""
# 		distance_threshold = 3.0
# 		nearest_point = None
# 		min_distance = math.sqrt(2 * (100 ** 2))
# 		for x, y in self.pol_points.items():
# 			distance = math.hypot(event.xdata - x, event.ydata - y)
# 			if distance < min_distance:
# 				min_distance = distance
# 				nearest_point = (x, y)
# 		if min_distance < distance_threshold:
# 			return nearest_point
# 		return None

# 	def _add_point(self, x, y=None):
# 		if self.points:
# 			return
# 		if isinstance(x, MouseEvent):
# 			x, y = x.xdata, x.ydata
# 		self.points[x] = y
# 		return x, y

# 	def pol_add_point(self, x, y=None):
# 		if self.pol_points:
# 			return
# 		if isinstance(x, MouseEvent):
# 			print('yea')
# 			x, y = x.xdata, x.ydata
# 		print(x,y)
# 		self.pol_points[x] = y
# 		print(self.pol_points)
# 		return x, y

# 	def _on_click(self, event):
# 		u""" callback method for mouse click event
# 		:type event: MouseEvent
# 		"""
# 		# left click
# 		if event.button == 1 and event.inaxes in [self.axes]:
# 			point = self._find_neighbor_point(event)
# 			if point:
# 				self._dragging_point = point
# 		self._update_plot()
# 		self.update_result()
			
# 	def _on_release(self, event):
# 		u""" callback method for mouse release event
# 		:type event: MouseEvent
# 		"""
# 		if event.button == 1 and event.inaxes in [self.axes] and self._dragging_point:
# 			self._add_point(event)
# 			self._dragging_point = None
# 			self._update_plot()

# 	def _on_motion(self, event):
# 		u""" callback method for mouse motion event
# 		:type event: MouseEvent
# 		"""
# 		if event.inaxes in [self.axes]:
# 			if not self._dragging_point:
# 				return
# 			self._remove_point(*self._dragging_point)
# 			self._dragging_point = self._add_point(event)
# 			self._update_plot()
# 			self.update_result()

# class make_slide:
# 	def __init__(self, fig, vs_alpha, vs_beta, rho):
# 		self.fig = fig
# 		self.slide_axes = self.fig.add_subplot(40,1,4)
# 		self.slide_axes.set_position([0.1,0.1,0.2,0.2],which='both')
# 		self.cursor2 = Cursor(self.slide_axes, useblit=True, color='red', linewidth=2)
# 		self.slider = slide(self.fig,self.slide_axes, vs_alpha, vs_beta, rho)
