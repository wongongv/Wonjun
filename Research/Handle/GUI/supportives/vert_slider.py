import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D
from math import sqrt
from matplotlib.widgets import AxesWidget
import six
import pdb
import glo_var

class VertSlider(AxesWidget):
	"""
	A slider representing a floating point range.

	For the slider to remain responsive you must maintain a
	reference to it.

	The following attributes are defined
	  *ax*        : the slider :class:`matplotlib.axes.Axes` instance

	  *val*       : the current slider value

	  *hline*     : a :class:`matplotlib.lines.Line2D` instance
					 representing the initial value of the slider

	  *poly*      : A :class:`matplotlib.patches.Polygon` instance
					 which is the slider knob

	  *valfmt*    : the format string for formatting the slider text

	  *label*     : a :class:`matplotlib.text.Text` instance
					 for the slider label

	  *closedmin* : whether the slider is closed on the minimum

	  *closedmax* : whether the slider is closed on the maximum

	  *slidermin* : another slider - if not *None*, this slider must be
					 greater than *slidermin*

	  *slidermax* : another slider - if not *None*, this slider must be
					 less than *slidermax*

	  *dragging*  : allow for mouse dragging on slider

	Call :meth:`on_changed` to connect to the slider event
	"""
	def __init__(self, ax, label, valmin, valmax, number, valinit=0.8, valfmt='%1.2f',
				 closedmin=True, closedmax=True, slidermin=None,
				 slidermax=None, dragging=True, **kwargs):
		"""
		Create a slider from *valmin* to *valmax* in axes *ax*.

		Additional kwargs are passed on to ``self.poly`` which is the
		:class:`matplotlib.patches.Rectangle` which draws the slider
		knob.  See the :class:`matplotlib.patches.Rectangle` documentation
		valid property names (e.g., *facecolor*, *edgecolor*, *alpha*, ...).

		Parameters
		----------
		ax : Axes
			The Axes to put the slider in

		label : str
			Slider label

		valmin : float
			The minimum value of the slider

		valmax : float
			The maximum value of the slider

		valinit : float
			The slider initial position

		label : str
			The slider label

		valfmt : str
			Used to format the slider value, fprint format string

		closedmin : bool
			Indicate whether the slider interval is closed on the bottom

		closedmax : bool
			Indicate whether the slider interval is closed on the top

		slidermin : Slider or None
			Do not allow the current slider to have a value less than
			`slidermin`

		slidermax : Slider or None
			Do not allow the current slider to have a value greater than
			`slidermax`


		dragging : bool
			if the slider can be dragged by the mouse

		"""
		AxesWidget.__init__(self, ax)

		self.valmin = valmin
		self.valmax = valmax
		self.val = valinit
		self.valinit = valinit
		self.poly = ax.axhspan(valmin, valinit, 0, 1, **kwargs)

		# self.hline = ax.axhline(valinit, 0, 1, color='r', lw=1)
		self.number=number
		self.valfmt = valfmt
		ax.set_xticks([])
		ax.set_ylim((valmin, valmax))
		ax.set_yticks([])
		ax.set_navigate(False)

		self.connect_event('button_press_event', self._update)
		self.connect_event('button_release_event', self._update)
		if dragging:
			self.connect_event('motion_notify_event', self._update)
		self.label = ax.text(0.5, 1.2, label, transform=ax.transAxes,
							 verticalalignment='center',
							 horizontalalignment='center')

		self.valtext = ax.text(0.5, -0.3, valfmt % valinit,
							   transform=ax.transAxes,
							   verticalalignment='center',
							   horizontalalignment='center')

		self.cnt = 0
		self.observers = {}

		self.closedmin = closedmin
		self.closedmax = closedmax
		self.slidermin = slidermin
		self.slidermax = slidermax
		self.drag_active = False



	def _update(self, event):
		"""update the slider position"""
		if self.ignore(event):
			return

		if event.button != 1:
			return

		if event.name == 'button_press_event' and event.inaxes == self.ax:
			self.drag_active = True
			event.canvas.grab_mouse(self.ax)

		if not self.drag_active:
			return

		elif ((event.name == 'button_release_event') or
			  (event.name == 'button_press_event' and
			   event.inaxes != self.ax)):
			self.drag_active = False
			event.canvas.release_mouse(self.ax)
			return

		val = event.ydata
		if val <= self.valmin:
			if not self.closedmin:
				return
			val = self.valmin
		elif val >= self.valmax:
			if not self.closedmax:
				return
			val = self.valmax

		if self.slidermin is not None and val <= self.slidermin.val:
			if not self.closedmin:
				return
			val = self.slidermin.val

		if self.slidermax is not None and val >= self.slidermax.val:
			if not self.closedmax:
				return
			val = self.slidermax.val

		self.set_val(val)
		if (self.number == glo_var.lambdas_degree) :
			glo_var.alpha = val
			self.rho.update()
		elif (self.number == glo_var.lambdas_degree + 1) :
			glo_var.beta = val
			self.rho.update()
		else:
			glo_var.lambdas[self.number][1] = val
			if self.lambda_poly != None:
				self.lambda_poly.update()

	def update_ab(self,val):
		self.val = val
		self.valtext.set_text(self.valfmt % val)
		self.ax.figure.canvas.draw_idle()



	def set_val(self, val):
		xy = self.poly.xy
		xy[1] = 0, val
		xy[2] = 1, val
		self.poly.xy = xy
		self.valtext.set_text(self.valfmt % val)
		if self.drawon:
			self.ax.figure.canvas.draw_idle()
		self.val = val
		if not self.eventson:
			return
		for cid, func in six.iteritems(self.observers):
			func(val)

	def on_changed(self, func):
		"""
		When the slider value is changed, call *func* with the new
		slider position

		A connection id is returned which can be used to disconnect
		"""
		cid = self.cnt
		self.observers[cid] = func
		self.cnt += 1
		return cid

	def disconnect(self, cid):
		"""remove the observer with connection id *cid*"""
		try:
			del self.observers[cid]
		except KeyError:
			pass

	def reset(self):
		"""reset the slider to the initial value if needed"""
		if (self.val != self.valinit):
			self.set_val(self.valinit)
	def receive(self,lambda_poly,rho):
		self.lambda_poly = lambda_poly
		self.rho = rho
	def delete(self,todelete):
		if todelete == 'lambda_poly':
			self.lambda_poly = None
		if todelete == 'rho':
			self.rho = None
class make_vs :
	def __init__(self,fig):
		self.fig = fig
		self.vaxes=[self.fig.add_subplot(40,1,6+i) for i in range(glo_var.lambdas_degree + 2)]
		[self.vaxes[i].set_position([0.35+0.02*(i+1),0.15,0.01,0.1],which='both') for i in range(glo_var.lambdas_degree)]
		self.vaxes[glo_var.lambdas_degree].set_position([0.35,0.15,0.01,0.1], which = 'both')
		self.vaxes[glo_var.lambdas_degree + 1].set_position([0.35 + (glo_var.lambdas_degree + 1)*0.02,0.15,0.01,0.1], which = 'both')

		self.vslides = [VertSlider(self.vaxes[i],r'$\lambda${}'.format(i),0,1,i) for i in range(glo_var.lambdas_degree)]
		self.vslides += [VertSlider(self.vaxes[glo_var.lambdas_degree],r'$\alpha$',0,1,glo_var.lambdas_degree,glo_var.alpha)] #alpha
		self.vslides += [VertSlider(self.vaxes[glo_var.lambdas_degree + 1],r'$\beta$',0,1,glo_var.lambdas_degree + 1, glo_var.beta)] #beta
		#  think about let numer of alpha and beta be 1000 and 1001 for later use(adding switches)
		#  when you add new thing, slice vslides and put it in front of alpha

		for j in range(glo_var.lambdas_degree):
			glo_var.lambdas[j] = [(j)/(glo_var.lambdas_degree - 1), self.vslides[j].val] 

	def receive(self, lambda_poly, rho):
		[self.vslides[i].receive(lambda_poly, rho) for i in range(glo_var.lambdas_degree)]			

	def delete(self,todelete):
		[self.vslides[i].delete(todelete) for i in range(len(self.vslides))]