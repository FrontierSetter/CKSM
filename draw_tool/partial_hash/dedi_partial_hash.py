from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt
import numpy as np

xPosition = [32, 64, 128, 256, 512, 1024, 2046]
# xPosition = [0, 1, 2, 3, 4, 5, 6]
xtickArr = ['32','64','128','256','512','1024','2048']
partialRateArr = [88.5968, 91.4175, 91.7633, 98.2856, 93.4616, 93.2143, 93.3089]
calcOverheadArr = [0.462007, 0.498028, 0.520771, 0.555602, 0.646362, 0.764094, 0.830889]
skipedCmpArr = [0.738756, 0.793132, 0.793198, 0.813813, 0.878168, 0.701435, 0.731554]

fig = plt.figure(figsize=(9,6)) #定义figure，（1）中的1是什么
ax_rate = HostAxes(fig,[0.06,0.15,0.8,0.7])  #用[left, bottom, weight, height]的方式定义axes，0 <= l,b,w,h <= 1

#parasite addtional axes, share x
ax_overhead = ParasiteAxes(ax_rate, sharex=ax_rate)
ax_cmp = ParasiteAxes(ax_rate, sharex=ax_rate)
# ax_cp = ParasiteAxes(ax_cof, sharex=ax_cof)
# ax_wear = ParasiteAxes(ax_cof, sharex=ax_cof)

#append axes
ax_rate.parasites.append(ax_overhead)
ax_rate.parasites.append(ax_cmp)
# ax_cof.parasites.append(ax_cp)
# ax_cof.parasites.append(ax_wear)



#invisible right axis of ax_cof
ax_rate.axis['right'].set_visible(False)
ax_rate.axis['top'].set_visible(False)
ax_overhead.axis['right'].set_visible(True)
ax_overhead.axis['right'].major_ticklabels.set_visible(True)
ax_overhead.axis['right'].label.set_visible(True)

font2 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size' : 18,
}
#set label for axis
ax_rate.set_ylabel('Partial Hash Skip Rate (%)', fontdict=font2)
ax_rate.set_xlabel('Partial Hash Length (Byte)', fontsize=18)
ax_overhead.set_ylabel('Partial Hash Calculation Overhead (ns)', fontsize=18)
ax_cmp.set_ylabel('Skiped memcmp Overhead (ns)')
# ax_cp.set_ylabel('CP')
# ax_wear.set_ylabel('Wear')

load_axisline = ax_cmp.get_grid_helper().new_fixed_axis
# cp_axisline = ax_cp.get_grid_helper().new_fixed_axis
# wear_axisline = ax_wear.get_grid_helper().new_fixed_axis

ax_cmp.axis['right2'] = load_axisline(loc='right', axes=ax_cmp, offset=(60,0))
# ax_cp.axis['right3'] = cp_axisline(loc='right', axes=ax_cp, offset=(80,0))
# ax_wear.axis['right4'] = wear_axisline(loc='right', axes=ax_wear, offset=(120,0))

fig.add_axes(ax_rate)

''' #set limit of x, y
ax_cof.set_xlim(0,2)
ax_cof.set_ylim(0,3)
'''

curve_cof, = ax_rate.plot(xPosition, partialRateArr, label="Skip Rate", color='black')
curve_temp, = ax_overhead.plot(xPosition, calcOverheadArr, label="Calculation Overhead", color='red')
curve_load, = ax_cmp.plot(xPosition, skipedCmpArr, label="Skiped Cmp Overhead", color='green')
# curve_cp, = ax_cp.plot([0, 1, 2], [0, 40, 25], label="CP", color='pink')
# curve_wear, = ax_wear.plot([0, 1, 2], [25, 18, 9], label="Wear", color='blue')


ax_overhead.set_ylim(0.4,1)
ax_cmp.set_ylim(0.4,1)
# ax_cp.set_ylim(0,50)
# ax_wear.set_ylim(0,30)

ax_rate.legend(fontsize=12)

#轴名称，刻度值的颜色
#ax_cof.axis['left'].label.set_color(ax_cof.get_color())
ax_overhead.axis['right'].label.set_color('red')
ax_cmp.axis['right2'].label.set_color('green')
# ax_cp.axis['right3'].label.set_color('pink')
# ax_wear.axis['right4'].label.set_color('blue')

ax_overhead.axis['right'].major_ticks.set_color('red')
ax_cmp.axis['right2'].major_ticks.set_color('green')
# ax_cp.axis['right3'].major_ticks.set_color('pink')
# ax_wear.axis['right4'].major_ticks.set_color('blue')

ax_overhead.axis['right'].major_ticklabels.set_color('red')
ax_cmp.axis['right2'].major_ticklabels.set_color('green')
# ax_cp.axis['right3'].major_ticklabels.set_color('pink')
# ax_wear.axis['right4'].major_ticklabels.set_color('blue')

ax_overhead.axis['right'].line.set_color('red')
ax_cmp.axis['right2'].line.set_color('green')
# ax_cp.axis['right3'].line.set_color('pink')
# ax_wear.axis['right4'].line.set_color('blue')

plt.xticks(xPosition, xtickArr, fontsize=16)


plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.savefig('partial_hash.pdf')
plt.show()