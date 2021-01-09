import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# python .\dedi_handler_time_box.py '..\log\7-29-3(large_128_pksm)\out_add_handler_time.log' '..\log\7-29-1(large_128_base)\out_add_handler_time.log' '..\log\7-29-2(large_128_uksm)\out_add_handler_time.log' '..\log\7-29-3(large_128_pksm)\out_exit_handler_time.log' '..\log\7-29-1(large_128_base)\out_exit_handler_time.log' '..\log\7-29-2(large_128_uksm)\out_exit_handler_time.log' 
# python .\dedi_handler_time_box.py '..\log\7-29-4(large_64_pksm)\out_add_handler_time.log' '..\log\7-29-6(large_64_base)\out_add_handler_time.log' '..\log\7-29-5(large_64_uksm)\out_add_handler_time.log' '..\log\7-29-4(large_64_pksm)\out_exit_handler_time.log' '..\log\7-29-6(large_64_base)\out_exit_handler_time.log' '..\log\7-29-5(large_64_uksm)\out_exit_handler_time.log'
# python .\dedi_handler_time_box.py '..\log\7-29-8(large_32_pksm)\out_add_handler_time.log' '..\log\7-29-10(large_32_base)\out_add_handler_time.log' '..\log\7-29-9(large_32_uksm)\out_add_handler_time.log' '..\log\7-29-8(large_32_pksm)\out_exit_handler_time.log' '..\log\7-29-10(large_32_base)\out_exit_handler_time.log' '..\log\7-29-9(large_32_uksm)\out_exit_handler_time.log'

xArr = []
yArr_add = []
label_add = []
yArr_exit = []
label_exit = []
typeArr = []
compArr = []

totalContainerNum = 3
addThreshold = 200.0
exitThreshold = 20.0

for i in range(1, 4):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseOverhead = float(baseArr[1])

    compTime = int(baseArr[2])
    # compTime += (float(compTime-baseTime)/(totalContainerNum-1.0))
    print("st: %d, ed: %d" % (baseTime, compTime))

    xArr.append([])
    yArr_add.append([])
    typeArr.append(curType)
    label_add.append(curType)

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curOverhead = float(curArr[1])
        curCnt = int(curArr[2]) if len(curArr) > 2 else 1

        if curOverhead > addThreshold:
            continue

        if curTime < baseTime:
            continue

        if curTime > compTime:
            break
        
        for i in range(curCnt):
            yArr_add[-1].append(float(curOverhead-baseOverhead))

for i in range(4, 7):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseOverhead = float(baseArr[1])

    compTime = int(baseArr[2])
    # compTime += (float(compTime-baseTime)/(totalContainerNum-1.0))
    print("st: %d, ed: %d" % (baseTime, compTime))

    xArr.append([])
    yArr_exit.append([])
    typeArr.append(curType)
    label_exit.append(curType)

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curOverhead = float(curArr[1])
        curCnt = int(curArr[2]) if len(curArr) > 2 else 1

        if curOverhead > exitThreshold:
            continue

        if curTime < baseTime:
            continue

        if curTime > compTime:
            break
        
        for i in range(curCnt):
            yArr_exit[-1].append(float(curOverhead-baseOverhead))

plt.figure(figsize=(9,6))

color=['#00B050', '#1f497d', '#F79646']

print('start draw1')
plt.subplot(121)

f=plt.boxplot(
    x=yArr_add,
    patch_artist=True,
    labels=label_add,#添加具体的标签名称
    boxprops={'color':'black','facecolor':'#9999ff'},
    flierprops={'marker':'o','markerfacecolor':'red','color':'black'},#设置异常值属性，点的形状、填充颜色和边框色
    showmeans=True,
    widths=0.65,
    whis=3,
    showfliers=False,
    meanprops={'marker':'D','markerfacecolor':'#8064A2','markeredgecolor':"#8064A2"},#设置均值点的属性，点的颜色和形状
    medianprops={"linestyle":'--','color':'#8064A2','linewidth':2},#设置中位数线的属性，线的类型和颜色

)

for box, c in zip(f['boxes'], color):
    box.set(facecolor =c)

# xfmt = ScalarFormatter(useMathText=True)
# xfmt.set_powerlimits((0, 0))
# plt.gca().yaxis.set_major_formatter(xfmt)
plt.title('page allocate latency',fontsize=16)

# plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=12)
plt.ylabel('Latency(ns)', fontsize=16)

print('start draw2')
plt.subplot(122)

f=plt.boxplot(
    x=yArr_exit,
    patch_artist=True,
    labels=label_add,#添加具体的标签名称
    boxprops={'color':'black','facecolor':'#9999ff'},
    flierprops={'marker':'o','markerfacecolor':'red','color':'black'},#设置异常值属性，点的形状、填充颜色和边框色
    showmeans=True,
    widths=0.65,
    whis=3,
    showfliers=False,
    meanprops={'marker':'D','markerfacecolor':'#ffd166','markeredgecolor':"#ffd166"},#设置均值点的属性，点的颜色和形状
    medianprops={"linestyle":'--','color':'#f5cac3','linewidth':2},#设置中位数线的属性，线的类型和颜色

)

for box, c in zip(f['boxes'], color):
    box.set(facecolor =c)


# xfmt = ScalarFormatter(useMathText=True)
# xfmt.set_powerlimits((0, 0))
# plt.gca().yaxis.set_major_formatter(xfmt)
plt.title('page reclaim latency',fontsize=16)

# plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=12)
# plt.ylabel('Overhead(ns)', fontsize=16)


plt.subplots_adjust(left=0.08, right=0.99, top=0.94, bottom=0.11)

print('start save')
plt.savefig('scal_handler.pdf')
# plt.savefig('scal_handler.png',dpi=1200)
print('start show')
plt.show()



