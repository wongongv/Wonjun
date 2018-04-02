import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, Cursor
import math
from matplotlib.backend_bases import MouseEvent


fig=plt.figure()
ax=fig.add_subplot(3,1,1)
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


class slide:
    def __init__(self,fig,axes):
        self.fig=fig
        self.axes = axes
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)
        self._dragging_point = None
        self.points = {0.5:0.5}
        self.initial_point, =self.axes.plot(0.5,0.5,"b", marker="o", markersize=10) 
        self._init_plot()
        print('new')

    def _init_plot(self):
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)
        plt.show()

    def _remove_point(self, x, _):
        if x in self.points:
            self.points.pop(x)

    def update_result(self):
        x, y = zip(*sorted(self.points.items()))
        new_x=x[0]
        new_y=y[0]
        rect.patches[0].set_height(new_x)
        rect.patches[1].set_height(new_y)

        print("J : {} , Lam : {}".format(J,Lambda))
        fig.canvas.draw()

    def _update_plot(self):

        x, y = zip(*sorted(self.points.items()))
        # Add new plot
        # Update current plot
        self.initial_point.set_data(x, y)
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

    def _add_point(self, x, y=None):
        if self.points:
            return
        if isinstance(x, MouseEvent):
            x, y = x.xdata, x.ydata
        self.points[x] = y
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

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        self._remove_point(*self._dragging_point)
        self._dragging_point = self._add_point(event)
        self._update_plot()
        self.update_result()


class poly:
    def __init__(self,fig):
        self.fig=fig
        self.points={0:0.5,0.3:0.5,0.6:0.5,0.9:0.5}
        self.x, self.y = zip(*sorted(self.points.items()))
        self._dragging_point = None
        # for i in range(len(self.x)):
        #     self.points[self.x[i]]=self.y[i]
        self.z=np.polyfit(self.x,self.y,5) # Use the interactive widget! that receives input.
        self.f=np.poly1d(self.z)
        self.x_new=np.linspace(self.x[0],self.x[-1],50) # 50 could be changed if more details are needed
        self.y_new=self.f(self.x_new)
        self.ax_poly=fig.add_subplot(3,1,2)
        self.ax_poly.plot(self.x,self.y,'o',self.x_new,self.y_new)
        self.ax_poly.set_ylim(0,1)
        self._init_plot()

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

slide_axes =fig.add_subplot(3,1,3)
cursor2 = Cursor(slide_axes, useblit=True, color='red', linewidth=2)
slider=slide(fig,slide_axes)



# slider.sfreq.on_changed(slider.update)
# slider.samp.on_changed(slider.update)




plt.show()





        # l.set_data(amp+freq) # update y data.
