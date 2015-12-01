"""
Copyright (c) 2014, Samsung Electronics Co.,Ltd.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of Samsung Electronics Co.,Ltd..
"""

"""
cuda4py - CUDA cffi bindings and helper classes.
URL: https://github.com/ajkxyz/cuda4py
Original author: Alexey Kazantsev <a.kazantsev@samsung.com>
"""

"""
Tests performance of cuFFT for various 2^a * 3^b * 5^c * 7^d.
"""
import cuda4py as cu
import cuda4py.cufft as cufft
import gc
import logging
import numpy
import os
import sqlite3
import time
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.old_env = os.environ.get("CUDA_DEVICE")
        if self.old_env is None:
            os.environ["CUDA_DEVICE"] = "0"
        self.ctx = cu.Devices().create_some_context()
        self.path = os.path.dirname(__file__)
        if not len(self.path):
            self.path = "."

    def tearDown(self):
        if self.old_env is None:
            del os.environ["CUDA_DEVICE"]
        else:
            os.environ["CUDA_DEVICE"] = self.old_env
        del self.old_env
        del self.ctx
        gc.collect()

    def _test_perf(self, dtype):
        db = sqlite3.connect("devices.db")
        db.execute("create table if not exists devices ("
                   "device_id integer not null primary key autoincrement, "
                   "description text not null unique)")
        device = self.ctx.device
        description = "%s (SM %d.%d, PROC %d, L2 %d, MEM %d)" % (
            device.name, device.compute_capability[0],
            device.compute_capability[1], device.multiprocessor_count,
            device.l2_cache_size, device.total_mem)
        try:
            db.execute("insert into devices (description) values (?)",
                       (description,))
            db.commit()
        except sqlite3.IntegrityError:
            pass
        cur = db.execute("select device_id from devices where description = ?",
                         (description,))
        for row in cur:
            device_id = row[0]
            break
        db.execute("create table if not exists dtypes ("
                   "dtype integer not null primary key, "
                   "description text not null unique)")
        try:
            db.execute("insert into dtypes (dtype, description) values (?, ?)",
                       (1, "float"))
            db.execute("insert into dtypes (dtype, description) values (?, ?)",
                       (2, "double"))
        except sqlite3.IntegrityError:
            pass
        db.execute("create table if not exists fft2d_sizes ("
                   "device_id integer not null, "
                   "dtype integer not null, "
                   "fft_version integer not null, "
                   "size integer not null, "
                   "dt double not null, "
                   "constraint pk_fft2d_size "
                   "primary key (device_id, dtype, fft_version, size), "
                   "constraint fk_fft2d_sizes_device "
                   "foreign key (device_id) references devices (device_id) "
                   "on delete cascade on update cascade, "
                   "constraint fk_fft2d_sizes_dtype "
                   "foreign key (dtype) references dtypes (dtype))")

        _dtype = {numpy.float32: 1,
                  numpy.float64: 2}[dtype]
        fft_version = cufft.CUFFT(self.ctx).version
        cur = db.execute("select size, dt from fft2d_sizes where "
                         "device_id = ? and dtype = ? and fft_version = ? "
                         "order by size", (device_id, _dtype, fft_version))
        times = []
        for row in cur:
            times.append((row[0], row[1]))

        if len(times):
            logging.debug("Found times in devices.db: %s", times)
            return

        gc.collect()

        factors = (2, 3, 5, 7)
        nums = list(factors)
        i = 0
        sz = numpy.zeros(1, dtype=dtype).itemsize
        max_mem = self.ctx.device.total_mem - 256 * 1024 * 1024

        def num_fits(x):
            return x * x * sz * 2 < max_mem

        valid = set()
        while i < len(nums) and num_fits(nums[i]):
            for factor in factors:
                x = nums[i] * factor
                if num_fits(x):
                    if x in valid:
                        continue
                    nums.append(x)
                    valid.add(x)
            i += 1
        del valid
        gc.collect()

        nums.sort()
        logging.debug("Will test %d sizes", len(nums))

        logging.debug("Allocating random array...")
        random = numpy.random.rand(nums[-1] * nums[-1]).astype(dtype)
        logging.debug("Done")
        times = []
        for num in nums:
            gc.collect()
            try:
                dt = self._check(dtype, num, random)
            except cu.CUDARuntimeError as e:
                logging.warning("%d x %d failed due: %s", num, num, e)
                continue
            while len(times) and times[-1][1] > dt:
                logging.debug("POP %d x %d", times[-1][0], times[-1][0])
                times.pop()
            times.append((num, dt))
            logging.debug("%d x %d completed in %.6f sec", num, num, dt)
        gc.collect()

        logging.debug("Times are: %s", times)

        for num, dt in times:
            db.execute("insert into fft2d_sizes "
                       "(device_id, dtype, fft_version, size, dt) "
                       "values (?, ?, ?, ?, ?)",
                       (device_id, _dtype, fft_version, num, dt))
        db.commit()

    def _check(self, dtype, num, random):
        x = random[:num * num]
        xbuf = cu.MemAlloc(self.ctx, x)
        ybuf = cu.MemAlloc(self.ctx, (num * num // 2 + 1) * x.itemsize * 2)

        # Forward transform
        fft = cufft.CUFFT(self.ctx)
        fft.auto_allocation = False

        sz = fft.make_plan_many(x.shape, 1,
                                {numpy.float32: cufft.CUFFT_R2C,
                                 numpy.float64: cufft.CUFFT_D2Z}[dtype])
        fft.workarea = cu.MemAlloc(self.ctx, sz)

        gc.collect()
        gc.disable()
        N = 12
        dry_run = 3
        for i in range(N + dry_run):
            {numpy.float32: fft.exec_r2c,
             numpy.float64: fft.exec_d2z}[dtype](xbuf, ybuf)
            if i == dry_run - 1:
                self.ctx.synchronize()
                t0 = time.time()
        self.ctx.synchronize()
        dt = (time.time() - t0) / N
        gc.enable()

        del fft
        del ybuf
        del xbuf
        gc.collect()

        return dt

    def test_perf_float(self):
        logging.debug("ENTER: test_perf_float")
        self._test_perf(numpy.float32)
        logging.debug("EXIT: test_perf_float")

    def test_perf_double(self):
        logging.debug("ENTER: test_perf_double")
        self._test_perf(numpy.float64)
        logging.debug("EXIT: test_perf_double")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
