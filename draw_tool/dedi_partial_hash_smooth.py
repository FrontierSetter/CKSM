from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

color1 = 'tab:blue'
color2 = 'tab:red'

# xPosition = [-40, 32, 128, 256, 512, 1024, 2046]
# xPosition = [24, 64, 128, 256, 512, 1024, 2046]
xPosition = [0, 1, 2, 3, 4, 5, 6]
# xtickArr = ['5','6','7','8','9','10','11']
xtickArr = ['32','64','128','256','512','1024','2048']
xtickReal = [32,64,128,256,512,1024,2048]
partialRateArr = [88.5968, 91.4175, 91.7633, 98.2856, 93.4616, 93.2143, 93.3089]
calcOverheadArr = [0.462007, 0.498028, 0.520771, 0.555602, 0.646362, 0.764094, 0.830889]
skipedCmpArr = [0.738756, 0.793132, 0.793198, 0.813813, 0.878168, 0.701435, 0.731554]

T = np.array(xPosition)
xnew = np.linspace(T.min(),T.max(),301)

partialRateArr_smooth = make_interp_spline(T,partialRateArr)(xnew)
calcOverheadArr_smooth = make_interp_spline(T,calcOverheadArr)(xnew)

fig = plt.figure(figsize=(15,6)) #定义figure，（1）中的1是什么

axRate = fig.add_subplot(111)
axOverhead=axRate.twinx()

plot1 = axRate.plot(xnew, partialRateArr_smooth, label="Skip Rate", color=color1, linewidth=4, marker='o', markersize=10, markevery=30)
plot2 = axOverhead.plot(xnew, calcOverheadArr_smooth, label="Calculation Overhead", color=color2, linewidth=4, marker='D', markersize=9, markevery=30)

axRate.set_xticks(xPosition)
axRate.spines['left'].set_color(color1)
# axRate.spines['top'].set_color('none')
for tl in axRate.get_yticklabels():
    tl.set_color(color1)
    tl.set_fontsize(18)
axRate.set_xticklabels(xtickArr, fontsize=18, rotation=0)
axRate.set_ylabel('Byte-by-byte Comparison Skip Rate(%)', fontsize=21, color=color1)
axRate.set_xlabel('Partial Hash Length(Bytes)', fontsize=21)
for tl in axRate.get_xticklabels():
    tl.set_fontsize(15)
# plt.text(0,0,'$2^{x}$', fontsize=14)

axOverhead.set_ylim(0.37,1)
axOverhead.spines['right'].set_color(color2)
axOverhead.spines['left'].set_color('none')
axOverhead.spines['top'].set_color('none')
for tl in axOverhead.get_yticklabels():
    tl.set_fontsize(18)
axOverhead.tick_params(axis='y', colors=color2)
axOverhead.set_ylabel('Partial Hash Calculation Overhead($\mu s$)', fontsize=21, color=color2)

plots = plot1+plot2
labs = [l.get_label() for l in plots]

axRate.legend(plots, labs, fontsize=22, handlelength=3)
# axOverhead.legend(fontsize=18)


# ax_rate.legend(fontsize=12)

# #轴名称，刻度值的颜色
# #ax_cof.axis['left'].label.set_color(ax_cof.get_color())
# ax_overhead.axis['right'].label.set_color('red')
# # ax_cmp.axis['right2'].label.set_color('green')
# # ax_cp.axis['right3'].label.set_color('pink')
# # ax_wear.axis['right4'].label.set_color('blue')

# ax_overhead.axis['right'].major_ticks.set_color('red')
# # ax_cmp.axis['right2'].major_ticks.set_color('green')
# # ax_cp.axis['right3'].major_ticks.set_color('pink')
# # ax_wear.axis['right4'].major_ticks.set_color('blue')

# ax_overhead.axis['right'].major_ticklabels.set_color('red')
# # ax_cmp.axis['right2'].major_ticklabels.set_color('green')
# # ax_cp.axis['right3'].major_ticklabels.set_color('pink')
# # ax_wear.axis['right4'].major_ticklabels.set_color('blue')

# ax_overhead.axis['right'].line.set_color('red')
# # ax_cmp.axis['right2'].line.set_color('green')
# # ax_cp.axis['right3'].line.set_color('pink')
# # ax_wear.axis['right4'].line.set_color('blue')


plt.subplots_adjust(left=0.06, right=0.94, top=0.95, bottom=0.11)

plt.savefig('partial_hash.pdf')
plt.show()