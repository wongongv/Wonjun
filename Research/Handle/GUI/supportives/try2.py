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
import vert_slider
# phase diagram, branches, lambda, alpha-beta switch, lambda-switch, HD-MC, LD-MC

fig=plt.figure()
ax=fig.add_subplot(35,1,1)
ax.set_position([0.1,0.6,0.1,0.1],which='both')
ax.set_ylim((0,1))
# ax.plot(left=0.25, bottom=0.25)
# ax.bar()
t = np.arange(0.0, 1.0, 0.001)

#two parameters
Lambda = 1
J = 1
#result
x=['J','Lambda']
y=[1,1] #initial value of start

rect = plt.bar(x,y) # this should be the resulting data
# plt.axis([0, 1, -10, 10])


# new=figure.add_subplot(35,1,11)
# new.set_position([0.1,0.1,0.1,0.1],which='both')
# t=np.arange(0.0, 1.0, 0.001)
# s=t
# line=Line2D(t,s)
# new.add_line(line)

class slideandpol:
    def __init__(self,fig,axes,lambdas):

# variables
        self.lambda_0=lambdas[0]
        self.lambda_1=lambdas[24]
        self.lambda_min=min(lambdas)
        self.l=3
        self.alpha=0.5
        self.beta=0.5
        self.intercall=pow(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_0*self.lambda_min/pow(1+sqrt(self.l),2)
        self.intercalr=pow(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_1*self.lambda_min/pow(1+sqrt(self.l),2)
        self.alpha_star=0.5*(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt( 0 if self.intercall < 0.0000001 else self.intercall ))
        self.beta_star=0.5*(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt(0 if self.intercalr < 0.0000001 else self.intercalr))
        self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
        self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
        self.rho_l=[]
        self.rho_r=[]
        self.lambdas=lambdas
# variable reference
        self.lambda_0_ref=self.lambda_0
        self.lambda_1_ref=self.lambda_1
        self.lambda_min_ref=self.lambda_min
# start
        self.fig=fig
        self.axes = axes
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self._dragging_point = None
        self.points = {0.5:0.5}
        self.initial_point, =self.axes.plot(0.5,0.5,"b", marker="o", markersize=10) 
        self.line_1 = Line2D([0,self.alpha_star], [0,self.beta_star])
        self.line_2 = Line2D([self.alpha_star,1], [self.beta_star],self.beta_star)
        self.line_3 = Line2D([self.alpha_star,self.alpha_star], [self.beta_star,1])
        self.axes.add_line(self.line_1)
        self.axes.add_line(self.line_2)
        self.axes.add_line(self.line_3)
# rho
        self.rho_l=[1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x) - sqrt(pow(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),2) - self.j_l/(self.l*lambda_x)) for lambda_x in self.lambdas]
        self.rho_r=[1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x) + sqrt(pow(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),2) - self.j_r/(self.l*lambda_x)) for lambda_x in self.lambdas]
        self.rho_axes=self.fig.add_subplot(35,1,5)
        self.rho_axes.set_position([0.1,0.4,0.3,0.2],which='both')
        self.xs=np.linspace(0,1,25)
        self.linel=Line2D(self.xs, self.rho_l)
        self.liner=Line2D(self.xs, self.rho_r,color='r')
        # self.initial_rho=self.rho_axes.plot(self.xs,self.rho_l,'o',color='b')
        # self.initial_rho=self.rho_axes.plot(self.xs,self.rho_r,'o',color='r')
        self.rho_axes.set_xlim(0,1)
        self.rho_axes.set_ylim(0,0.4)
        self.rholup=self.rho_axes.add_line(self.linel)
        self.rhorup=self.rho_axes.add_line(self.liner)

# pol
        self.ax_poly=fig.add_subplot(35,1,2)
        self.pol_points={0:0.5,0.4:0.5,0.6:0.7,0.9:0.5}
        self.pol_x, self.pol_y = zip(*sorted(self.pol_points.items()))
        self.pol_dragging_point = None
        # for i in range(len(self.x)):
        #     self.points[self.x[i]]=self.y[i]
        self.pol_z=np.polyfit(self.pol_x,self.pol_y,5) # Use the interactive widget! that receives input.
        self.pol_f=np.poly1d(self.pol_z)
        self.pol_x_new=np.linspace(self.pol_x[0],self.pol_x[-1],50) # 50 could be changed if more details are needed
        self.pol_y_new=self.pol_f(self.pol_x_new)
        self.initial_pol= self.ax_poly.plot(self.pol_x,self.pol_y,'o',self.pol_x_new,self.pol_y_new)
        self.ax_poly.set_ylim(0,1)
        self.ax_poly.set_xlim(0,1)

# # p-diagram
#         self.p_diagram_alpha_star = 0.5
#         self.p_diagram_beta_start = 0.5
#         self.p_diagram_points = self.points
#         for x, y in self.points.items():
#             a, b = x, y
#         self.p_diagram_axes = self.fig.add_subplot(35,1,4)
#         self.p_diagram_axes.set_xlim(0, 1)
#         self.p_diagram_axes.set_ylim(0, 1)
#         self.p_diagram_initial_point, =self.p_diagram_axes.plot(a,b,"b", marker="o", markersize=10)
        self._init_plot()
    def _init_plot(self):
        # self.draw_rho()
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        plt.show()


    def _remove_point(self, x, _):
        if x in self.points:
            self.points.pop(x)

    def pol_remove_point(self, x, _):
        if x in self.pol_points:
            self.pol_points.pop(x)
    def update_variables(self,al,be):
        self.alpha=al
        self.beta=be
    def update_result(self):
        x, y = zip(*sorted(self.points.items()))
        new_x=x[0]
        new_y=y[0]
        self.update_variables(new_x,new_y)
        rect.patches[0].set_height(new_x)
        rect.patches[1].set_height(new_y)

        print("J : {} , Lam : {}".format(J,Lambda))
        for x,y in self.points.items():
            self.alpha=x
            self.beta=y
        self.lambda_0=lambdas[0]
        self.lambda_1=lambdas[24]
        self.lambda_min=min(lambdas)
        self.intercall=pow(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_0*self.lambda_min/pow(1+sqrt(self.l),2)
        self.intercalr=pow(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2),2)-4*self.lambda_1*self.lambda_min/pow(1+sqrt(self.l),2)
        self.alpha_star=0.5*(self.lambda_0-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt( 0 if self.intercall < 0.0000001 else self.intercall ))
        self.beta_star=0.5*(self.lambda_1-(self.l-1)*self.lambda_min/pow((1+sqrt(self.l)),2) -sqrt(0 if self.intercalr < 0.0000001 else self.intercalr))
        self.j_l=self.alpha*(self.lambda_0-self.alpha)/(self.lambda_0+(self.l-1)*self.alpha)
        self.j_r=self.beta*(self.lambda_1-self.beta)/(self.lambda_1+(self.l-1)*self.beta)
        self.rhointercall=[(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_l*(self.l-1)/(2*self.l*lambda_x),2) - self.j_l/(self.l*lambda_x)) for lambda_x in self.lambdas]
        self.rhointercalr=[(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),pow(1/(2*self.l) + self.j_r*(self.l-1)/(2*self.l*lambda_x),2) - self.j_r/(self.l*lambda_x)) for lambda_x in self.lambdas] 
        self.rho_l=[x - sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercall]
        self.rho_r=[x + sqrt(0 if y < 0.000001 else y) for x, y in self.rhointercalr]
        self.rholup.set_ydata(self.rho_l)
        self.rhorup.set_ydata(self.rho_r)
        # self.rho_axes.plot(self.xs,self.rho_l,'o',color='b')
        # self.rho_axes.plot(self.xs,self.rho_r,'o',color='r')
        print(self.alpha)
        print(self.beta)
        # print(rho_l)
        fig.canvas.draw()
    

    def _update_plot(self):

        x, y = zip(*sorted(self.points.items()))
        # Add new plot
        # Update current plot
        self.initial_point.set_data(x, y)
        # self.p_diagram_initial_point.set_data(x, y)

        pol_x, pol_y = zip(*sorted(self.pol_points.items()))
        print(pol_x,pol_y)
        pol_z=np.polyfit(pol_x,pol_y,5) # Use the interactive widget! that receives input.
        pol_f=np.poly1d(pol_z)
        pol_x_new=np.linspace(pol_x[0],pol_x[-1],50) # 50 could be changed if more details are needed
        pol_y_new=pol_f(pol_x_new)
        self.ax_poly.plot(pol_x,pol_y,'o',pol_x_new,pol_y_new)
        
        self.fig.canvas.draw()
    def _find_neighbor_point(self, event):
        u""" Find point around mouse position
        :rtype: ((int, int)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 3.0
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for x, y in self.points.items():
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None
    def pol_find_neighbor_point(self, event):
        u""" Find point around mouse position
        :rtype: ((int, int)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 3.0
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for x, y in self.pol_points.items():
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None

    def _add_point(self, x, y=None):
        if self.points:
            return
        if isinstance(x, MouseEvent):
            x, y = x.xdata, x.ydata
        self.points[x] = y
        return x, y

    def pol_add_point(self, x, y=None):
        if self.pol_points:
            return
        if isinstance(x, MouseEvent):
            print('yea')
            x, y = x.xdata, x.ydata
        print(x,y)
        self.pol_points[x] = y
        print(self.pol_points)
        return x, y

    def _on_click(self, event):
        u""" callback method for mouse click event
        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self.axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
            #pol
        if event.button == 1 and event.inaxes in [self.ax_poly]:
            pol_point = self.pol_find_neighbor_point(event)
            if pol_point:
                self.pol_dragging_point = pol_point
        self._update_plot()
        self.update_result()
            
    def _on_release(self, event):
        u""" callback method for mouse release event
        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self.axes] and self._dragging_point:
            self._add_point(event)
            self._dragging_point = None
            self._update_plot()
        #pol
        if event.button == 1 and event.inaxes in [self.ax_poly] and self.pol_dragging_point:
            self.pol_add_point(event)
            self.pol_dragging_point = None
            self._update_plot()     

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if event.inaxes in [self.axes]:
            if not self._dragging_point:
                return
            self._remove_point(*self._dragging_point)
            self._dragging_point = self._add_point(event)
            self._update_plot()
            self.update_result()
        #pol
        # if event.inaxes in [self.ax_poly]: 
        #     if not self.pol_dragging_point:
        #         return
        #     self.pol_remove_point(*self.pol_dragging_point)
        #     self.pol_dragging_point = self.pol_add_point(event)
        #     self._update_plot()

class poly:
    def __init__(self,fig):
        self.fig=fig

    def _init_plot(self):
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        plt.show()
    # def update_result(self):
    #     x, y = zip(*sorted(self.points.items()))
    #     new_x=x[0]
    #     new_y=y[0]
    #     rect.patches[0].set_height(new_x)
    #     rect.patches[1].set_height(new_y)

    #     print("J : {} , Lam : {}".format(J,Lambda))
    #     fig.canvas.draw()
    def _add_point(self, x, y=None):
        if self.points:
            return
        if isinstance(x, MouseEvent):
            x, y = x.xdata, x.ydata
        self.points[x] = y
        return x, y

    def _update_plot(self):

        x, y = zip(*sorted(self.points.items()))
        # Add new plot
        # Update current plot
        self.z=np.polyfit(x,y,10) # Use the interactive widget! that receives input.
        self.f=np.poly1d(self.z)
        self.x_new=np.linspace(x[0],x[-1],50) # 50 could be changed if more details are needed
        self.y_new=self.f(self.x_new)
        self.ax_poly.plot(self.x,self.y,'o',self.x_new,self.y_new)
        self.fig.canvas.draw()
    def _find_neighbor_point(self, event):
        u""" Find point around mouse position
        :rtype: ((int, int)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 3.0
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for x, y in self.points.items():
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None    

    def _on_click(self, event):
        u""" callback method for mouse click event
        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self.ax_poly]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
            # else:
            #     self._add_point(event)
        self._update_plot()
            # self.update_result()

    def _on_release(self, event):
        u""" callback method for mouse release event
        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self.ax_poly] and self._dragging_point:
            self._add_point(event)
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        self._remove_point(*self._dragging_point)
        self._dragging_point = self._add_point(event)
        self._update_plot()
        # self.update_result()


# pol=poly(fig)


# phase diagram, branches, lambda, alpha-beta switch, lambda-switch, HD-MC, LD-MC
# ---------------------------------------------------------phase diagram

class p_diagram :
    def __init__(self,fig,slider) :
        # need equations
 
        self.p_diagram__init_plot()
    def _init_plot(self):
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        plt.show()
    def _update_plot(self):
        for x, y in self.slider.points.items():
            a, b = x, y
        self.points = slider.points
        self.axes.plot(a,b,"b", marker="o", markersize=10)
        self.fig.canvas.draw()
    def _on_click(self, event):
        u""" callback method for mouse click event
        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self.ax_poly]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
            # else:
            #     self._add_point(event)
        self._update_plot()
            # self.update_result()

    def _on_release(self, event):
        u""" callback method for mouse release event
        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self.ax_poly] and self._dragging_point:
            self._add_point(event)
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        self._remove_point(*self._dragging_point)
        self._dragging_point = self._add_point(event)
        self._update_plot()
        # self.update_result()    
# ----------------------------------------------------------

    





fig.set_size_inches(18.5, 10.5, forward=True)






slide_axes =fig.add_subplot(35,1,3)
slide_axes.set_position([0.1,0.1,0.2,0.2],which='both')
cursor2 = Cursor(slide_axes, useblit=True, color='red', linewidth=2)
slider=slideandpol(fig,slide_axes,[])
# slider.sfreq.on_changed(slider.update)
# slider.samp.on_changed(slider.update)


# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button, RadioButtons

# fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.25, bottom=0.25)
# t = np.arange(0.0, 1.0, 0.001)
# a0 = 5
# f0 = 3
# s = a0*np.sin(2*np.pi*f0*t)
# l, = plt.plot(t, s, lw=2, color='red')
# plt.axis([0, 1, -10, 10])

# axcolor = 'lightgoldenrodyellow'
# axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
# axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

# sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
# samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)


# def update(val):
#     amp = samp.val
#     freq = sfreq.val
#     l.set_ydata(amp*np.sin(2*np.pi*freq*t))
#     fig.canvas.draw_idle()
# sfreq.on_changed(update)
# samp.on_changed(update)

# resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


# def reset(event):
#     sfreq.reset()
#     samp.reset()
# button.on_clicked(reset)

# rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
# radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


# def colorfunc(label):
#     l.set_color(label)
#     fig.canvas.draw_idle()
# radio.on_clicked(colorfunc)

plt.show()

