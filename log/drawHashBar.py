# 并列柱状图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np

x=np.arange(5)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

y1=[0.5567123692808192,0.5783602800307962,0.5999582642128273,0.5352330461674398,0.572245099753405]
y2=[1.1468531468531469, 1.2869692532942898, 1.1641842743332178, 1.032934131736527,1.0980253878702397]

for i in range(len(y1)):
    print(1-y1[i]/y2[i])


bar_width=0.2#设置柱状图的宽度
tick_label=['FCV Training','Idle','Kernel Compile','Docker Start','KVM Init']

#绘制并列柱状图
plt.bar(x,y1,bar_width,color='royalblue',label='Partial-Hash')
plt.bar(x+bar_width,y2,bar_width,color='firebrick',label='normal')

plt.legend()#显示图例，即label
plt.xticks(x+bar_width/2,tick_label)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.show()