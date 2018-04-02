import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.widgets import Cursor


fig=plt.figure()
ax=fig.add_subplot(3,1,1)
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
    def __init__(self):
        self.axfreq = plt.axes([0.1, 0.1, 0.8, 0.03])
        self.axamp = plt.axes([0.1, 0.15, 0.8, 0.03])
        self.sfreq = Slider(self.axfreq, 'Freq', 0, 1.0, valinit=1,valfmt='%1.3f') #valinit = start position
        self.samp = Slider(self.axamp, 'Amp', 0, 1.0, valinit=1,valfmt='%1.3f')
    def update(self,val):

        amp = self.samp.val
        freq = self.sfreq.val
        print(val)
        print(amp)
        rect.patches[0].set_height(freq)
        rect.patches[1].set_height(amp)
        ax.set_ylim((0,1))
        fig.canvas.draw_idle()
        print("J : {} , Lam : {}".format(J,Lambda))
        fig.canvas.draw()

class poly:
    def __init__(self):
        self.points=np.array([(1,1),(2,4),(3,1),(9,3)]) #put data by reading txt(maybe?)
        self.x=self.points[:,0]
        self.y=self.points[:,1]
        self.z=np.polyfit(self.x,self.y,5) # Use the interactive widget! that receives input.
        self.f=np.poly1d(self.z)
        self.x_new=np.linspace(self.x[0],self.x[-1],50) # 50 could be changed if more details are needed
        self.y_new=self.f(self.x_new)
    def update(self):
        #l.set_ydata
        return



ax_poly=fig.add_subplot(3,1,2)
pol=poly()
ax_poly.plot(pol.x,pol.y,'o',pol.x_new,pol.y_new) # make marker with 'o', think about title


#cursor
cursor = Cursor(ax_poly, useblit=True, color='red', linewidth=2)

slider=slide()
slider.sfreq.on_changed(slider.update)
slider.samp.on_changed(slider.update)




plt.show()





        # l.set_data(amp+freq) # update y data.