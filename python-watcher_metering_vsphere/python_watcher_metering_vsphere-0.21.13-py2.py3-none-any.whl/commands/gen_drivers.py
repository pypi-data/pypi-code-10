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
import os

from oslo_log import log
from watcher_metering_vsphere.tests._fixtures import FakePuller

LOG = log.getLogger(__name__)


header = """# -*- encoding: utf-8 -*-
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

from oslo_log import log
from watcher_metering_vsphere.base import BaseVSphereMetricPuller

LOG = log.getLogger(__name__)
"""

template = """
class {metric_cls_name}(BaseVSphereMetricPuller):
    {metric_description}
    metric_type = "{metric_type}"
    metric_name = "{metric_name}"
    metric_unit = "{metric_unit}"
    pulling_interval = 10
"""

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
        description='Generates a class implemetation for each desired driver'
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
        'filepath', default=default_filepath,
        help='filepath of the output'
    )

    args = parser.parse_args()
    return args


def format_docstring(docstring):
    quoted_doc = "\"\"\"{0}\"\"\"".format(docstring)
    max_line_length = 79 - 4  # -4 for indentation

    if len(quoted_doc) <= max_line_length:
        return quoted_doc  # short enough so we return it as is

    word_split_doc = quoted_doc.split(" ")

    start_line_idx = 0
    lines = []

    for idx, _ in enumerate(word_split_doc):
        tmp_line = " ".join(word_split_doc[start_line_idx:idx + 1])

        if idx == len(word_split_doc) - 1:  # last word
            if len(tmp_line) < max_line_length:
                # last word fits in the last line
                line = " ".join(word_split_doc[start_line_idx:idx + 1])
                lines.append(line)
            else:
                # last word does not fit in the last line
                line = " ".join(word_split_doc[start_line_idx:idx])
                lines.append(line)
                lines.append(word_split_doc[-1])
            break
        elif len(tmp_line) < max_line_length:
            continue
        line = " ".join(word_split_doc[start_line_idx:idx])
        start_line_idx = idx

        lines.append(line)

    if len(lines):
        last_line = lines.pop()
        last_line = last_line[:len(last_line) - 3]  # remove the end quotes
        lines.append(last_line)
        lines.append("\"\"\"")  # End of docstring on a new line

    return "\n    ".join([l for l in lines if l])


def main():
    default_filepath = os.path.join(os.getcwd(), "generated_drivers.py")
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

    output = "{0}".format(header)

    for vsphere_metric_name in required_drivers:
        metric_metadata = mapping[vsphere_metric_name]
        group_and_sample = vsphere_metric_name.split(".")
        cls_name = "".join(
            ["VSphere"] +
            [part[0].upper() + part[1:]
             for part in group_and_sample if part]
        )

        description = format_docstring(metric_metadata["description"])

        output += "\n"
        output += template.format(
            metric_cls_name=cls_name,
            metric_type=metric_metadata["type"],
            metric_name=vsphere_metric_name,
            metric_unit=metric_metadata["unit"],
            metric_description=description,
        )

    with open(args.filepath, "w") as gen_file:
        gen_file.write(output)

    print("Done.")

if __name__ == '__main__':
    main()
