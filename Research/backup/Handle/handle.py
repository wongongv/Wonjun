import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import plotly.plotly as py
import numpy as np

# fig=plt.figure()
# ax=fig.add_subplot(1,1,1)
# line = Line2D([0,0.5], [0,0.5], marker = 'o', markerfacecolor = 'red')
# line2 = Line2D([0.5,0.5], [0.5,1],  markerfacecolor = 'red')
# line3 = Line2D([0.5,1], [0.5,0.5],  markerfacecolor = 'red')
# ax.add_line(line3)
# ax.add_line(line2)
# ax.add_line(line)
# plt.xlabel(r'$\alpha$')
# plt.ylabel(r'$\beta$')
# plt.title("Simple TASEP phase diagram\n")
# plt.legend()



# fig2=plt.figure()
# ax2=fig2.add_subplot(1,1,1)
# rhol=0.5-pow((0.25-( 0.05*(0.65)/0.49)),0.5)
# print(rhol)
# line2_1 = Line2D([0,1], [rhol,rhol],  markerfacecolor = 'red')
# ax2.add_line(line2_1)
# plt.xlabel('x')
# plt.ylabel(r'$\rho$')
# plt.title(r"LD, $\alpha = 0.05$, $\beta = 1$")
# ax2.set_ylim(0,1)
# ax2.set_xlim(0,1)
# ax2.plot()


# fig3=plt.figure()
# ax3=fig3.add_subplot(1,1,1)
# rhor=0.5+pow((0.25-( 0.05*(0.65)/0.49)),0.5)
# print(rhor)
# line3_1 = Line2D([0,1], [rhor,rhor],  markerfacecolor = 'red')
# ax3.add_line(line3_1)
# plt.xlabel('x')
# plt.ylabel(r'$\rho$')
# plt.title(r"HD, $\alpha = 1$, $\beta = 0.05$")
# ax3.set_ylim(0,1)
# ax3.set_xlim(0,1)

# fig4=plt.figure()
# ax4=fig4.add_subplot(1,1,1)
# rhoc=0.5
# print(rhoc)
# line4_1 = Line2D([0,1], [rhoc,rhoc],  markerfacecolor = 'red')
# ax4.add_line(line4_1)
# plt.xlabel('x')
# plt.ylabel(r'$\rho$')
# plt.title(r"MC, $\alpha = 1$, $\beta = 1$")
# ax4.set_ylim(0,1)
# ax4.set_xlim(0,1)

# fig5=plt.figure()
# ax5=fig5.add_subplot(1,1,1)
# points_5=np.array([(0,0),(0.2,0.2*0.5/0.7),(0.3,0.4*0.3/0.7)])
# x_5=points_5[:,0]
# print(x_5)
# y_5=points_5[:,1]
# z_5=np.polyfit(x_5,y_5,2)
# f_5=np.poly1d(z_5)
# x_new_5=np.linspace(x_5[0],x_5[-1],50)
# y_new_5=f_5(x_new_5)
# ax5.plot(x_new_5,y_new_5)
# line5_1 = Line2D([0.3,1], [0.4*0.3/0.7,0.4*0.3/0.7],  markerfacecolor = 'red')
# ax5.add_line(line5_1)
# ax5.set_ylim(0,1)
# ax5.set_xlim(0,1)

fig6=plt.figure()
ax6=fig6.add_subplot(1,1,1)
points_6=np.array([(0,0),(0.2,0.2*0.5/0.7),(0.3,0.4*0.3/0.7)])
x_6=points_6[:,0]
print(x_6)
y_6=points_6[:,1]
z_6=np.polyfit(x_6,y_6,2)
f_6=np.poly1d(z_6)
x_new_6=np.linspace(x_6[0],x_6[-1],50)
y_new_6=f_6(x_new_6)
ax6.plot(x_new_6,y_new_6)
line6_1 = Line2D([0.3,1], [0.175,0.175],  markerfacecolor = 'red')
plt.xlabel(r'$\alpha$')
plt.ylabel('J')
plt.title(r"Graph of J, function of $\beta$ with $\alpha = 0.3$, $\lambda = 0.7$")
ax6.add_line(line6_1)
ax6.set_ylim(0,1)
ax6.set_xlim(0,1)

fig7=plt.figure()
ax7=fig7.add_subplot(1,1,1)
points_7=np.array([(0,0),(0.2,0.2*0.5/0.7),(0.3,0.4*0.3/0.7)])
x_7=points_7[:,0]
print(x_7)
y_7=points_7[:,1]
z_7=np.polyfit(x_7,y_7,2)
f_7=np.poly1d(z_7)
x_new_7=np.linspace(x_7[0],x_7[-1],50)
y_new_7=f_7(x_new_7)
ax7.plot(x_new_7,y_new_7)
line7_1 = Line2D([0.3,1], [0.175,0.175],  markerfacecolor = 'red')
plt.xlabel(r'$\beta$')
plt.ylabel('J')
plt.title(r"Graph of J, function of $\alpha$ with $\beta = 0.3$, $\lambda = 0.7$")
ax7.add_line(line7_1)
ax7.set_ylim(0,1)
ax7.set_xlim(0,1)

plt.show()
