import sys
def _PrintErrorAndExit(min,max):
    if max == "":
        sys.exit("This script requires Python version %s or newer" % min)
    else:
        sys.exit("The supported Python version for this script is from %s to %s" % (min,max))

def PyVersionCheck(min,max=""):
    _min = min.split(".")
    for i in range(0,len(_min)):   
        if sys.version_info[i] < int(_min[i]):
            _PrintErrorAndExit(min,max)
    if max == "":
        return
    _max = max.split(".")
    for i in range(0,len(_max)):
        if sys.version_info[i] < int(_max[i]):
            return
        elif sys.version_info[i] > int(_max[i]):
            _PrintErrorAndExit(min,max)