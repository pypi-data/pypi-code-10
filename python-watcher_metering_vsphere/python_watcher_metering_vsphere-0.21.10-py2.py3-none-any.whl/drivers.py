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

from oslo_log import log
from watcher_metering_vsphere.base import BaseVSphereMetricPuller

LOG = log.getLogger(__name__)


class VSphereCpuCoreUtilization(BaseVSphereMetricPuller):
    """CPU utilization of the corresponding core (if hyper-threading is
    enabled) as a percentage during the interval (A core is utilized if either
    or both of its logical CPUs are utilized)
    """
    metric_type = "gauge"
    metric_name = "cpu.coreUtilization"
    metric_unit = "%"
    pulling_interval = 10


class VSphereCpuCostopSummation(BaseVSphereMetricPuller):
    """Time the virtual machine is ready to run, but is unable to run due to
    co-scheduling constraints
    """
    metric_type = "delta"
    metric_name = "cpu.costop.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuCpuentitlementLatest(BaseVSphereMetricPuller):
    """Amount of CPU resources allocated to the virtual machine or resource
    pool, based on the total cluster capacity and the resource configuration
    of the resource hierarchy
    """
    metric_type = "cumulative"
    metric_name = "cpu.cpuentitlement.latest"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereCpuDemandEntitlementRatioLatest(BaseVSphereMetricPuller):
    """CPU resource entitlement to CPU demand ratio (in percents)"""
    metric_type = "cumulative"
    metric_name = "cpu.demandEntitlementRatio.latest"
    metric_unit = "%"
    pulling_interval = 10


class VSphereCpuEntitlementLatest(BaseVSphereMetricPuller):
    """CPU resources devoted by the ESX scheduler"""
    metric_type = "cumulative"
    metric_name = "cpu.entitlement.latest"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereCpuIdleSummation(BaseVSphereMetricPuller):
    """Total time that the CPU spent in an idle state"""
    metric_type = "delta"
    metric_name = "cpu.idle.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuMaxlimitedSummation(BaseVSphereMetricPuller):
    """Time the virtual machine is ready to run, but is not run due to maxing
    out its CPU limit setting
    """
    metric_type = "delta"
    metric_name = "cpu.maxlimited.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuOverlapSummation(BaseVSphereMetricPuller):
    """Time the virtual machine was interrupted to perform system services on
    behalf of itself or other virtual machines
    """
    metric_type = "delta"
    metric_name = "cpu.overlap.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuReadySummation(BaseVSphereMetricPuller):
    """Time that the virtual machine was ready, but could not get scheduled to
    run on the physical CPU during last measurement interval
    """
    metric_type = "delta"
    metric_name = "cpu.ready.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuRunSummation(BaseVSphereMetricPuller):
    """Time the virtual machine is scheduled to run"""
    metric_type = "delta"
    metric_name = "cpu.run.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuSwapwaitSummation(BaseVSphereMetricPuller):
    """CPU time spent waiting for swap-in"""
    metric_type = "delta"
    metric_name = "cpu.swapwait.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuSystemSummation(BaseVSphereMetricPuller):
    """Amount of time spent on system processes on each virtual CPU in the
    virtual machine
    """
    metric_type = "delta"
    metric_name = "cpu.system.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuUsage(BaseVSphereMetricPuller):
    """CPU usage as a percentage during the interval"""
    metric_type = "gauge"
    metric_name = "cpu.usage"
    metric_unit = "%"
    pulling_interval = 10


class VSphereCpuUsagemhz(BaseVSphereMetricPuller):
    """CPU usage in megahertz during the interval"""
    metric_type = "gauge"
    metric_name = "cpu.usagemhz"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereCpuUsedSummation(BaseVSphereMetricPuller):
    """Total CPU usage"""
    metric_type = "delta"
    metric_name = "cpu.used.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereCpuUtilization(BaseVSphereMetricPuller):
    """CPU utilization as a percentage during the interval (CPU usage and CPU
    utilization might be different due to power management technologies or
    hyper-threading)
    """
    metric_type = "gauge"
    metric_name = "cpu.utilization"
    metric_unit = "%"
    pulling_interval = 10


class VSphereCpuWaitSummation(BaseVSphereMetricPuller):
    """Total CPU time spent in wait state"""
    metric_type = "delta"
    metric_name = "cpu.wait.summation"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereDiskBusResetsSummation(BaseVSphereMetricPuller):
    """Number of SCSI-bus reset commands issued during the collection
    interval
    """
    metric_type = "delta"
    metric_name = "disk.busResets.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskCapacityLatest(BaseVSphereMetricPuller):
    """Configured size of the datastore"""
    metric_type = "cumulative"
    metric_name = "disk.capacity.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereDiskCommandsSummation(BaseVSphereMetricPuller):
    """Number of SCSI commands issued during the collection interval"""
    metric_type = "delta"
    metric_name = "disk.commands.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskCommandsAbortedSummation(BaseVSphereMetricPuller):
    """Number of SCSI commands aborted during the collection interval"""
    metric_type = "delta"
    metric_name = "disk.commandsAborted.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskDeltausedLatest(BaseVSphereMetricPuller):
    """Storage overhead of a virtual machine or a datastore due to delta disk
    backings
    """
    metric_type = "cumulative"
    metric_name = "disk.deltaused.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereDiskMaxTotalLatencyLatest(BaseVSphereMetricPuller):
    """Highest latency value across all disks used by the host"""
    metric_type = "cumulative"
    metric_name = "disk.maxTotalLatency.latest"
    metric_unit = "ms"
    pulling_interval = 10


class VSphereDiskNumberReadSummation(BaseVSphereMetricPuller):
    """Number of disk reads during the collection interval"""
    metric_type = "delta"
    metric_name = "disk.numberRead.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskNumberWriteSummation(BaseVSphereMetricPuller):
    """Number of disk writes during the collection interval"""
    metric_type = "delta"
    metric_name = "disk.numberWrite.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskProvisionedLatest(BaseVSphereMetricPuller):
    """Amount of storage set aside for use by a datastore or a virtual
    machine
    """
    metric_type = "cumulative"
    metric_name = "disk.provisioned.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereDiskScsiReservationConflictsSummation(BaseVSphereMetricPuller):
    """Number of SCSI reservation conflicts for the LUN during the collection
    interval
    """
    metric_type = "delta"
    metric_name = "disk.scsiReservationConflicts.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereDiskUnsharedLatest(BaseVSphereMetricPuller):
    """Amount of space associated exclusively with a virtual machine"""
    metric_type = "cumulative"
    metric_name = "disk.unshared.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereDiskUsage(BaseVSphereMetricPuller):
    """Aggregated disk I/O rate. For hosts, this metric includes the rates for
    all virtual machines running on the host during the collection
    interval.
    """
    metric_type = "gauge"
    metric_name = "disk.usage"
    metric_unit = "KBps"
    pulling_interval = 10


class VSphereDiskUsedLatest(BaseVSphereMetricPuller):
    """Amount of space actually used by the virtual machine or the datastore"""
    metric_type = "cumulative"
    metric_name = "disk.used.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemActive(BaseVSphereMetricPuller):
    """Amount of memory that is actively used, as estimated by VMkernel based
    on recently touched memory pages
    """
    metric_type = "cumulative"
    metric_name = "mem.active"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemConsumed(BaseVSphereMetricPuller):
    """Amount of host physical memory consumed by a virtual machine, host, or
    cluster
    """
    metric_type = "cumulative"
    metric_name = "mem.consumed"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemGranted(BaseVSphereMetricPuller):
    """Amount of host physical memory or physical memory that is mapped for a
    virtual machine or a host
    """
    metric_type = "cumulative"
    metric_name = "mem.granted"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemHeap(BaseVSphereMetricPuller):
    """VMkernel virtual address space dedicated to VMkernel main heap and
    related data
    """
    metric_type = "cumulative"
    metric_name = "mem.heap"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemHeapfree(BaseVSphereMetricPuller):
    """Free address space in the VMkernel main heap"""
    metric_type = "cumulative"
    metric_name = "mem.heapfree"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemLlSwapIn(BaseVSphereMetricPuller):
    """Amount of memory swapped-in from host cache"""
    metric_type = "cumulative"
    metric_name = "mem.llSwapIn"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemLlSwapOut(BaseVSphereMetricPuller):
    """Amount of memory swapped-out to host cache"""
    metric_type = "cumulative"
    metric_name = "mem.llSwapOut"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemLlSwapUsed(BaseVSphereMetricPuller):
    """Space used for caching swapped pages in the host cache"""
    metric_type = "cumulative"
    metric_name = "mem.llSwapUsed"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemMementitlementLatest(BaseVSphereMetricPuller):
    """Memory allocation as calculated by the VMkernel scheduler based on
    current estimated demand and reservation, limit, and shares policies set
    for all virtual machines and resource pools in the host or cluster
    """
    metric_type = "cumulative"
    metric_name = "mem.mementitlement.latest"
    metric_unit = "MB"
    pulling_interval = 10


class VSphereMemOverhead(BaseVSphereMetricPuller):
    """Host physical memory (KB) consumed by the virtualization infrastructure
    for running the virtual machine
    """
    metric_type = "cumulative"
    metric_name = "mem.overhead"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemShared(BaseVSphereMetricPuller):
    """Amount of guest physical memory that is shared with other virtual
    machines, relative to a single virtual machine or to all powered-on
    virtual machines on a host
    """
    metric_type = "cumulative"
    metric_name = "mem.shared"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSharedcommon(BaseVSphereMetricPuller):
    """Amount of machine memory that is shared by all powered-on virtual
    machines and vSphere services on the host
    """
    metric_type = "cumulative"
    metric_name = "mem.sharedcommon"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemStateLatest(BaseVSphereMetricPuller):
    """One of four threshold levels representing the percentage of free memory
    on the host. The counter value determines swapping and ballooning behavior
    for memory reclamation.
    """
    metric_type = "cumulative"
    metric_name = "mem.state.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereMemSwapIn(BaseVSphereMetricPuller):
    """swapIn"""
    metric_type = "cumulative"
    metric_name = "mem.swapIn"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapin(BaseVSphereMetricPuller):
    """Amount swapped-in to memory from disk"""
    metric_type = "cumulative"
    metric_name = "mem.swapin"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapOut(BaseVSphereMetricPuller):
    """swapOut"""
    metric_type = "cumulative"
    metric_name = "mem.swapOut"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapout(BaseVSphereMetricPuller):
    """Amount of memory swapped-out to disk"""
    metric_type = "cumulative"
    metric_name = "mem.swapout"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapped(BaseVSphereMetricPuller):
    """Current amount of guest physical memory swapped out to the virtual
    machine swap file by the VMkernel
    """
    metric_type = "cumulative"
    metric_name = "mem.swapped"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwaptarget(BaseVSphereMetricPuller):
    """Target size for the virtual machine swap file"""
    metric_type = "cumulative"
    metric_name = "mem.swaptarget"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapunreserved(BaseVSphereMetricPuller):
    """Amount of memory that is unreserved by swap"""
    metric_type = "cumulative"
    metric_name = "mem.swapunreserved"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSwapused(BaseVSphereMetricPuller):
    """Amount of memory that is used by swap"""
    metric_type = "cumulative"
    metric_name = "mem.swapused"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemSysUsage(BaseVSphereMetricPuller):
    """Amount of host physical memory used by VMkernel for core functionality,
    such as device drivers and other internal uses
    """
    metric_type = "cumulative"
    metric_name = "mem.sysUsage"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemUnreserved(BaseVSphereMetricPuller):
    """Amount of memory that is unreserved"""
    metric_type = "cumulative"
    metric_name = "mem.unreserved"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemUsage(BaseVSphereMetricPuller):
    """Memory usage as percentage of total configured or available memory"""
    metric_type = "cumulative"
    metric_name = "mem.usage"
    metric_unit = "%"
    pulling_interval = 10


class VSphereMemVmmemctl(BaseVSphereMetricPuller):
    """Amount of memory allocated by the virtual machine memory control driver
    (vmmemctl), which is installed with VMware Tools
    """
    metric_type = "cumulative"
    metric_name = "mem.vmmemctl"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemVmmemctltarget(BaseVSphereMetricPuller):
    """Target value set by VMkernal for the virtual machine's memory balloon
    size
    """
    metric_type = "cumulative"
    metric_name = "mem.vmmemctltarget"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemZero(BaseVSphereMetricPuller):
    """Memory that contains 0s only"""
    metric_type = "cumulative"
    metric_name = "mem.zero"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemZippedLatest(BaseVSphereMetricPuller):
    """Memory (KB) zipped"""
    metric_type = "cumulative"
    metric_name = "mem.zipped.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereMemZipSavedLatest(BaseVSphereMetricPuller):
    """Memory (KB) saved due to memory zipping"""
    metric_type = "cumulative"
    metric_name = "mem.zipSaved.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereNetBroadcastRxSummation(BaseVSphereMetricPuller):
    """Number of broadcast packets received during the sampling interval"""
    metric_type = "delta"
    metric_name = "net.broadcastRx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetBroadcastTxSummation(BaseVSphereMetricPuller):
    """Number of broadcast packets transmitted during the sampling interval"""
    metric_type = "delta"
    metric_name = "net.broadcastTx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetDroppedRxSummation(BaseVSphereMetricPuller):
    """Number of receives dropped"""
    metric_type = "delta"
    metric_name = "net.droppedRx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetDroppedTxSummation(BaseVSphereMetricPuller):
    """Number of transmits dropped"""
    metric_type = "delta"
    metric_name = "net.droppedTx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetErrorsRxSummation(BaseVSphereMetricPuller):
    """Number of packets with errors received during the sampling interval"""
    metric_type = "delta"
    metric_name = "net.errorsRx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetErrorsTxSummation(BaseVSphereMetricPuller):
    """Number of packets with errors transmitted during the sampling
    interval
    """
    metric_type = "delta"
    metric_name = "net.errorsTx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetMulticastRxSummation(BaseVSphereMetricPuller):
    """Number of multicast packets received during the sampling interval"""
    metric_type = "delta"
    metric_name = "net.multicastRx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetMulticastTxSummation(BaseVSphereMetricPuller):
    """Number of multicast packets transmitted during the sampling interval"""
    metric_type = "delta"
    metric_name = "net.multicastTx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetPacketsRxSummation(BaseVSphereMetricPuller):
    """Number of packets received during the interval"""
    metric_type = "delta"
    metric_name = "net.packetsRx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetPacketsTxSummation(BaseVSphereMetricPuller):
    """Number of packets transmitted during the interval"""
    metric_type = "delta"
    metric_name = "net.packetsTx.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetThroughputContentionSummation(BaseVSphereMetricPuller):
    """The aggregate network droppped packets for the host"""
    metric_type = "delta"
    metric_name = "net.throughput.contention.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetUnknownProtosSummation(BaseVSphereMetricPuller):
    """Number of frames with unknown protocol received during the sampling
    interval
    """
    metric_type = "delta"
    metric_name = "net.unknownProtos.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereNetUsage(BaseVSphereMetricPuller):
    """Network utilization (combined transmit-rates and receive-rates) during
    the interval
    """
    metric_type = "gauge"
    metric_name = "net.usage"
    metric_unit = "KBps"
    pulling_interval = 10


class VSpherePowerEnergySummation(BaseVSphereMetricPuller):
    """Total energy used since last stats reset"""
    metric_type = "delta"
    metric_name = "power.energy.summation"
    metric_unit = "J"
    pulling_interval = 10


class VSphereSysDiskUsageLatest(BaseVSphereMetricPuller):
    """Amount of disk space usage for each mount point"""
    metric_type = "cumulative"
    metric_name = "sys.diskUsage.latest"
    metric_unit = "%"
    pulling_interval = 10


class VSphereSysHeartbeatLatest(BaseVSphereMetricPuller):
    """Number of heartbeats issued per virtual machine during the interval"""
    metric_type = "cumulative"
    metric_name = "sys.heartbeat.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereSysHeartbeatSummation(BaseVSphereMetricPuller):
    """Number of heartbeats issued per virtual machine during the interval"""
    metric_type = "delta"
    metric_name = "sys.heartbeat.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereSysOsUptimeLatest(BaseVSphereMetricPuller):
    """Total time elapsed, in seconds, since last operating system boot-up"""
    metric_type = "cumulative"
    metric_name = "sys.osUptime.latest"
    metric_unit = "s"
    pulling_interval = 10


class VSphereSysResourceCpuAllocMaxLatest(BaseVSphereMetricPuller):
    """CPU allocation limit (in MHz) of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceCpuAllocMax.latest"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereSysResourceCpuAllocMinLatest(BaseVSphereMetricPuller):
    """CPU allocation reservation (in MHz) of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceCpuAllocMin.latest"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereSysResourceCpuAllocSharesLatest(BaseVSphereMetricPuller):
    """CPU allocation shares of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceCpuAllocShares.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereSysResourceCpuUsage(BaseVSphereMetricPuller):
    """Amount of CPU used by the Service Console and other applications during
    the interval
    """
    metric_type = "gauge"
    metric_name = "sys.resourceCpuUsage"
    metric_unit = "MHz"
    pulling_interval = 10


class VSphereSysResourceFdUsageLatest(BaseVSphereMetricPuller):
    """Number of file descriptors used by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceFdUsage.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereSysResourceMemAllocMaxLatest(BaseVSphereMetricPuller):
    """Memory allocation limit (in KB) of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemAllocMax.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemAllocMinLatest(BaseVSphereMetricPuller):
    """Memory allocation reservation (in KB) of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemAllocMin.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemAllocSharesLatest(BaseVSphereMetricPuller):
    """Memory allocation shares of the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemAllocShares.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereSysResourceMemConsumedLatest(BaseVSphereMetricPuller):
    """Memory consumed by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemConsumed.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemCowLatest(BaseVSphereMetricPuller):
    """Memory shared by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemCow.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemMappedLatest(BaseVSphereMetricPuller):
    """Memory mapped by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemMapped.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemOverheadLatest(BaseVSphereMetricPuller):
    """Overhead memory consumed by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemOverhead.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemSharedLatest(BaseVSphereMetricPuller):
    """Memory saved due to sharing by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemShared.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemSwappedLatest(BaseVSphereMetricPuller):
    """Memory swapped out by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemSwapped.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemTouchedLatest(BaseVSphereMetricPuller):
    """Memory touched by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemTouched.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysResourceMemZeroLatest(BaseVSphereMetricPuller):
    """Zero filled memory used by the system resource group"""
    metric_type = "cumulative"
    metric_name = "sys.resourceMemZero.latest"
    metric_unit = "KB"
    pulling_interval = 10


class VSphereSysUptimeLatest(BaseVSphereMetricPuller):
    """Total time elapsed, in seconds, since last system startup"""
    metric_type = "cumulative"
    metric_name = "sys.uptime.latest"
    metric_unit = "s"
    pulling_interval = 10


class VSphereVirtualDiskBusResetsSummation(BaseVSphereMetricPuller):
    """Number of resets to a virtual disk"""
    metric_type = "delta"
    metric_name = "virtualDisk.busResets.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskCommandsAbortedSummation(BaseVSphereMetricPuller):
    """Number of terminations to a virtual disk"""
    metric_type = "delta"
    metric_name = "virtualDisk.commandsAborted.summation"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskLargeSeeksLatest(BaseVSphereMetricPuller):
    """Number of seeks during the interval that were greater than 8192 LBNs
    apart
    """
    metric_type = "cumulative"
    metric_name = "virtualDisk.largeSeeks.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskMediumSeeksLatest(BaseVSphereMetricPuller):
    """Number of seeks during the interval that were between 64 and 8192 LBNs
    apart
    """
    metric_type = "cumulative"
    metric_name = "virtualDisk.mediumSeeks.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskReadIOSizeLatest(BaseVSphereMetricPuller):
    """Average read request size in bytes"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.readIOSize.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskReadLatencyUSLatest(BaseVSphereMetricPuller):
    """Read latency in microseconds"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.readLatencyUS.latest"
    metric_unit = "µs"
    pulling_interval = 10


class VSphereVirtualDiskReadLoadMetricLatest(BaseVSphereMetricPuller):
    """Storage DRS virtual disk metric for the read workload model"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.readLoadMetric.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskReadOIOLatest(BaseVSphereMetricPuller):
    """Average number of outstanding read requests to the virtual disk during
    the collection interval
    """
    metric_type = "cumulative"
    metric_name = "virtualDisk.readOIO.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskSmallSeeksLatest(BaseVSphereMetricPuller):
    """Number of seeks during the interval that were less than 64 LBNs apart"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.smallSeeks.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskWriteIOSizeLatest(BaseVSphereMetricPuller):
    """Average write request size in bytes"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.writeIOSize.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskWriteLatencyUSLatest(BaseVSphereMetricPuller):
    """Write latency in microseconds"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.writeLatencyUS.latest"
    metric_unit = "µs"
    pulling_interval = 10


class VSphereVirtualDiskWriteLoadMetricLatest(BaseVSphereMetricPuller):
    """Storage DRS virtual disk metric for the write workload model"""
    metric_type = "cumulative"
    metric_name = "virtualDisk.writeLoadMetric.latest"
    metric_unit = "num"
    pulling_interval = 10


class VSphereVirtualDiskWriteOIOLatest(BaseVSphereMetricPuller):
    """Average number of outstanding write requests to the virtual disk during
    the collection interval
    """
    metric_type = "cumulative"
    metric_name = "virtualDisk.writeOIO.latest"
    metric_unit = "num"
    pulling_interval = 10
