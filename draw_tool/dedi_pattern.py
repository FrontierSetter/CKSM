import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from math import log
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from matplotlib.pyplot import MultipleLocator

# python .\dedi_pattern.py '..\log\7-23-5(64nginx_hlist)\out_total.log' '..\log\7-23-4(10elastic_hlist)\out_total.log'
# python .\dedi_pattern.py '..\log\8-26-3(nginx32_scan_pattern)\intro_pattern.log' '..\log\7-23-4(10elastic_hlist)\out_total.log'

label = []

dictArr = []

x_name = []

for i in range(1, len(sys.argv)):
    inFile = open(sys.argv[i], 'r')
    dictArr.append({})
    while True:
        curLine = inFile.readline()
        if curLine == "":
            break
        curArr = curLine.strip('\n').split()
        print(curArr)
        if 'meta' in curArr:
            # scale.append(int(curArr[1]))
            x_name.append(curArr[1])
            continue

        curIdx = curArr[0]
        curCnt = int(curArr[-1])

        if curIdx not in label:
            label.append(curIdx)

        if curIdx not in dictArr[-1]:
            dictArr[-1][curIdx] = curCnt
        else:
            dictArr[-1][curIdx] += curCnt

localThreshold = 10

pltIdxBase = (len(sys.argv)-1)*100+10
barWidth = 0.75
x=np.arange(len(label))
lnLabel = []
for idx in label:
    numIdx = int(idx)
    if numIdx == 0:
        lnLabel.append(str(numIdx))
    else:
        lnLabel.append("$2^{%d}$" % (log(numIdx,2)))

plt.figure(figsize=(12,6))

for i in range(1, len(sys.argv)):
    plt.subplot(pltIdxBase+i)
    curArr = []
    for idx in label:
        if idx in dictArr[i-1]:
            curArr.append(dictArr[i-1][idx]/100000.0)
        else:
            curArr.append(0)
    plt.bar(x[:localThreshold+2], curArr[:localThreshold+2], barWidth, color='#1f497d', label='Minor Pattern')
    plt.bar(x[localThreshold+2:], curArr[localThreshold+2:], barWidth, color='#C00000', label='Major Pattern')

    if i == 1:
        plt.text(-1, 5.77, r'$\times10^{5}$',fontsize=18)
    else:
        plt.text(-1, 9.35, r'$\times10^{5}$',fontsize=18)



    # def formatnum(x, pos):
    #     num = scale[i-1]
    #     return '$%.1f$' % (x/num)
    # formatter = FuncFormatter(formatnum)
    # plt.gca().yaxis.set_major_formatter(formatter)
    # plt.text(0, 1.95, r'x 10$^{%d}$'%(int(log(scale[i-1],10))),fontsize=15)

    # matplotlib.rcParams.update({'font.size': 16})#设置左上角标签大小
    # xfmt = ScalarFormatter(useMathText=True)
    # xfmt.set_powerlimits((0, 0))
    # plt.gca().yaxis.set_major_formatter(xfmt)
    
    # if i == 1:
    #     plt.gca().yaxis.set_major_locator(MultipleLocator(5000))
    #     plt.ylim(0,15000)

    plt.legend(fontsize=20, loc='center left')
    plt.xticks(x,lnLabel,fontsize=17)
    plt.yticks(fontsize=20)
    plt.xlabel('Number of pages associated with the pattern', fontsize=26)
    if i == 1:
        plt.text(-1, 4.70, r'$Nginx_{\times32}$',fontsize=20)
    else:
        plt.text(-1, 7.36, r'$Elasticsearch_{\times10}$',fontsize=20)
    # plt.xlabel(x_name[i-1], fontsize=26)
    plt.ylabel('Frequancy', fontsize=26)
    plt.subplots_adjust(left=0.07, right=0.99, top=0.96, bottom=0.12, hspace=0.36)

plt.savefig('mem_pattern.pdf')
plt.show()



