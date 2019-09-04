import os
import sys
import shutil
import argparse


#file_path = sys.argv[1]

def generateDir(prefix):

    DirName = prefix+'.runShellDir'
    if os.path.exists(DirName):
        shutil.rmtree(DirName)
    os.mkdir(DirName)

def generateIndivShell(prefix,content,num,flag):

    count = 1
    DirName = os.path.abspath(prefix+'.runShellDir')
    shellList = []
    for i in range(0,len(content),num):
        shellName = 'work.'+'%04d'%count+'.sh'
        shellPath = os.path.join(DirName,shellName)
        shellList.append(shellPath)
        with open(shellPath,'w') as fo:
            write_item = ''.join(list((map(lambda x:x.strip()+' && echo '+flag+'\n',content[i:i+num]))))
            fo.write(write_item)
        count += 1
    return shellList

def generateSubmit(qsubPrefix,shellData,qsubDict):

    writeItem = []
    for i in shellData:
        outDir = os.path.dirname(i)
        if qsubDict["host"]:
            qsubFront = "qsub -clear -cwd -o %s -e %s -l vf=%s,p=%s,h=%s -binding linear:%s -q %s -P %s "%(outDir,outDir,qsubDict['mem'],qsubDict['core'],qsubDict['host'],qsubDict['core'],qsubDict['queue'],qsubDict['project'])
        else:
            qsubFront = "qsub -clear -cwd -o %s -e %s -l vf=%s,p=%s -binding linear:%s -q %s -P %s "%(outDir,outDir,qsubDict['mem'],qsubDict['core'],qsubDict['core'],qsubDict['queue'],qsubDict['project'])
        qsubFront += i +'\n'
        writeItem.append(qsubFront)

    with open(qsubPrefix+'.qsub.sh','w') as fo:
        fo.writelines(writeItem)

parser = argparse.ArgumentParser(description='split shell into small jobs.')
parser.add_argument('shellPath', help='file to be splitd')
parser.add_argument('-mem','--mem', default ='0.5G', help='required mem')
parser.add_argument('-line','--line',type= int,default = 1,help='required split line')
parser.add_argument('-host','--host',help='required host location')
parser.add_argument('-core','--core',default = 1,help='required core')
parser.add_argument('-queue','--queue',default = 'st.q',help='required queue')
parser.add_argument('-project','--project',default = 'P18Z10200N0160',help='required project')
parser.add_argument('-flag','--flag',default = 'This-job-finished!',help='required finished status return')
args = parser.parse_args()
argsDict = {"mem":args.mem,"core":args.core,"queue":args.queue,"project":args.project,"host":args.host}

generateDir(os.path.splitext(args.shellPath)[0])
fh = open(args.shellPath,'r')
a = fh.readlines()
fh.close()
shellPath = generateIndivShell(os.path.splitext(args.shellPath)[0],a,args.line,args.flag)
generateSubmit(os.path.splitext(args.shellPath)[0],shellPath,argsDict)
