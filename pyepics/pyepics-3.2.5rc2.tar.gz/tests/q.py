import epics
import debugtime

mfields = ('ACCL', 'ATHM', 'BACC', 'BDST', 'BVEL', 'CARD', 'CNEN', 'DCOF', 'DESC',
'DHLM', 'DIR', 'DLLM', 'DLY', 'DMOV', 'DRBV', 'DTYP', 'DVAL', 'EGU',
'ERES', 'FOFF' 'FOFF', 'FRAC', 'HHSV', 'HIGH', 'HIHI', 'HLM', 'HLS',
'HLSV', 'HOMF', 'HOMR', 'HOPR', 'HSV', 'ICOF', 'JAR', 'JOGF', 'JOGR',
'JVEL', 'LDVL', 'LLM', 'LLS', 'LLSV', 'LOLO', 'LOPR', 'LOW', 'LRLV',
'LRVL', 'LSPG', 'LSV', 'LVAL', 'LVIO', 'MIP', 'MISS', 'MOVN', 'MRES',
'MSTA', 'OFF', 'OMSL', 'OUT', 'PCOF', 'PREC', 'RBV', 'RCNT', 'RDBD',
'RDIF', 'REP', 'RHLS', 'RLLS', 'RLV', 'RMP', 'RRBV', 'RRES', 'RTRY',
'RTYP', 'RVAL', 'RVEL', 'S', 'SBAK', 'SBAS', 'SET', 'SMAX', 'SPMG', 'SREV',
'STAT', 'STOP', 'TDIR', 'TWF', 'TWR', 'TWV', 'UEIP', 'UREV', 'URIP', 'VAL',
'VBAS', 'VELO', 'VERS', 'VMAX')

pvnames = []

for pre, num in (('13IDE:', 20), ('13XRM:', 6), ('13IDA:', 30),
                 ('13BMA:', 10), ('13BMD:', 60), ('13IDC:', 30),
                 ('13BMC:', 20), ('13IDD:', 60)):
    for i in range(num):
        for f in mfields:
            pvnames.append("%sm%i.%s" % (pre, i+1, f))


dt = debugtime.debugtime()
dt.add('Will connect to %i PVs' % len(pvnames))

pvlist = [epics.PV(i, connection_timeout=0.25) for i in pvnames]
dt.add("created PVs")
values = [p.get() for p in pvlist]
dt.add("got values PVs")
f = open('pvdata.out', 'w')
f.write("\n".join(["%s\t%s" % (p.pvname, repr(p.get())) for p in pvlist]))
f.close()
dt.add("wrote values PVs")

for p in pvlist:
    if not p.connected:
        print p.pvname


dt.show()



