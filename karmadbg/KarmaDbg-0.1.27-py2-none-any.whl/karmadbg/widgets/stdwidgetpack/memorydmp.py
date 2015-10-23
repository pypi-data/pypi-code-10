import string

from PySide.QtGui import *
from PySide.QtCore import *
from karmadbg.uicore.async import async
from karmadbg.uicore.basewidgets import NativeDataViewWidget


def getWord(bytes):
    return bytes.next() + ( bytes.next() << 8 )


def getDWord(bytes):
    return getWord(bytes) + ( getWord(bytes) << 16 )

def getQWord(bytes):
    return getDWord(bytes) + ( getDWord(bytes) << 32 )


class DumpView(QTextEdit):

    offsetFormats = [
        "Not Visible", "Absolute" , "Relative"  #, "Symbol"
        ]

    formats = [
        "Not Visible", "Byte Hex", "Word Hex", "Dword Hex", "QWord Hex", "Text"
        ]

    def __init__(self, uimanager, parent = None):
        super(DumpView, self).__init__(parent)
        self.uimanager = uimanager
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setAcceptDrops(False)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.leftFormatIndex = self.getFormatIndex("Byte Hex")
        self.rightFormatIndex = self.getFormatIndex("Text")
        self.offsetFormatIndex = self.getOffsetFormatIndex("Absolute")
        self.lineCount = 0
        self.startOffset = 0
        self.currentOffset = 0

    def getFormatIndex(self, format):
        return self.formats.index(format)

    def getOffsetFormatIndex(self, format):
        return self.offsetFormats.index(format)

    def getVisibleLineCount(self):
        cursor = self.textCursor()
        fontMetric = QFontMetrics( cursor.charFormat().font()) 
        lineHeight = fontMetric.height()
        return self.height() / lineHeight

    def getByteHexLine(self, bytes):
        text = ""
        for b in bytes:
            if text != "":
               text += " "
            text += "%02x" % b
        return text

    def getWordHexLine(self, bytes):
        text = ""
        byteiter = iter(bytes)
        for i in range(8):
            if text != "":
                text += " "
            text += "%04x" % getWord(byteiter)
        return text

    def getDWordHexLine(self, bytes):
        text = ""
        byteiter = iter(bytes)
        for i in range(4):
            if text != "":
                text += " "
            text += "%08x" % getDWord(byteiter)
        return text

    def getQWordHexLine(self, bytes):
        text = ""
        byteiter = iter(bytes)
        for i in range(2):
            if text != "":
                text += " "
            text += "%016x" % getQWord(byteiter)
        return text


    def getTextLine(self, bytes):
        text = ""
        for b in bytes:
            c = chr(b)
            if c in string.printable and not c in string.whitespace:
                text += c
            else:
                text += "."
        return text

    def getOffsetText(self, offset, line):
        return {0 : lambda x, y: "",  1 : lambda x, y: "%0x" % (offset + line*16), 2 : lambda x, y: "%04x" % (offset - self.startOffset + line*16) }[self.offsetFormatIndex](offset, line)

    def getLeftPaneText(self, memdmp, line):
        return {
            0 : lambda x: "", 
            1 : self.getByteHexLine,
            2 : self.getWordHexLine,
            3 : self.getDWordHexLine,
            4 : self.getQWordHexLine,
            5 : self.getTextLine 
        }[self.leftFormatIndex](memdmp[ line*16 : ( line+1)*16 ]) 

    def getRightPaneText(self, memdmp, line):
        return {
            0 : lambda x: "", 
            1 : self.getByteHexLine,
            2 : self.getWordHexLine,
            3 : self.getDWordHexLine,
            4 : self.getQWordHexLine,
            5 : self.getTextLine 
        }[self.rightFormatIndex](memdmp[ line*16 : ( line+1)*16 ])

    @async
    def dataUpdate(self, expression):

        self.startOffset = yield( self.uimanager.debugClient.getExpressionAsync(expression) )
        self.currentOffset =  self.startOffset 

        if not self.isVisible():
            return

        self.lineCount = self.getVisibleLineCount() 

        self.viewUpdate()

    @async
    def viewUpdate(self):

        if self.currentOffset == 0:
            return

        rangeLength = self.lineCount * 16
        if rangeLength == 0:
            return

        memdmp = yield( self.uimanager.debugClient.getMemoryAsync(offset = self.currentOffset, length=rangeLength) )

        text = ""

        for line in xrange(self.lineCount):

            offsetText = self.getOffsetText(self.currentOffset, line)
            leftText = self.getLeftPaneText(memdmp, line)
            rightText = self.getRightPaneText(memdmp, line)

            lineText = offsetText
            if lineText != "":
                if  leftText != "":
                    lineText += " | " + leftText
            else:
                lineText = leftText


            if lineText != "":
                if rightText != "":
                    lineText += " | " + rightText
            else:
                lineText = rightText

            text += lineText + "\n"

        self.setPlainText(text)


    def resizeEvent (self, resizeEvent):

        super(DumpView, self).resizeEvent(resizeEvent)

        lineCount = self.getVisibleLineCount() 

        if self.lineCount != lineCount:
           self.lineCount = lineCount
           self.viewUpdate()

    def showEvent(self, event):

        super(DumpView, self).showEvent(event)

        lineCount = self.getVisibleLineCount() 

        if self.lineCount != lineCount:
           self.lineCount = lineCount
           self.viewUpdate()

    def keyPressEvent(self,event):

        lineCount = self.getVisibleLineCount()

        if event.key() == Qt.Key_Up:
            self.currentOffset -= 0x10
            self.viewUpdate()
            return

        if event.key() == Qt.Key_Down:
            self.currentOffset += 0x10
            self.viewUpdate()
            return

        if event.key() == Qt.Key_PageUp:
            self.currentOffset -= lineCount * 0x10
            self.viewUpdate()
            return

        if event.key() == Qt.Key_PageDown:
            self.currentOffset += lineCount * 0x10
            self.viewUpdate()
            return

        super(DumpView, self).keyPressEvent(event)

    def wheelEvent( self, wheelEvent ):
        numSteps = wheelEvent.delta() / 0x10
        self.currentOffset -= numSteps * 0x10
        self.viewUpdate()


    def setLeftPaneFormat(self, index):
        self.leftFormatIndex = index
        self.viewUpdate()

    def setRightPaneFormat(self, index):
        self.rightFormatIndex = index
        self.viewUpdate()

    def setOffsetPaneFormat(self, index):
        self.offsetFormatIndex = index
        self.viewUpdate()


class MemoryDmpWidget(NativeDataViewWidget):

    def __init__(self, widgetSettings, uimanager):
        super(MemoryDmpWidget,self).__init__(uimanager)
        self.uimanager = uimanager

        frame = QFrame(parent=self)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        self.dumpView= DumpView(uimanager)

        self.exprEdit = QLineEdit()
        self.exprEdit.setText("@$scopeip")
        self.exprEdit.returnPressed.connect(self.dataUpdate)
        hlayout.addWidget(self.exprEdit)

        label = QLabel("Offset:")
        hlayout.addWidget(label)

        self.offsetCombo = QComboBox()
        for format in DumpView.offsetFormats:
            self.offsetCombo.addItem(format)
        self.offsetCombo.setCurrentIndex(self.dumpView.offsetFormatIndex)
        self.offsetCombo.currentIndexChanged.connect(lambda x : self.dumpView.setOffsetPaneFormat( self.offsetCombo.currentIndex() ) )
        hlayout.addWidget(self.offsetCombo)

        label = QLabel("Left:")
        hlayout.addWidget(label)

        self.leftCombo = QComboBox()
        for format in DumpView.formats:
            self.leftCombo.addItem(format)
        self.leftCombo.setCurrentIndex( self.dumpView.leftFormatIndex )
        self.leftCombo.currentIndexChanged.connect(lambda x : self.dumpView.setLeftPaneFormat( self.leftCombo.currentIndex() ) )
        hlayout.addWidget(self.leftCombo)


        label = QLabel("Right:")
        hlayout.addWidget(label)

        self.rightCombo = QComboBox()
        for format in DumpView.formats:
            self.rightCombo.addItem(format)
        self.rightCombo.setCurrentIndex( self.dumpView.rightFormatIndex )
        self.rightCombo.currentIndexChanged.connect(lambda x : self.dumpView.setRightPaneFormat( self.rightCombo.currentIndex() ) )
        hlayout.addWidget(self.rightCombo)

        hlayout.setSpacing(4)
        hlayout.setContentsMargins(0,0,0,0)
        vlayout.addLayout(hlayout)
        #self.hexTextEdit.setStyleSheet("border: 0px;")
        vlayout.addWidget(self.dumpView)
        vlayout.setSpacing(4)
        vlayout.setContentsMargins(4,4,4,4)
        frame.setLayout(vlayout)
        
        self.setWindowTitle("Memory")
        self.setWidget(frame)
        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)

    def dataUpdate(self):
        self.dumpView.dataUpdate(self.exprEdit.text())








#class MemoryDmpWidget(NativeDataViewWidget):

#    def __init__(self, widgetSettings, uimanager):
#        super(MemoryDmpWidget,self).__init__(uimanager)
#        self.uimanager = uimanager

#        frame = QFrame(parent=self)

#        vlayout = QVBoxLayout()
#        hlayout = QHBoxLayout()
#        self.exprEdit = QLineEdit()
#        self.exprEdit.returnPressed.connect(self.dataUpdate)
#        hlayout.addWidget(self.exprEdit)
#        self.combo = QComboBox()
#        self.combo.addItem("Byte")
#        self.combo.addItem("Byte Signed")
#        self.combo.addItem("Byte Hex")
#        self.combo.addItem("Byte Char")
#        self.combo.currentIndexChanged.connect(lambda x : self.dataUpdate())
#        hlayout.addWidget(self.combo)
#        hlayout.setSpacing(4)
#        hlayout.setContentsMargins(0,0,0,0)
#        vlayout.addLayout(hlayout)
#        self.hexTextEdit = QPlainTextEdit()
#        self.hexTextEdit.setReadOnly(True)
#        #self.hexTextEdit.setStyleSheet("border: 0px;")
#        vlayout.addWidget(self.hexTextEdit)
#        vlayout.setSpacing(4)
#        vlayout.setContentsMargins(4,4,4,4)
#        frame.setLayout(vlayout)
        
#        self.setWindowTitle("Memory")
#        self.setWidget(frame)
#        self.uimanager.mainwnd.addDockWidget(Qt.TopDockWidgetArea, self)

#    def dataUnavailable(self):
#        self.hexTextEdit.setPlainText("")

#    @async
#    def dataUpdate(self):
#        memdmp = []
#        expr = self.exprEdit.text()
#        if expr:
#            if self.combo.currentIndex() == 0:
#                memdmp = yield( self.uimanager.debugClient.callServerAsync(getBytes, expr, 0x1000) )
#                if memdmp:
#                    text = reduce(lambda x, y: x + "%d " % y, memdmp, "")
#                    self.hexTextEdit.setPlainText(text)
#            if self.combo.currentIndex() == 1:
#                memdmp = yield( self.uimanager.debugClient.callServerAsync(getSignBytes, expr, 0x1000) )
#                if memdmp:
#                    text = reduce(lambda x, y: x + "%d " % y, memdmp, "")
#                    self.hexTextEdit.setPlainText(text)
#            if self.combo.currentIndex() == 2:
#                memdmp = yield( self.uimanager.debugClient.callServerAsync(getBytes, expr, 0x1000) )
#                if memdmp:
#                    text = reduce(lambda x, y: x + "%02X " % y, memdmp, "")
#                    self.hexTextEdit.setPlainText(text)
#            if self.combo.currentIndex() == 3:
#                memdmp = yield( self.uimanager.debugClient.callServerAsync(getChars, expr, 0x1000) )
#                if memdmp:
#                    text = reduce(lambda x, y: x + "%s " % ( "?" if ord(y) < 32 else y ), memdmp, "")
#                    self.hexTextEdit.setPlainText(text)

#        if memdmp == []:
#            self.hexTextEdit.setPlainText("")
#        if memdmp == None:
#            self.hexTextEdit.setPlainText("Unavailable memory")

#def getBytes(expr,length):

#    import pykd

#    try:
#        exprVal = pykd.expr(expr)
#    except pykd.DbgException:
#        return None

#    try:
#        return pykd.loadBytes(pykd.addr64(exprVal),length)
#    except pykd.MemoryException:
#        return None

#def getSignBytes(expr,length):

#    import pykd

#    try:
#        exprVal = pykd.expr(expr)
#    except pykd.DbgException:
#        return None

#    try:
#        return pykd.loadSignBytes(pykd.addr64(exprVal),length)
#    except pykd.MemoryException:
#        return None

#def getChars(expr,length):
#    import pykd

#    try:
#        exprVal = pykd.expr(expr)
#    except pykd.DbgException:
#        return None

#    try:
#        return pykd.loadChars(pykd.addr64(exprVal),length)
#    except pykd.MemoryException:
#        return None


