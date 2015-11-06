# -*- encoding: utf-8 -*-
# Copyright (c) 2015 b<>com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import argparse
from collections import OrderedDict
import csv
import os

from oslo_log import log
from watcher_metering_vsphere.tests._fixtures import FakePuller

LOG = log.getLogger(__name__)

required_drivers = [
    "cpu.coreUtilization",
    "cpu.costop.summation",
    "cpu.cpuentitlement.latest",
    "cpu.demandEntitlementRatio.latest",
    "cpu.entitlement.latest",
    "cpu.idle.summation",
    "cpu.maxlimited.summation",
    "cpu.overlap.summation",
    "cpu.ready.summation",
    "cpu.run.summation",
    "cpu.swapwait.summation",
    "cpu.system.summation",
    "cpu.usage",
    "cpu.usagemhz",
    "cpu.used.summation",
    "cpu.utilization",
    "cpu.wait.summation",
    "disk.busResets.summation",
    "disk.capacity.latest",
    "disk.commands.summation",
    "disk.commandsAborted.summation",
    "disk.deltaused.latest",
    "disk.maxTotalLatency.latest",
    "disk.numberRead.summation",
    "disk.numberWrite.summation",
    "disk.provisioned.latest",
    "disk.scsiReservationConflicts.summation",
    "disk.unshared.latest",
    "disk.usage",
    "disk.used.latest",
    "mem.active",
    "mem.consumed",
    "mem.granted",
    "mem.heap",
    "mem.heapfree",
    "mem.llSwapIn",
    "mem.llSwapOut",
    "mem.llSwapUsed",
    "mem.mementitlement.latest",
    "mem.overhead",
    "mem.shared",
    "mem.sharedcommon",
    "mem.state.latest",
    "mem.swapIn",
    "mem.swapin",
    "mem.swapOut",
    "mem.swapout",
    "mem.swapped",
    "mem.swaptarget",
    "mem.swapunreserved",
    "mem.swapused",
    "mem.sysUsage",
    "mem.unreserved",
    "mem.usage",
    "mem.vmmemctl",
    "mem.vmmemctltarget",
    "mem.zero",
    "mem.zipped.latest",
    "mem.zipSaved.latest",
    "net.broadcastRx.summation",
    "net.broadcastTx.summation",
    "net.droppedRx.summation",
    "net.droppedTx.summation",
    "net.errorsRx.summation",
    "net.errorsTx.summation",
    "net.multicastRx.summation",
    "net.multicastTx.summation",
    "net.packetsRx.summation",
    "net.packetsTx.summation",
    "net.throughput.contention.summation",
    "net.unknownProtos.summation",
    "net.usage",
    "power.energy.summation",
    "sys.diskUsage.latest",
    "sys.heartbeat.latest",
    "sys.heartbeat.summation",
    "sys.osUptime.latest",
    "sys.resourceCpuAllocMax.latest",
    "sys.resourceCpuAllocMin.latest",
    "sys.resourceCpuAllocShares.latest",
    "sys.resourceCpuUsage",
    "sys.resourceFdUsage.latest",
    "sys.resourceMemAllocMax.latest",
    "sys.resourceMemAllocMin.latest",
    "sys.resourceMemAllocShares.latest",
    "sys.resourceMemConsumed.latest",
    "sys.resourceMemCow.latest",
    "sys.resourceMemMapped.latest",
    "sys.resourceMemOverhead.latest",
    "sys.resourceMemShared.latest",
    "sys.resourceMemSwapped.latest",
    "sys.resourceMemTouched.latest",
    "sys.resourceMemZero.latest",
    "sys.uptime.latest",
    "virtualDisk.busResets.summation",
    "virtualDisk.commandsAborted.summation",
    "virtualDisk.largeSeeks.latest",
    "virtualDisk.mediumSeeks.latest",
    "virtualDisk.readIOSize.latest",
    "virtualDisk.readLatencyUS.latest",
    "virtualDisk.readLoadMetric.latest",
    "virtualDisk.readOIO.latest",
    "virtualDisk.smallSeeks.latest",
    "virtualDisk.writeIOSize.latest",
    "virtualDisk.writeLatencyUS.latest",
    "virtualDisk.writeLoadMetric.latest",
    "virtualDisk.writeOIO.latest",
]


def parse_args(default_filepath=""):
    parser = argparse.ArgumentParser(
        description='Generates CSV table containing information '
                    'about each desired/implemented driver'
    )
    parser.add_argument(
        '--vsphere',
        dest='host',
        default="10.10.255.115",
        help='vSphere FQDN or IP address'
    )
    parser.add_argument(
        '--username',
        dest='username',
        default="Administrator@vsphere.local",
        help='vSphere username'
    )
    parser.add_argument(
        '--password',
        dest='password',
        default="R00troot!",
        help='vSphere password'
    )
    parser.add_argument(
        '--format', default="csv",  # or rst
        help='filepath of the output'
    )
    parser.add_argument(
        'filepath', default=default_filepath,
        help='filepath of the output'
    )

    args = parser.parse_args()
    return args


def export_csv(data, headers, filepath):
    csv_data = [{headers[k]: v for k, v in row.items()} for row in data]
    keys = headers.values()
    with open(filepath, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(csv_data)


def export_rst(data, headers, filepath):
    from tabulate import tabulate
    rst_data = [{headers[k]: v for k, v in row.items()} for row in data]
    with open(filepath, 'w') as output_file:
        output_file.write(tabulate(rst_data, headers, tablefmt="grid"))


def main():
    default_filepath = os.path.join(os.getcwd(), "drivers.csv")
    args = parse_args(default_filepath)

    data_puller = FakePuller(
        FakePuller.get_name(),
        FakePuller.get_default_probe_id(),
        FakePuller.get_default_interval(),
        datacenter=args.host,
        username=args.username,
        password=args.password,
    )

    mapping = data_puller.wrapper.get_counter_mapping()

    data = []

    for vsphere_metric_name in required_drivers:
        metric_metadata = mapping[vsphere_metric_name]
        row = dict(
            wm_name="vsphere_{}".format(vsphere_metric_name.replace(".", "_")),
            metric_type=metric_metadata["type"],
            metric_name=vsphere_metric_name,
            metric_unit=metric_metadata["unit"],
            metric_description=metric_metadata["description"],
        )
        data.append(row)

    # old column name --> new vSphere name
    headers_mapping = OrderedDict([
        ("wm_name", "Metric name"),
        ("metric_name", "vSphere Metric name"),
        ("metric_unit", "Metric unit"),
        ("metric_type", "Metric type"),
        ("metric_description", "Description"),
    ])

    if args.format != "csv":
        export_rst(data, headers_mapping, args.filepath)
    else:
        export_csv(data, headers_mapping, args.filepath)

    print("Done.")

if __name__ == '__main__':
    main()
