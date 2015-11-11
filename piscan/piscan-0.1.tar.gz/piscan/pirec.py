#!/usr/bin/env python
import serial
import subprocess
import time
import pika
import os
import datetime
import logging
import logging.handlers
import argparse
import sys


LOG_FILENAME = "/tmp/piscrape2.log"
LOG_LEVEL = logging.DEBUG  # Could be e.g. "DEBUG" or "WARNING"

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("*** Starting PiScrape.Py ***")
#logger.info("*** FORCED SYSTEM EXIT ***")
#sys.exit()

port = "/dev/ttyUSB0"
#port = '/dev/ttyACM0'
baudrate = 115200

#global sqlch, parsed
serTimeout = float(.005) 
#test = "GLG"
TGIDold = 0
metadata = ''

try:
    serialFromScanner = serial.Serial(port, baudrate, timeout=serTimeout)
    serialFromScanner.bytesize = serial.EIGHTBITS #number of bits per bytes
    serialFromScanner.parity = serial.PARITY_NONE #set parity check: no parity
    serialFromScanner.stopbits = serial.STOPBITS_ONE #number of stop bits
    serialFromScanner.timeout = 1            #non-block read
    serialFromScanner.xonxoff = False     #disable software flow control
    serialFromScanner.rtscts = False     #disable hardware (RTS/CTS) flow control
    serialFromScanner.dsrdtr = False       #disable hardware (DSR/DTR) flow control
except:
    logger.error('*** Failed to open serial port ***', exc_info=True)
serialFromScanner.flushInput()

def getData(test):
    global serBuffer, nextChar, recflag
    global sqlch, parsed
    serBuffer = '' #clear the serBuffer
    nextChar = '' #reset the nextChar marker
    try:
        test = test + '\r\n'
        serialFromScanner.write(test.encode('UTF-8'))
    except:
        logger.error('*** Failed to write data (' + test + ') to serial port ***', exc_info=True)
    time.sleep(.1)

def receiveData():
    if (serialFromScanner.inWaiting() > 0):
        global nextChar, serBuffer
        global sqlch, parsed
        while nextChar != '\r':
            try:
                nextChar = serialFromScanner.read(1).decode('UTF-8')
                serBuffer += nextChar
            except:
                logger.error('*** read failed ***', exc_info=True)

def setrecflag():
    global recflag, frames, seqnum
    recflag = 0
    seqnum = 1
    frames = []

def parseData(pserBuffer):
    global sqlch, parsed, GLGData, rssi, freq, ft, modu, att, pl, name1, name2, name3
    parsed = pserBuffer.split(",")
    stringtest = parsed[0]
    length = len(parsed) 
    if stringtest == "GLG":
        if (length >= 9):
            try:
                ft = parsed[1]
                modu = parsed[2]
                att = parsed[3]
                pl = parsed[4]
                name1 = parsed[5]
                name2 = parsed[6]
                name3 = parsed[7]
                sqlch = parsed[9]
                GLGData = parsed 
            except:
                tempstr = '|'.join(parsed)
                logger.error('*** parse GLG failed  ***' + tempstr, exc_info=True) 
                sqlch = '2'       
#            if (len(sqlch) > 0):
#                print(parsed)        
    if stringtest == "PWR":
        if (length >= 2):
            try:
                rssi = parsed[1] 
                freq = parsed[2] 
            except:
                tempstr = '|'.join(parsed)
                logger.error('*** parse PWR failed  ***' + tempstr, exc_info=True) 
                rssi = '0'
                freq = '0000.0000' 

            if (len(rssi) > 0):
                print(rssi + ' - ' + freq)       
                time.sleep(.1)
                serialFromScanner.flushInput()


global sqlch
sqlch = '1'
setrecflag()


# Get Sequence Number
fl = open("/etc/piscan/seqnum","r")
fr = fl.read()
seqnum = int(float(fr))
fl.close()
wavfn = "/etc/piscan/" + str(seqnum) + ".wav"

while True: 
    time.sleep(.1)
    getData('GLG')
    receiveData()
    parseData(serBuffer)
#    GLGData = parsed
#    print(parsed)        
    if (sqlch == '0'): 
        # Start recording
        if (recflag == 0):
            cmd = ['sox','-r','48000','-c','1','-t','alsa','hw:1,0','-t','wav', wavfn] 
            popen = subprocess.Popen ( cmd )
            starttime = datetime.datetime.now()
            print("* START recording")
            print(GLGData)        
            recflag=1
        if (recflag == 1): 
            #print("* recording")
            print (sqlch + datetime.datetime.now().strftime("%H:%M:%S:%f"))
        getData('PWR')
        receiveData()
        parseData(serBuffer)
    else:
        # Stop recording and save file
        if (recflag == 1): 
            recflag = 0
            #seqnum = seqnum + 1 
            stptime = datetime.datetime.now()
            difference = stptime - starttime
            print("Second: %s", difference.seconds)
            popen.kill()
            print("* DONE recording")

            # Build LameQ Message & Update LameQ
            try:
                a = "1"
                b = "a457529c4fc8ca95e65012a109661826"
                c = str(seqnum) + ".wav"
                dd = "{0:.2f}".format(difference.microseconds)
                d = str(difference.seconds) + '.' + str(dd)
                d = str(difference.seconds) + '.' + str(difference.microseconds)
                ee = float(freq)/10000
                e = "{0:.4f}".format(ee)         # Freq 0000.0000
                f = name1        # SysSite   || SysSite
                g = name2        # Sys Group || GroupName
                h = name3        # Talk Grp  || ChannelName
                i = "CNV"        # CallSign  || SysType
                j = modu         # Modulation
                k = pl           # PL
                l = starttime.strftime("%Y-%m-%d %H:%M:%S")  # CutTime StrTime  YYYY-MM-DD HH:MM:SS
                m = rssi         # RSSI from Pidl.py
                n = str(seqnum)  # Internal counter from seq file

                message = a + "~" + b + "~" + c + "~" + d + "~" + e + "~" + f + "~" + g + "~" + h + "~" + i + "~" + j + "~" + k + "~" + l + "~" + m + "~" + n + "~~~~~~~~~"
                print (message)
                logger.info("Message creation successgful : " + message )
            except:
                a = a
                logger.info("*** Message creation unsuccessgful "  )


            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='LameQ', durable=True)
                channel.basic_publish(exchange='', routing_key='LameQ', body=message, properties=pika.BasicProperties(delivery_mode = 2,))
                connection.close()
                logger.info("Message queued to LameQ : " + message )
            except:
                a = a
                logger.info("*** Message skipped - connect/publish to queue" )

            seqnum = seqnum + 1 

            fl = open("/etc/piscan/seqnum","w")
            fl.write(str(seqnum))
            wavfn = "/etc/piscan/" + str(seqnum) + ".wav"
            fl.close()





