# -*- encoding: utf-8 -*-
# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from watcher_metering_vsphere import drivers as vsphere


DRIVERS = [
    vsphere.VSphereSysResourceCpuUsage,
    vsphere.VSphereMemStateLatest,
    vsphere.VSphereNetBroadcastRxSummation,
    vsphere.VSphereSysResourceMemMappedLatest,
    vsphere.VSphereCpuEntitlementLatest,
    vsphere.VSphereNetMulticastRxSummation,
    vsphere.VSphereMemLlSwapOut,
    vsphere.VSphereNetDroppedRxSummation,
    vsphere.VSphereVirtualDiskWriteLoadMetricLatest,
    vsphere.VSphereMemZipSavedLatest,
    vsphere.VSpherePowerEnergySummation,
    vsphere.VSphereCpuDemandEntitlementRatioLatest,
    vsphere.VSphereMemShared,
    vsphere.VSphereSysResourceMemAllocMinLatest,
    vsphere.VSphereDiskMaxTotalLatencyLatest,
    vsphere.VSphereMemZero,
    vsphere.VSphereMemGranted,
    vsphere.VSphereNetErrorsRxSummation,
    vsphere.VSphereSysResourceCpuAllocSharesLatest,
    vsphere.VSphereCpuIdleSummation,
    vsphere.VSphereSysResourceMemConsumedLatest,
    vsphere.VSphereVirtualDiskBusResetsSummation,
    vsphere.VSphereSysDiskUsageLatest,
    vsphere.VSphereSysUptimeLatest,
    vsphere.VSphereSysResourceMemZeroLatest,
    vsphere.VSphereMemHeapfree,
    vsphere.VSphereMemSysUsage,
    vsphere.VSphereDiskNumberWriteSummation,
    vsphere.VSphereCpuWaitSummation,
    vsphere.VSphereSysResourceMemSwappedLatest,
    vsphere.VSphereDiskUnsharedLatest,
    vsphere.VSphereNetUnknownProtosSummation,
    vsphere.VSphereDiskScsiReservationConflictsSummation,
    vsphere.VSphereVirtualDiskReadLoadMetricLatest,
    vsphere.VSphereVirtualDiskCommandsAbortedSummation,
    vsphere.VSphereCpuSystemSummation,
    vsphere.VSphereNetPacketsRxSummation,
    vsphere.VSphereMemUsage,
    vsphere.VSphereCpuUsage,
    vsphere.VSphereNetDroppedTxSummation,
    vsphere.VSphereVirtualDiskWriteLatencyUSLatest,
    vsphere.VSphereMemMementitlementLatest,
    vsphere.VSphereVirtualDiskLargeSeeksLatest,
    vsphere.VSphereMemUnreserved,
    vsphere.VSphereMemSwapOut,
    vsphere.VSphereSysResourceMemAllocSharesLatest,
    vsphere.VSphereCpuOverlapSummation,
    vsphere.VSphereNetBroadcastTxSummation,
    vsphere.VSphereSysResourceMemCowLatest,
    vsphere.VSphereCpuCostopSummation,
    vsphere.VSphereVirtualDiskReadIOSizeLatest,
    vsphere.VSphereSysHeartbeatLatest,
    vsphere.VSphereMemVmmemctl,
    vsphere.VSphereMemHeap,
    vsphere.VSphereSysResourceCpuAllocMaxLatest,
    vsphere.VSphereMemSwapped,
    vsphere.VSphereVirtualDiskWriteOIOLatest,
    vsphere.VSphereVirtualDiskReadLatencyUSLatest,
    vsphere.VSphereMemSharedcommon,
    vsphere.VSphereNetErrorsTxSummation,
    vsphere.VSphereVirtualDiskWriteIOSizeLatest,
    vsphere.VSphereVirtualDiskReadOIOLatest,
    vsphere.VSphereCpuSwapwaitSummation,
    vsphere.VSphereDiskUsage,
    vsphere.VSphereSysResourceMemSharedLatest,
    vsphere.VSphereMemSwaptarget,
    vsphere.VSphereCpuRunSummation,
    vsphere.VSphereMemActive,
    vsphere.VSphereNetPacketsTxSummation,
    vsphere.VSphereSysResourceMemAllocMaxLatest,
    vsphere.VSphereDiskBusResetsSummation,
    vsphere.VSphereCpuCoreUtilization,
    vsphere.VSphereCpuReadySummation,
    vsphere.VSphereMemSwapout,
    vsphere.VSphereDiskNumberReadSummation,
    vsphere.VSphereMemSwapused,
    vsphere.VSphereDiskCommandsSummation,
    vsphere.VSphereSysResourceMemTouchedLatest,
    vsphere.VSphereVirtualDiskMediumSeeksLatest,
    vsphere.VSphereMemConsumed,
    vsphere.VSphereMemZippedLatest,
    vsphere.VSphereNetThroughputContentionSummation,
    vsphere.VSphereCpuMaxlimitedSummation,
    vsphere.VSphereMemLlSwapUsed,
    vsphere.VSphereCpuCpuentitlementLatest,
    vsphere.VSphereCpuUsagemhz,
    vsphere.VSphereDiskCommandsAbortedSummation,
    vsphere.VSphereVirtualDiskSmallSeeksLatest,
    vsphere.VSphereMemSwapunreserved,
    vsphere.VSphereMemOverhead,
    vsphere.VSphereNetUsage,
    vsphere.VSphereMemVmmemctltarget,
    vsphere.VSphereNetMulticastTxSummation,
    vsphere.VSphereCpuUtilization,
    vsphere.VSphereDiskDeltausedLatest,
    vsphere.VSphereSysHeartbeatSummation,
    vsphere.VSphereCpuUsedSummation,
    vsphere.VSphereMemSwapin,
    vsphere.VSphereDiskCapacityLatest,
    vsphere.VSphereSysOsUptimeLatest,
    vsphere.VSphereDiskUsedLatest,
    vsphere.VSphereSysResourceCpuAllocMinLatest,
    vsphere.VSphereSysResourceFdUsageLatest,
    vsphere.VSphereMemLlSwapIn,
    vsphere.VSphereMemSwapIn,
    vsphere.VSphereDiskProvisionedLatest,
    vsphere.VSphereSysResourceMemOverheadLatest,
]


def list_opts():
    drivers_opts = [
        (driver.get_entry_name(), driver.get_config_opts())
        for driver in DRIVERS
        ]
    return drivers_opts
