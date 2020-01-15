# 并列柱状图
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod', 'KSM-100':'violet', 'KSM-200':'chocolate', 'KSM-50':'rosybrown'}

barName = ['Base', 'CKSM-50', 'CKSM-100', 'CKSM-200', 'CKSM-500']

x=np.arange(4)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

y=[
    [18021.4375, 17735.566666666666, 17837.085000000003, 9411.6075],
    [18038.650833333333, 17910.596666666668, 18102.666666666668, 9396.889166666668],
    [17484.254999999997, 17560.40, 18212.155833333334, 9206.6525],
    [17963.75416666667, 17604.171666666665, 17989.981666666667, 9321.8325],
    [17406.091666666667, 17582.962499999998, 17690.070833333335, 9134.874999999998]
]
# y1=[18021.4375, 9411.6075, 17837.085000000003, 17735.566666666666]
# y2=[18038.650833333333, 9396.889166666668, 18102.666666666668, 17910.596666666668]
# y3=[17484.254999999997, 9206.6525, 18212.155833333334, 17560.40]
# y4=[17963.75416666667, 9321.8325, 17989.981666666667, 17604.171666666665]
# y5=[17406.091666666667, 9134.874999999998, 17690.070833333335, 17582.962499999998]


bar_width=0.1#设置柱状图的宽度
tick_label=['Mem_Seq_R','Mem_Seq_W','Mem_Rnd_R','Mem_Rnd_W']

plt.figure(figsize=(11,6))


#绘制并列柱状图
for i in range(5):
    plt.bar(x+i*bar_width,y[i],bar_width,color=colorTable[barName[i]],label=barName[i])

# plt.bar(x,y1,bar_width,color='royalblue',label='Partial-Hash')
# plt.bar(x+bar_width,y2,bar_width,color='firebrick',label='normal')
# plt.bar(x+bar_width*2,y2,bar_width,color='firebrick',label='normal')
# plt.bar(x+bar_width*3,y2,bar_width,color='firebrick',label='normal')
# plt.bar(x+bar_width*4,y2,bar_width,color='firebrick',label='normal')


plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
plt.legend(fontsize=14)#显示图例，即label

plt.ylabel('Bandwidth(MB/s)', fontsize=16)

plt.xticks(x+bar_width*5.0/2.0,tick_label)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig('mem_bench.pdf')


plt.show()