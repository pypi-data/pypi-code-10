
__doc__ = """register reader for windows nt.
"""


import os

if os.name != "nt": 
   raise SystemError("This is not a windows nt system")


class NTRegReader:

    def __init__(self):
        self.engine = None
        candidates = ["_winreg", "win32"]
        for candidate in candidates:
            if getattr(self, "_try%s"%candidate)(): break
        msg = "No module in %s is found. Don't know how to read register then." % candidates
        if not self.engine: raise msg
        self.bases = (
             self.engine.HKEY_USERS,
             self.engine.HKEY_CURRENT_USER,
             self.engine.HKEY_LOCAL_MACHINE,
             self.engine.HKEY_CLASSES_ROOT)
        return


    def read(self, base, path):
        """read register keys at given base/path. 
        return a dict of registry key:value pairs.
        All names are converted to lowercase.
        """
        try:
            handle = self.OpenKeyEx(base, path)
        except self.Error:
            return {}
        res = {}
        counter = 0
        while True:
            try:
                name, value, type = self.EnumValue(handle, counter)
            except self.Error:
                break
            name = name.lower()
            res[_to_mbcs(name)] = _to_mbcs(value)
            counter = counter + 1
        return res


    def readValue(self, path, key):
        print("read register key %r from %r" % (key, path))
        for base in self.bases:
            res = self.read(base, path)
            if res:
                return res[key]
            continue
        return None


    def _try_winreg(self):
        try:
            import winreg
        except ImportError:
            return False

        
        self.engine = _winreg
        self.OpenKeyEx = winreg.OpenKeyEx
        self.EnumKey = winreg.EnumKey
        self.EnumValue = winreg.EnumValue
        self.Error = winreg.error
        return True

    def _trywin32(self):
        try:
            import win32api
            import win32con
        except ImportError:
            return False

        self.engine = win32con

        self.OpenKeyEx = win32api.RegOpenKeyEx
        self.EnumKey = win32api.RegEnumKey
        self.EnumValue = win32api.RegEnumValue
        self.Error = win32api.error
        return True


def _to_mbcs(s):
    "try encode string using mbcs"  
    enc = getattr(s, "encode", None)
    if enc is not None:
        try:
            s = enc("mbcs")
        except UnicodeError:
            pass
    return s


reader = NTRegReader()
