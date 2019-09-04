import re,os,time
import signal
import threading
from sys import argv
import subprocess as sp
from datetime import datetime

def runShell():

    shellCommand = argv[2]
    sp.call(["sh",shellCommand])

def quit(signum,frame):
    sys.exit()

def sleepMinutes():
    minute = float(argv[1])
    time.sleep(minute * 60)

def writeRunLog():

    timeNow = str(datetime.now())
    timeNow = re.sub("\..*","",timeNow)
    with open(argv[2]+'.run.log','w') as fo:
        fo.write("This job is still running at "+timeNow+'\n')

def process_fun():
    while True:
        writeRunLog()
        sleepMinutes()

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT,quit)
        signal.signal(signal.SIGTERM,quit)
        p = threading.Thread(target = process_fun)
        p.setDaemon(True)
        p.start()
        runShell()
    except Exception as e:
        pass
