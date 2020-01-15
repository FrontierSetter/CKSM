# 并列柱状图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np

x=np.arange(5)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

y1=[0.9442192804695108,0.9693127060613745,0.9831702014791084,0.895712888019212,0.9235144566020079]
y2=[1.1468531468531469, 1.2869692532942898, 1.1641842743332178, 1.032934131736527,1.0980253878702397]

for i in range(len(y1)):
    y1[i] *= 100
    y2[i] = 100-y1[i]


bar_width=0.2#设置柱状图的宽度
tick_label=['FCV Training','Idle','Kernel Compile','Docker Start','KVM Init']
plt.figure(figsize=(9,6))

#绘制并列柱状图
plt.bar(x,y1,bar_width,color='royalblue',label='with Partial-Hash')
plt.bar(x+bar_width,y2,bar_width,color='firebrick',label='without Partial-Hash')

plt.ylabel('Proportion(%)', fontsize=16)


plt.legend(fontsize=14)#显示图例，即label
plt.yticks(fontsize=14)
plt.xticks(x+bar_width/2,tick_label, fontsize=14)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig('partial_par.pdf')

plt.show()