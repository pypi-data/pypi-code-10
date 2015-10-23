import pykd
import re
import pkgutil

def getLocalsCount():

    try:
        return len(pykd.getFrame().getParams() + pykd.getFrame().getLocals())
    except pykd.DbgException:
        return []


def getLocal(localIndex,subitems):

    try:

        varName, var = (pykd.getFrame().getParams() + pykd.getFrame().getLocals())[localIndex]

        varPrinter = getMultilinePrinter(varName, var)

        for subitem in subitems:
            varPrinter = varPrinter.getSubPrinter(subitem)

        return (varPrinter.getVarName(), varPrinter.getVarType(), varPrinter.getVarLocation(), varPrinter.getVarShortValue(), varPrinter.getVarSubitems() )

    except pykd.DbgException as e:
        return None


def getTypedVar(varName, subitems):

    try:

        var = pykd.typedVar(varName)
        varPrinter = getMultilinePrinter(varName, var)

        for subitem in subitems:
            varPrinter = varPrinter.getSubPrinter(subitem)

        return (varPrinter.getVarName(), varPrinter.getVarType(), varPrinter.getVarLocation(), varPrinter.getVarShortValue(), varPrinter.getVarSubitems() )

    except pykd.DbgException as e:
        return None


def getMultilinePrinter(varName, var):

    for multilinePrinter in multilinePrinterList:
        if re.match( multilinePrinter[0], var.type().name() ):
           return multilinePrinter[1](varName, var)

    return defaultMultilinePrinter(varName, var)


def defaultMultilinePrinter(varName, var):

    if var.type().isBase():
        return TypedVarPrinter(varName, var)

    if var.type().isUserDefined():
        return StructPrinter(varName, var)

    if var.type().isPointer():
        if var.type().deref().isUserDefined():
            return PtrStructPrinter(varName, var)
        if var.type().deref().isVtbl():
            return PtrVtblPrinter(varName, var)
        return TypedVarPrinter(varName, var)

    if var.type().isArray():
        return ArrayPrinter(varName,var)

    return TypedVarPrinter(varName, var)

def getShortPrinter(var):

    for shortPrinter in shortPrinterList:

        if re.match( shortPrinter[0], var.type().name() ):
            retVal = shortPrinter[1](var)
            if retVal != None:
                return retVal

    return defaultShortPrinter(var)

def defaultShortPrinter(var):

    if var.type().isBase():
        return baseVarPrinter(var)

    if var.type().isPointer():
        return pointerVarPrinter(var)

    if var.type().isArray():
        return "Array"

    if var.type().isUserDefined():
        return "Struct"

    if var.type().isEnum():
        return enumShortPrinter(var)

    return var.type().name()

def baseVarPrinter(var):
    try:
        if var.isInteger():
            return str(long(var))
        else:
            return str(float(var))
    except pykd.MemoryException:
        return "access violation"

def pointerVarPrinter(var):
    addr = var.getAddress()
    if pykd.isValid(addr):
        return hex(pykd.ptrPtr(addr))
    else:
        return "invalid memory (0x%x)" % addr

def enumShortPrinter(var):
    intval = long(var)
    for i in xrange(var.type().getNumberFields()):
        if intval == var.type().field(i):
            return "%d (%s)" % ( intval, var.type().fieldName(i) )
    return "%d (no enum value match)" % intval

class BaseMultilinePrinter(object):

    def __init__(self, varName, varValue):
        self.varName = varName
        self.varValue = varValue

    def getVarName(self):
        return self.varName

    def getVarType(self):
        return ""

    def getVarLocation(self):
        return ""

    def getVarShortValue(self):
        return ""

    def getVarSubitems(self):
        return []

    def getSubPrinter(self, subItemName):
        return None

class LongValuePrinter(BaseMultilinePrinter):

    def __init__(self, varName, varValue):
        super(LongValuePrinter,self).__init__(varName, varValue)

    def getVarShortValue(self):
        return long(self.varValue)

class StrValuePrinter(BaseMultilinePrinter):

    def __init__(self, varName, varValue):
        super(StrValuePrinter,self).__init__(varName, varValue)

    def getVarShortValue(self):
        return str(self.varValue)

class OffsetPrinter(BaseMultilinePrinter):

    def __init__(self, varName, varValue):
        super(OffsetPrinter,self).__init__(varName, varValue)

    def getVarShortValue(self):
        return pykd.findSymbol(self.varValue)

class MemoryInvalidPrinter(BaseMultilinePrinter):

    def __init__(self, varName, badaddress):
        super(MemoryInvalidPrinter,self).__init__(varName, None)

    def getVarShortValue(self):
        return "Invalid memory"

class TypedVarPrinter(BaseMultilinePrinter):

    def __init__(self, varName, varValue):
        super(TypedVarPrinter,self).__init__(varName, varValue)

    def getVarType(self):
        return self.varValue.type().name()

    def getVarShortValue(self):
        return getShortPrinter(self.varValue)

    def getVarLocation(self):
        return hex( self.varValue.getAddress() )

class StructPrinter(TypedVarPrinter):

    def __init__(self, varName, varValue):
        super(StructPrinter,self).__init__(varName, varValue)

    def getVarSubitems(self):
        return map( lambda x,y: (x,y),  [ fieldName for fieldName, fieldType in self.varValue.type().fields() ], xrange(len(self.varValue.type().fields())) )

    def getSubPrinter(self, fieldNumber):
        return getMultilinePrinter(self.varValue.fieldName(fieldNumber), self.varValue.field(fieldNumber))

class PtrStructPrinter(TypedVarPrinter):

    def __init__(self, varName, varValue):
        super(PtrStructPrinter,self).__init__(varName, varValue)

    def getVarSubitems(self):
       fields = self.varValue.type().deref().fields()
       return map( lambda x,y: (x,y),  [ fieldName for fieldName, fieldType in fields ], xrange(len(fields)) )

    def getSubPrinter(self, fieldNumber):
        try:
            fieldName = self.varValue.type().deref().fieldName(fieldNumber)
            return getMultilinePrinter(fieldName, self.varValue.deref().field(fieldNumber))
        except pykd.MemoryException:
            return MemoryInvalidPrinter(fieldName, self.varValue.getAddress())


class PtrVtblPrinter(TypedVarPrinter):

    def __init__(self, varName, varValue):
        super(PtrVtblPrinter,self).__init__(varName, varValue)

    def getVarSubitems(self):
        addr = self.varValue.getAddress()
        if pykd.isValid(addr):
            return [ ( "[%d]" % i, i ) for i in xrange(len(self.varValue.deref())) ]
        else:
            return []

    def getSubPrinter(self, subItemKey):
        arrayElem = self.varValue.deref()[subItemKey]
        return OffsetPrinter("[%d]" % subItemKey, arrayElem)


class ArrayPrinter(TypedVarPrinter):

    def __init__(self, varName, varValue):
        super(ArrayPrinter,self).__init__(varName, varValue)

    def getVarSubitems(self):
        return [ ("[%d]" % d, d) for d in xrange(min(0x100,len(self.varValue))) ]

    def getSubPrinter(self, subItemKey):
        arrayElem = self.varValue[subItemKey]
        return getMultilinePrinter("[%d]" % subItemKey, arrayElem)


shortPrinterList = []

def shortprinter(*typeNames):
    
    def decorator(fn):

        for typeName in typeNames:
            shortPrinterList.append( (typeName,fn,) )

        def wrapper(var):

            return fn(var)

        return wrapper

    return decorator

multilinePrinterList = []

def multilineprinter(*typeNames):

    def decorator(fn):

        for typeName in typeNames:
            multilinePrinterList.append( (typeName,fn,) )

        def wrapper(var):

            return fn(var)

        return wrapper

    return decorator

def registerVarPrinters():
    
    import karmadbg.varprinters

    for loader, module_name, ispkg in pkgutil.iter_modules( karmadbg.varprinters.__path__):
        if not ispkg:
            loader.find_module(module_name).load_module(module_name)
 
registerVarPrinters()





























