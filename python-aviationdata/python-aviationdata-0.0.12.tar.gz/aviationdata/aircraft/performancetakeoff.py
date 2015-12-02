import csv

class EntryTakeOff(object):
    weight = None
    da = None
    groundroll = None
    groundrollObstacle = None
    _oat = None
    _pa = None

    def __init__(self, weight=None, da=None, groundroll=None, groundrollObstacle=None, pa=None, oat=None):
        super(EntryTakeOff, self).__init__()
        self.weight = weight
        self.da = da
        self.groundroll = groundroll
        self.groundrollObstacle = groundrollObstacle
        if not self.da:
            self.pa = pa
            self.oat = oat

    def __str__(self):
        return ", ".join(["Weight %.0f" % self.weight, "DA %.0f" % self.da, "Groundroll %.1f" % self.groundroll, "Groundroll 50ft Obs %.1f" % self.groundrollObstacle])

    @property
    def oat(self):
        return self._oat

    @oat.setter
    def oat(self, value):
        self._oat = value
        self._calcDa()

    @property
    def pa(self):
        return self._pa

    @pa.setter
    def pa(self, value):
        self._pa = value
        self._calcDa()

    def _calcDa(self):
        self.da = 0.0
        if self.pa and self.oat:
            self.da = int(self.pa) + int((self.oat - (15 - ((self.pa / 1000) * 2))) * 120)

class PerformanceTakeOff(object):
    entries = None

    def __init__(self):
        super(PerformanceTakeOff, self).__init__()
        self.entries = []

    def addEntry(self, entry):
        self.entries.append(entry)

    def importCsv(self, file):
        with open(file, 'r') as f:
            c = csv.DictReader(f)
            for row in c:
                self.addEntry(EntryTakeOff(
                    weight=float(row['Weight']),
                    oat=float(row['OAT']),
                    pa=float(row['PA']),
                    groundroll=float(row['GroundRoll']),
                    groundrollObstacle=float(row['at 50 ft AGL'])
                ))

    def getPerformance(self, weight, **kwargs):
        da = kwargs['da'] if 'da' in kwargs else None
        if not da:
            pa = kwargs['pa'] if 'pa' in kwargs else None
            alt = kwargs['alt'] if 'alt' in kwargs else None
            oat = kwargs['oat'] if 'oat' in kwargs else None
            hpa = kwargs['hpa'] if 'hpa' in kwargs else None
            if pa and oat:
                da = int(pa) + int((oat - (15 - ((pa / 1000) * 2))) * 120)
            if alt and oat and hpa:
                pa = int(float(alt) + 1000.0 * (1013.25 - float(hpa)))
                da = pa + int((oat - (15 - ((pa / 1000) * 2))) * 120)

        if not da:
            raise Exception("Sorry, have not enough information to calculate DA. Please provide da directly or pa, alt, oat, hpa")

        leftLower_entries = filter(lambda z: z.weight <= weight and z.da <= da, self.entries)
        rightLower_entries = filter(lambda z: z.weight >= weight and z.da <= da, self.entries)
        leftHigher_entries = filter(lambda z: z.weight <= weight and z.da >= da, self.entries)
        rightHigher_entries = filter(lambda z: z.weight >= weight and z.da >= da, self.entries)

        leftLower = None
        rightLower = None
        leftHigher = None
        rightHigher = None
        if leftLower_entries:
            leftLower = reduce(lambda x, y: x if x.weight >= y.weight and x.da >= y.da else y, leftLower_entries)
        if rightLower_entries:
            rightLower = reduce(lambda x, y: x if x.weight <= y.weight and x.da >= y.da else y, rightLower_entries)
        if leftHigher_entries:
            leftHigher = reduce(lambda x, y: x if x.weight >= y.weight and x.da <= y.da else y, leftHigher_entries)
        if rightHigher_entries:
            rightHigher = reduce(lambda x, y: x if x.weight <= y.weight and x.da <= y.da else y, rightHigher_entries)

        if leftLower and rightLower:
            lower = EntryTakeOff(weight=weight, da=leftLower.da,
                             groundroll=(rightLower.groundroll-leftLower.groundroll)/(rightLower.weight-leftLower.weight)*(weight-leftLower.weight)+leftLower.groundroll,
                             groundrollObstacle=(rightLower.groundrollObstacle-leftLower.groundrollObstacle)/(rightLower.weight-leftLower.weight)*(weight-leftLower.weight)+leftLower.groundrollObstacle

            )
        else:
            lower = leftLower if leftLower else rightLower
        if leftHigher and rightHigher:
            higher = EntryTakeOff(weight=weight, da=leftHigher.da,
                             groundroll=(rightHigher.groundroll-leftHigher.groundroll)/(rightHigher.weight-leftHigher.weight)*(weight-leftHigher.weight)+leftHigher.groundroll,
                             groundrollObstacle=(rightHigher.groundrollObstacle-leftHigher.groundrollObstacle)/(rightHigher.weight-leftHigher.weight)*(weight-leftHigher.weight)+leftHigher.groundrollObstacle

            )
        else:
            higher = leftHigher if leftHigher else rightHigher

        if lower and higher:
            return EntryTakeOff(weight=weight, da=da,
                            groundroll=(higher.groundroll-lower.groundroll)/(higher.da-lower.da)*(da-lower.da)+lower.groundroll,
                            groundrollObstacle=(higher.groundrollObstacle-lower.groundrollObstacle)/(higher.da-lower.da)*(da-lower.da)+lower.groundrollObstacle
            )
        return None

if __name__ == '__main__':
    pto = PerformanceTakeOff()
    pto.addEntry(EntryTakeOff(weight=530.0,da=1000,groundroll=160,groundrollObstacle=180))
    pto.addEntry(EntryTakeOff(weight=530.0,da=2000,groundroll=180,groundrollObstacle=200))
    pto.addEntry(EntryTakeOff(weight=530.0,da=3000,groundroll=200,groundrollObstacle=220)) # lower left
    pto.addEntry(EntryTakeOff(weight=530.0,da=4000,groundroll=220,groundrollObstacle=240)) # higher right
    pto.addEntry(EntryTakeOff(weight=530.0,da=5000,groundroll=240,groundrollObstacle=260))
    pto.addEntry(EntryTakeOff(weight=530.0,da=6000,groundroll=246,groundrollObstacle=280))

    pto.addEntry(EntryTakeOff(weight=580.0,da=1000,groundroll=180,groundrollObstacle=200))
    pto.addEntry(EntryTakeOff(weight=580.0,da=2000,groundroll=200,groundrollObstacle=220))
    pto.addEntry(EntryTakeOff(weight=580.0,da=3000,groundroll=220,groundrollObstacle=240)) # lower right
    pto.addEntry(EntryTakeOff(weight=580.0,da=4000,groundroll=240,groundrollObstacle=260)) # higher right
    pto.addEntry(EntryTakeOff(weight=580.0,da=5000,groundroll=260,groundrollObstacle=280))
    pto.addEntry(EntryTakeOff(weight=580.0,da=6000,groundroll=280,groundrollObstacle=300))

    pto.addEntry(EntryTakeOff(weight=630.0,da=1000,groundroll=200,groundrollObstacle=220))
    pto.addEntry(EntryTakeOff(weight=630.0,da=2000,groundroll=220,groundrollObstacle=240))
    pto.addEntry(EntryTakeOff(weight=630.0,da=3000,groundroll=240,groundrollObstacle=260))
    pto.addEntry(EntryTakeOff(weight=630.0,da=4000,groundroll=260,groundrollObstacle=280))
    pto.addEntry(EntryTakeOff(weight=630.0,da=5000,groundroll=280,groundrollObstacle=300))
    pto.addEntry(EntryTakeOff(weight=630.0,da=6000,groundroll=300,groundrollObstacle=320))

    #x = pto.getPerformance(weight=545.0, da=3200)
    #print "--------------"
    #print x

    pto2 = PerformanceTakeOff()
    pto2.importCsv('tecnam.csv')
    x =  pto2.getPerformance(weight=545, alt=1788, hpa=1013.25, oat=13)
    print "--------------"
    print x
