import sys
import os.path

inputFilePath = sys.argv[1]
pathTuple = os.path.split(inputFilePath)
print(pathTuple)

inputFile = open(inputFilePath, 'r')
outputFile = open(os.path.join(pathTuple[0], 'out_'+pathTuple[1]), 'w')


sumDict = {}
cntDict = {}

while True:
    curLine = inputFile.readline()
    if curLine == "":
        break
    elif curLine == "\n":
        outputFile.write("\n")

    curLine = curLine.strip('\n')

    curLineArr = [x for x in curLine.strip('\n').split(' ') if x]

    if len(curLine) == 0:
        continue

    curSum = float(curLineArr[3].strip(','))
    curCnt = float(curLineArr[6].strip(','))

    sumDict[curLineArr[0].strip(':')] = curSum
    cntDict[curLineArr[0].strip(':')] = curCnt
    

    outputFile.write("%s, true_avg = %f\n" % (curLine, curSum/curCnt))

outputFile.write("\n")
outputFile.write("unstable partial rate: %f\n" % (sumDict['unstable_partial_hash_skip']/sumDict['unstable_total']))
outputFile.write("stable partial rate: %f\n" % (sumDict['stable_partial_hash_skip']/sumDict['stable_total']))
outputFile.write("all partial rate: %f\n" % ((sumDict['unstable_partial_hash_skip']+sumDict['stable_partial_hash_skip'])/(sumDict['unstable_total']+sumDict['stable_total'])))
outputFile.write("\n")
outputFile.write("unstable cmp time: %f\n" % (sumDict['unstable_partial_cmp']/cntDict['unstable_partial_cmp']))
outputFile.write("stable cmp time: %f\n" % (sumDict['stable_partial_cmp']/cntDict['stable_partial_cmp']))
outputFile.write("all cmp time: %f\n" % ((sumDict['unstable_partial_cmp']+sumDict['stable_partial_cmp'])/(cntDict['unstable_partial_cmp']+cntDict['stable_partial_cmp'])))

outputFile.close()
inputFile.close()