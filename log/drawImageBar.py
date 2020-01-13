# 并列柱状图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np

x=np.arange(5)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

# y1=[6.8,6.7,7.5,0.5,2.6]
# y2=[2.4328404796788097, 3.930813962853783, 3.398950243540646, 4.053208556149732,2.1462049868061372]

y2=[
    1.780233272,
    0.558659218,
    0, # -0.274977085
    66.62198391,
    5.345211581
]
y1=[
    13.1368938,
    8.379888268,
    13.47387718,
    67.49329759,
    29.06458797
]


bar_width=0.2#设置柱状图的宽度
tick_label=['redis','postgres','Apache','MongoDB','Nginx']

#绘制并列柱状图
plt.bar(x,y1,bar_width,color='royalblue',label='CKSM')
plt.bar(x+bar_width,y2,bar_width,color='firebrick',label='UKSM')

plt.legend()#显示图例，即label
plt.xticks(x+bar_width/2,tick_label)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置

plt.xlabel('Image type')
plt.ylabel('Memory saving percentage(%)')


plt.savefig('image_64.pdf')


plt.show()