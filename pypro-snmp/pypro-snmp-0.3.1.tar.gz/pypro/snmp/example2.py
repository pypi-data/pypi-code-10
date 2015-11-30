__author__ = 'teemu kanstren'

#http://www.mibdepot.com/cgi-bin/getmib3.cgi?i=1&n=UCD-SNMP-MIB&r=f5&f=UCD-SNMP-MIB&v=v2&t=tree

import pypro.snmp.config as config
import pypro.snmp.main as main
from pypro.snmp.oids.simple import *
from pypro.snmp.oids.ram_used import RamUsed
from pypro.snmp.oids.cpu_load_prct import CPULoadPrct
from pypro.snmp.oids.oid import OID_Type

config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = False
config.CSV_ENABLED = True
config.KAFKA_AVRO_ENABLED = False
config.KAFKA_JSON_ENABLED = False
config.INFLUX_ENABLED = True
config.INFLUX_HOST = "192.168.2.165"
config.INFLUX_PORT = 8086
config.PRINT_CONSOLE = True
config.SNMP_AUTH = False

config.SNMP_OIDS.append(OID('1.3.6.1.2.1.1.3.0', 'system_uptime', 'public', '192.168.2.1', 161, 'router', OID_Type.int))
config.SNMP_OIDS.append(SystemCPUTimePrct('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(IdleCPUTimePrct('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(UserCPUTimePrct('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(ProcessorLoad('public', '192.168.2.1', 161, 'router', 196608))
config.SNMP_OIDS.append(CPULoadPrct('public', '192.168.2.1', 161, 'router'))

config.SNMP_OIDS.append(RamTotal('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(RamFree('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(RamUsed('public', '192.168.2.1', 161, 'router'))

config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 1))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 1))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 2))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 2))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 3))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 3))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 4))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 4))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 5))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 5))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 6))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 6))
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 7))
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 7))

main.run_poller()
