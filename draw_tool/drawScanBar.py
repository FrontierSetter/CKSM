# 并列柱状图
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

x=np.arange(5)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同

y2=[2.4328404796788097, 3.930813962853783, 3.398950243540646, 4.053208556149732,2.1462049868061372]


bar_width=0.4#设置柱状图的宽度
tick_label=['PyTorch','Idle','Compile','Docker','KVM']
plt.figure(figsize=(9,6))

#绘制并列柱状图
bars = plt.bar(x,y2,bar_width,label='scan',color='#5390d9', edgecolor='black', linewidth=1)

# for b in bars:
#     h = b.get_height()
#     plt.text(b.get_x()+b.get_width()/2, h, '%.2f$\\times$' % (h), ha='center', va='bottom', fontsize=22)

plt.ylabel('Scan Amplification Factor', fontsize=28)

plt.yticks(fontsize=20)
# plt.legend(fontsize=18)#显示图例，即label
plt.xticks(x,tick_label, fontsize=24)#显示x坐r标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
# plt.xticks([])
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
plt.subplots_adjust(left=0.11, right=0.98, top=0.99, bottom=0.12)
plt.axhline(y=1,ls="--",c="red",linewidth=4)#添加水平直线
# plt.savefig('scan_overhead.pdf')

plt.savefig('sparse_scan.pdf')
plt.show()