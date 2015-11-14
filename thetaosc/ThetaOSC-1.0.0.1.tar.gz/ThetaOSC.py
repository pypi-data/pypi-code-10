#!python
#-*- coding:utf-8 -*-
"""
  A module to control Ricoh Theta-S based on OSC(Open Sperical Camera)API
  aka, Richo Theta API-2.
  https://developers.theta360.com/ja/docs/v2/api_reference/
  https://developers.google.com/streetview/open-spherical-camera/
"""
import traceback

import httplib
import urllib
import json
import struct
import os.path
import types
import thread
import struct
import time
try:
    import  cv2, numpy
    opencv_available=True
except:
    opencv_available=False

class OscException(Exception):
    pass


_Options=(
    "aperture",
    "_captureInterval",
    "captureMode",
    "_captureNumber", # 0: limitless, 2<= _captureNumber <= 9999
    "dateTimeZone", # YYYY:MM:DD hh:mm:ss+(-)hh:mm
    "exposureCompensation", #-2.0, -1.7, -1.3, -1.0, -0.7, -0.3, 0.0, 0.3, 0.7, 1.0, 1.3, 1.7, 2.0
    "exposureProgram", # 1: manual, 2: Normal, 4: shutterSpeed 9:ISO
    "fileFormat", #
    "_filter", # off: no filter, DR Comp: DR compensation, Noise Reduction:Noise Reduction
    "gpsInfo",
    "_HDMIreso", # L:1920x1080, M: 1280x720, S:720x480
    "iso", # 0: Auto, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600
    "offDelay",  # 30 <= offDelay <= 1800, or 65535=Never
    "remainingPictures",
    "remainingSpace",
    "_remainingVideos",
    "shutterSpeed",
    "_shutterVolume",
    "sleepDelay", # 30 <= offDelay <= 1800, or 65535=Never
    "totalSpace",
    "whiteBalance",# auto/daylight/shade/cludy-daylight/icandescent/_warmWhiteFluorescent/_dayLightFluorescent/_dayWhiteFluorescent//fluorescent/_bulbFlowrescent
    "_wlanChannel", #0,1,6,11
)


class ThetaS:
    port=80
    host="192.168.1.1"
    _jsonHeaders={
            "Content-type": "application/json;charset=utf-8",
            "Accept":"application/json",
        }

    def __init__(self):
        self.connection=httplib.HTTPConnection(self.host,self.port)
        self.commandInprogress=dict()
        
    def connect(self):
        self.connection.connect()
        self.startSession()
        
    def Info(self):
        self.connection.connect()
        self.connection.request("GET","/osc/info")
        res=self.connection.getresponse()
        self.connection.close()
        return json.loads(res.read())

    def State(self):
        self.connection.connect()
        self.connection.request("POST","/osc/state",None, ThetaS._jsonHeaders)
        res=self.connection.getresponse()
        self.connection.close()
        return json.loads(res.read())
        
    def CheckForUpdates(self,
                        stateFingerprint,
                        waitTimeout=None):
        if waitTimeout:
            params=json.dumps(dict(stateFingerprint=stateFingerprint,
                                   waitTimeout=waitTimeout))
        else:
            params=json.dumps(dict(stateFingerprint=stateFingerprint))
        self.connection.connect()
        self.connection.request("POST", "/osc/checkForUpdates", params, ThetaS._jsonHeaders)
        res=self.connection.getresponse()
        self.connection.close()
        return json.loads(res.read())
        
    def __del__(self):
        self.connection.close()

    def _sendOscCommand(self,
                        oscCommand,
                        params,
                        headers= _jsonHeaders):
        self.connection.connect()
        self.connection.request("POST",
                                oscCommand,
                                params,
                                headers=headers)
        res=self.connection.getresponse()
        if res.status != 200:
            print res.status, res.reason
        self.connection.close()
        if res:
            rheaders=dict(res.getheaders())
            print res.getheader("content-type")
            if "json" in rheaders["content-type"]: # image/jpeg or video/mp4
                output=json.loads(res.read())
                if output["state"] == "done":
                    if output.has_key("id") and self.commandInprogress.has_key(output["id"]):
                        del self.commandInprogress[output["id"]]
                    if output.has_key("results"):
                        return output["results"]
                    else:
                        return True
                elif output["state"] == "inProgress":
                    self.commandInprogress[output["id"]]=output
                    return False
                else:
                    raise OscException("Command Execution Error %s"%output["error"])
            elif ("image" in rheaders["content-type"]) or ("video" in rheaders["content-type"]):
                return res.read()
            else:
                return res
        else:
            raise OscException("Command Execution Error:No response")
        
    def CommandStatus(self,id):
        parms=json.dumps(dict(id="%s"%id))
        return self._sendOscCommand("/osc/commands/status", parms)
        
    def execute(self, command, parms={},
                headers={"Content-type": "application/json;charset=utf-8",
                         "Accept":"application/json"} ):
        parms=json.dumps(dict(name=command, parameters=parms))
        return self._sendOscCommand("/osc/commands/execute", parms, headers)
        
    def startSession(self):
        res=self.execute("camera.startSession")
        if res:
            self.sessionId=res["sessionId"]
            self.sessionTimeout=res["timeout"]
            return res
        else:
            raise OscException("Failed to start session")
    
    def updateSession(self):
        res=self.execute("camera.updateSession",dict(sessionId=self.sessionId))
        self.sessionId=res["sessionId"]
        return res
        
    def closeSession(self):
        res=self.execute("camera.closeSession",dict(sessionId=self.sessionId))
        return res

    def _finishWlan(self):
        res=self.execute("camera._finishWlan",dict(sessionId=self.sessionId))
        return res
        
    def getOptions(self, optionNames=_Options):
        if (type(optionNames) in types.StringTypes):
            optionNames=[optionNames,]
        options=[opt for opt in optionNames if opt in _Options]
        if options:
            return self.execute("camera.getOptions",dict(sessionId=self.sessionId,
                                              optionNames=options))
        else:
            raise OscException("Invalid Option name(s):%s"%optionNames)
        
    def setOptions(self, options):# type(options) == dict
        for k, v in options.iteritems():
            if unicode(k) not in _Options:
                del options[k]
        print options
        return self.execute("camera.setOptions",
                            dict(sessionId=self.sessionId,
                                 options=options))
    
    def InitiateCapture(self, storageId=0, objectFormatId=0):
        return self.takePicture()
                     
    def takePicture(self):
        res=self.execute("camera.takePicture",dict(sessionId=self.sessionId))
        return res
        
    def _startCapture(self):
        res=self.execute("camera._startCapture",dict(sessionId=self.sessionId))
        return res

    def _stopCapture(self):
        res=self.execute("camera._stopCapture",dict(sessionId=self.sessionId))
        return res

    def listImages(self,entryCount=8, maxSize=160, includeThumb=True):
        res=self.execute("camera.listImages",
                         dict(
                             entryCount=entryCount,
                             maxSize=maxSize,
                             includeThumb=includeThumb))
        entries=res[u"entries"]
        print entries[0]["uri"],type(entries),entryCount-len(entries),
        while res.has_key(u'continuationToken'):
            res=self.execute("camera.listImages",
                             dict(
                                 entryCount=max(entryCount-len(entries),1),
                                 maxSize=maxSize,
                                 continuationToken=res[u'continuationToken'],
                                 includeThumb=includeThumb))
            entries.extend(res[u"entries"])
            print entries[-1]["uri"]
        return entries
    
    def _listAll(self, entryCount=8, detail=True,sort="newest"):
        res=self.execute("camera._listAll",
                         dict(
                             entryCount=entryCount,
                             detail=detail,
                             sort=sort))
        entries=res[u"entries"]
        print entries[0]["uri"],type(entries),entryCount-len(entries),
        while res.has_key(u'continuationToken'):
            res=self.execute("camera._listAll",
                             dict(
                                 entryCount=max(entryCount-len(entries),1),
                                 continuationToken=res[u'continuationToken'],
                                 sort=sort))
            entries.extend(res[u"entries"])
            print entries[-1]["uri"]
        return entries

    def delete(self, fielUri):
        res=self.execute("camera.delete",
                         dict(fileUri=fileUri))
        return res
                         
    def getImage(self, fileUri, _type="thumb"):#_type:"thumb" or "full"
        res=self.execute("camera.getImage",
                         dict(fileUri=fileUri, _type=_type))
        dirs,fname=os.path.split(fileUri)
        if _type=="thumb":
            fn,ext=os.path.splitext(fname)
            fname =fn+"-thumb"+ext
        f=open(fname,"w")
        f.write(res)
        f.close()
        return True
    
    def _getVideo(self, fileUri, _type="full"): # _type:thumb or full
        res=self.execute("camera._getVideo",
                         dict(fileUri=fileUri, type=_type))
        dirs,fname=os.path.split(fileUri)
        if _type=="thumb":
            fn,ext=os.path.splitext(fname)
            fname =fn+"-thumb"+ext
        f=open(fname,"w")
        f.write(res)
        f.close()
        return True
    
    def _getLivePreview(self):
        res=self.execute("camera._getLivePreview",
                         dict(sessionId=self.sessionId))
        print res.getheader("contnt-type"),res.getheaders()
        type=res.msg.type # 'multipart/x-mixed-replace'
        maintype=res.msg.maintype#multipart
        subtype=res.msg.subtype #x-mixed-replace
        plist=res.msg.plist#['boundary=--boundarydonotcross']
        return res

    def getMetadata(self, fileUri, ): # _type:thumb or full
        res=self.execute("camera.getMetadata",
                         dict(fileUri=fileUri))
        return res
    #
    def SetCaptureMode(self,value):
        if (value not in ("image","_video","_liveStreaming")):
            raise OscException("Invaid apture Mode for THETA-S")
        return self.setOptions(dict(captureMode=value))

    def GetCaptureMode(self):
        return self.getOptions("captureMode")

    def SetStillMode(self):
        return self.setOptions(dict(captureMode="image"))

    def SetVideoMode(self):
        return self.setOptions(dict(captureMode="_video"))
    
    def SetTimelapseNumber(self, n):
        return self.setOptions(dict(_captureNumber=n))

    def SetTimelapseInterval(self, interval):# sec
        if not ( 5 < interval <3600):
            raise OscException("TimeLaspInterval Out-of-range")
        return self.setOptions(dict(_captureInterval=interval))

    def GetTimelapseNumber(self):
        return self.getOptions(["_captureNumber",])

    def GetTimelapseInterval(self):
        return self.getOptions(["_captureInterval",])

    def GetAndSaveObject(self,entry):
        print entry
        if entry.has_key(u"recordTime"):
            self._getVideo(entry["uri"],"thumb")
            self._getVideo(entry["uri"],"full")
        else:
            self.getImage(entry["uri"],"thumb")
            self.getImage(entry["uri"],"full")
                
    def GetAndSaveAllObjects(self):
        objects=self._listAll()
        for entry in objects:
            print entry
            self.GetAndSaveObject(entry)

def showLivePreview(dev):
    res=dev._getLivePreview()
    boundary=res.msg.plist[0].split("=")[1]
    f=os.fdopen(res.fileno(),"r")
    while not f.closed:
        #print "---"
        nextline=f.readline()
        while (boundary not in nextline):
            nextline=f.readline()
        content_type=f.readline()
        content_size=f.readline()
        #print nextline, content_type,content_size
        f.readline() # skip over null line
        size=int(content_size.split(':')[1])
        size +=4
        raw=f.read(size)
        buf=numpy.array(struct.unpack("%dB"%size,raw),dtype=numpy.uint8)
        img=cv2.imdecode(buf, cv2.IMREAD_COLOR)
        #print size, len(img)
        cv2.imshow("preview", img)
        key=cv2.waitKey(20) & 0xff
        #print key
        if (key > 0) and (key == ord('q')):
            f.close()
        elif (key > 0) and (key == ord('p')):
            f.close()
            res.close()
            dev.takePicture()
            cv2.waitKey(8000) # should be replaced with the routine to wait for the service
            res=dev._getLivePreview() 
            boundary=res.msg.plist[0].split("=")[1]
            f=os.fdopen(res.fileno(),"r")
        else:
            cv2.waitKey(20)
            continue
    f.close()
    res.close()
    return

def CaptureTest(n=1,delay=20):
    import time

    dev=ThetaS()
    dev.startSession()
    for i in xrange(n):
        print "Initiate Capture"
        dev.InitiateCapture(0,0) # Richo theta does not accept any parameters
        while True:
            print "Check for Event"
            evt = dev.CheckForEvent(None)
            if evt == None:
                raise OscException("Capture did not complete")
            if evt.eventcode == PtpValues.StandardEvents.OBJECT_ADDED:
                objectid = evt.params[0]
                break

        if objectid != None:
            dev.GetAndSaveObject(objectid)
            try:
                dev.DeleteObject(objectid)
            except:
                raise
                
        if (i < n-1 ):time.sleep(delay)
    
def OpenCaptureTest(n=1,delay=5):
    import time
    dev=ThetaS()
    n=0
    print "Initiate Capture"
    dev.SetStillCaptureMode(3) #TimeLapse mode
    print dev.GetTimelapseNumber(),dev.GetTimelapseInterval()
    dev.InitiateOpenCapture(0,0) # Richo theta does not accept any parameters
    objectids=[]
    i=0
    while True:
        print "Check for Event"
        evt = dev.CheckForEvent(None)
        if evt == None:
            raise Exception("Capture did not complete")
        if evt.eventcode == PtpValues.StandardEvents.CAPTURE_COMPLETE:
            print "Capture Complete transaction id:",evt.params[0]
            transactionid=evt.params[0]
            break
        elif evt.eventcode == PtpValues.StandardEvents.DEVICE_PROP_CHANGED:
            print "Device Property Changed transaction-id:",evt.params[0]
            continue
        elif evt.eventcode == PtpValues.StandardEvents.OBJECT_ADDED:
            print "%d-th Object Added. Object id:%x"%(i,evt.params[0])
            objectids.append(evt.params[0])
            i+=1
            if i < n:
                continue
        else:
            print "event code %x:"%evt.eventcode

    try:
        dev.TerminateOpenCapture(transactionid)
    except PtpException as  e:
        print e
        pass

    dev.SetStillCaptureMode(1) #normal mode
    for objectid in  objectids:
        print "saving object %x into file"%objectid
        dev.GetAndSaveObject(objectid)
        try:
            dev.DeleteObject(objectid)
        except:
            print "failed to download %x"%objectid
            continue
    dev.SetStillCaptureMode(1) # bring it backt to normal mode
    print "Current Still Capture mode:",dev.GetStillCaptureMode()

def DumpDeviceDetail():
    device=ThetaS()
    deviceInfo=device.Info()
    State=device.State()
    options=device.getOptions()
    try:
        print "----------- DEVICE -----------"
        print "StandardVersion: %i" % deviceInfo.StandardVersion
        print "VendorExtensionID: %i (%s)" % (deviceInfo.VendorExtensionID, PtpValues.VendorNameById(deviceInfo.VendorExtensionID))
        print "VendorExtensionVersion: %i" % deviceInfo.VendorExtensionVersion
        print "VendorExtensionDesc: %s" % deviceInfo.VendorExtensionDesc
        print "FunctionalMode: %i (%s)" % (deviceInfo.FunctionalMode, PtpValues.FunctionalModeNameById(deviceInfo.FunctionalMode))
        print "OperationsSupported:\n\t%s" % "\n\t".join([PtpValues.OperationNameById(op, deviceInfo.VendorExtensionID) for op in deviceInfo.OperationsSupported])
        print "EventsSupported:\n\t%s" % "\n\t".join([PtpValues.EventNameById(op, deviceInfo.VendorExtensionID) for op in deviceInfo.EventsSupported])
        print "CaptureFormats:\n\t%s" % "\n\t".join([PtpValues.ObjectFormatNameById(op, deviceInfo.VendorExtensionID) for op in deviceInfo.CaptureFormats])
        print "ImageFormats:\n\t%s" % "\n\t".join([PtpValues.ObjectFormatNameById(op, deviceInfo.VendorExtensionID) for op in deviceInfo.ImageFormats])
        print "Manufacturer: %s" % deviceInfo.Manufacturer
        print "Model: %s" % deviceInfo.Model
        print "DeviceVersion: %s" % deviceInfo.DeviceVersion
        print "SerialNumber: %s" % deviceInfo.SerialNumber

        print
        print "----------- PROPERTIES -----------"
        first = True
        for propertyId in deviceInfo.DevicePropertiesSupported:
            propertyInfo = theta360.GetDevicePropInfo(propertyId)
        
            if not first:
                print
                first = False
            print "PropertyCode: 0x%04x (%s)" % (propertyInfo.PropertyCode, PtpValues.PropertyNameById(propertyInfo.PropertyCode, deviceInfo.VendorExtensionID))
            print "DataType: %s" % PtpValues.SimpleTypeDetailsById(propertyInfo.DataType)[0]
            print "GetSet: %s" % PtpValues.GetSetNameById(propertyInfo.GetSet, deviceInfo.VendorExtensionID)
            try:
                print "FactoryDefaultValue: %s" % propertyInfo.FactoryDefaultValue
            except:
                print "FactoryDefaultValue: ", propertyInfo.FactoryDefaultValue
            try:
                print "CurrentValue: %s" % propertyInfo.CurrentValue
            except:
                print "CurrentValue: ", propertyInfo.CurrentValue
            if propertyInfo.MinimumValue != None:
                print "MinimumValue: %s" % propertyInfo.MinimumValue 
            if propertyInfo.MaximumValue != None:
                print "MaximumValue: %s" % propertyInfo.MaximumValue 
            if propertyInfo.StepSize != None:
                print "StepSize: %s" % propertyInfo.StepSize 
            if propertyInfo.Enumeration != None:
                print "Enumeration:",
                print propertyInfo.Enumeration

        print
        print "----------- STORAGE -----------"
        first = True
        for storageId in theta360.GetStorageIDs():
            storageInfo = theta360.GetStorageInfo(storageId)
        
            if storageInfo == None:
                continue        
            if not first:
                print
                first = False
            print "StorageId: 0x%08x" % storageId
            print "StorageType: %s" % PtpValues.StorageTypeNameById(storageInfo.StorageType, deviceInfo.VendorExtensionID)
            print "FilesystemType: %s" % PtpValues.FilesystemTypeNameById(storageInfo.FilesystemType, deviceInfo.VendorExtensionID)
            print "AccessCapability: %s" % PtpValues.AccessCapabilityNameById(storageInfo.AccessCapability, deviceInfo.VendorExtensionID)
            print "MaxCapacity: %i" % storageInfo.MaxCapacity
            print "FreeSpaceInBytes: %i" % storageInfo.FreeSpaceInBytes
            print "FreeSpaceInImages: %i" % storageInfo.FreeSpaceInImages
            print "StorageDescription: %s" % storageInfo.StorageDescription
            print "VolumeLabel: %s" % storageInfo.VolumeLabel
                
        print
        print "----------- OBJECTS -----------"
        first = True
        for objectHandle in theta360.GetObjectHandles(0xffffffff,0,0):
            objectInfo = theta360.GetObjectInfo(objectHandle)
        
            if not first:
                print
                first = False
            print "ObjectHandle: 0x%08x" % objectHandle
            print "StorageId: 0x%08x" % objectInfo.StorageId
            print "ObjectFormat: %s" % PtpValues.ObjectFormatNameById(objectInfo.ObjectFormat, deviceInfo.VendorExtensionID)
            print "ProtectionStatus: %s" % PtpValues.ProtectionStatusNameById(objectInfo.ProtectionStatus, deviceInfo.VendorExtensionID)
            print "ObjectCompressedSize: %i" % objectInfo.ObjectCompressedSize
            print "ThumbFormat: %s" % PtpValues.ObjectFormatNameById(objectInfo.ThumbFormat, deviceInfo.VendorExtensionID)
            print "ThumbCompressedSize: %i" % objectInfo.ThumbCompressedSize
            print "ThumbPixWidth: %i" % objectInfo.ThumbPixWidth
            print "ThumbPixHeight: %i" % objectInfo.ThumbPixHeight
            print "ImagePixWidth: %i" % objectInfo.ImagePixWidth
            print "ImagePixHeight: %i" % objectInfo.ImagePixHeight
            print "ImageBitDepth: %i" % objectInfo.ImageBitDepth
            print "ParentObjectHandle: 0x%08x" % objectInfo.ParentObjectHandle
            print "AssociationType: %s" % PtpValues.AssociationTypeNameById(objectInfo.AssociationType, deviceInfo.VendorExtensionID)
            print "AssociationDesc: 0x%08x" % objectInfo.AssociationDesc
            print "SequenceNumber: %i" % objectInfo.SequenceNumber
            print "Filename: %s" % objectInfo.Filename
            print "CaptureDate: %s" % objectInfo.CaptureDate
            print "ModificationDate: %s" % objectInfo.ModificationDate
            print "Keywords: %s" % objectInfo.Keywords

            #        STANDARD:SEND_OBJECT_INFO
            #        STANDARD:SEND_OBJECT
            


    except PtpException, e:
        print "PTP Exception: %s" % PtpValues.ResponseNameById(e.responsecode, vendorId)
    except Exception, e:
        print "An exception occurred: %s" % e
        traceback.print_exc()


def testAll():
    import time
    print "Dump device detail"
    DumpDeviceDetail()
    time.sleep(0.05) #  wait for connection closing
    print "\nCapture Test"
    CaptureTest()

if __name__ == "__main__":
    #testAll()
    dev=ThetaS()
    dev.connect()
    dev.takePicture()
    time.sleep(8)
    dev.takePicture()
    time.sleep(8)
    dev.takePicture()


