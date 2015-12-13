from deterministic_encryption_utils.encryption.VirtualFile import VirtualFile
import os
from encviewfuse_decryptorui.decryptorui.FilenameUtils import FilenameUtils

class SegmentedVirtualFile(VirtualFile):

    def __init__(self, absRootPathNotSegmented):
        super(SegmentedVirtualFile, self).__init__(absRootPathNotSegmented + '.seg.0')
        super(SegmentedVirtualFile, self).closeFileHandle()
        self.fileSegments = SegmentedVirtualFile.__getSegments(absRootPathNotSegmented)
        
    def read(self, offset, size):
        relevantKeys = self.__getFileHandlesForRange(offset, size)

        readData = b''
        for relevantKey in relevantKeys:
            currentSegment = self.fileSegments[relevantKey]
            offsetToUse = offset + len(readData) - relevantKey
            sizeToUse = min(currentSegment.size() - offsetToUse, size - len(readData))
            readData = readData + currentSegment.read(offsetToUse, sizeToUse)
        
        return readData
    
    def size(self):
        highestOffset = max(self.fileSegments.keys())
        return highestOffset + self.fileSegments.get(highestOffset).size()

    def closeFileHandle(self):
        for fileSegment in self.fileSegments.values():
            fileSegment.closeFileHandle()
    
    def __getFileHandlesForRange(self, offset, length):
        availableKeys = sorted(self.fileSegments.keys())
        
        startKey = availableKeys[0]
        for key in availableKeys:
            if key > offset:
                break
            else:
                startKey = key
                
        relevantKeys = list()
        for key in availableKeys:
            if key < startKey:
                continue
            elif key > offset + length:
                break
            else:
                relevantKeys.append(key)
                
        return relevantKeys
    
    @staticmethod
    def __getSegments(absRootPathNotSegmented):
        dirName = os.path.dirname(absRootPathNotSegmented)
        fileName = os.path.basename(absRootPathNotSegmented)
        
        entries = list()
        for entry in os.listdir(dirName):
            name, segment = FilenameUtils.splitSegmentedFileName(entry)
            if name != fileName or segment is None:
                continue
            entries.append(VirtualFile(os.path.join(dirName, entry)))
        entries.sort(key=lambda x: FilenameUtils.splitSegmentedFileName(x.name())[1])
        
        offset = 0
        fileHandles = dict()
        for entry in entries:
            fileHandles[offset] = entry
            offset = offset + entry.size()
        
        return fileHandles