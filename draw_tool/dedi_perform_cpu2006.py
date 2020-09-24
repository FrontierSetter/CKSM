# 并列柱状图
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

y_base = [
    272,
    430,
    293,
    366,
    432,
    404,
    484,
    597,
    487,
    408,
    411,
    228,
]

y_cksm = [
    274,
    477,
    313,
    379,
    438,
    405,
    495,
    608,
    495,
    419,
    414,
    229,
]

bar_width=0.26#设置柱状图的宽度
tick_label=['perlbench','bzip2','gcc','mcf','gobmk','hmmer','sjeng','libquantum','h264ref','omnetpp','astar','xalancbmk']
x=np.arange(len(tick_label))

totalRatio = 0.0
for cksm, base in zip(y_cksm, y_base):
    cur = float(cksm)/base
    print(cur)
    totalRatio += cur
print("total: %f" % (totalRatio/len(tick_label)))



plt.figure(figsize=(9,6))

#绘制并列柱状图
plt.bar(x-bar_width/2*1.18,y_base,bar_width,label='Base',color="#0496ff",edgecolor='black',hatch='-')
plt.bar(x+bar_width/2*1.18,y_cksm,bar_width,label='CKSM',color="#47b347",edgecolor='black',hatch='//')

plt.ylabel('Times(s)', fontsize=22)
plt.xlabel('Benchmark', fontsize=22)

plt.legend(fontsize=20)#显示图例，即label
plt.yticks(fontsize=18)
plt.xticks(x,tick_label, fontsize=14,rotation=25)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.subplots_adjust(left=0.102, right=0.98, top=0.99, bottom=0.18)

# plt.savefig('scan_overhead.pdf')

plt.savefig('perform_cpu2006_int.pdf')
plt.show()