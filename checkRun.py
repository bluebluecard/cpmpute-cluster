import sys
import os
from datetime import datetime

dirPath = sys.argv[2]

waitTime = sys.argv[1]

def compareTime(logFile):

    with open(logFile,'r') as f:
        data = f.readlines()
    logTimeStr = ' '.join(data[0].strip().split(' ')[-2:])
    logTimeFormat = datetime.strptime(logTimeStr,"%Y-%m-%d %H:%M:%S")
    nowTime = datetime.now()
    if (nowTime - logTimeFormat).seconds < 60 * float(waitTime):
        return logFile


for path, dirList, fileList in os.walk(dirPath):

    checkFileLog = [compareTime(os.path.join(path,fileName)) \
         for fileName in fileList if fileName.endswith('run.log') and compareTime(os.path.join(path,fileName))]

for i in checkFileLog:
    print(i)
