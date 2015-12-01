# Tests convolution using FFT.
# For padding kernels:
# This software contains source code provided by NVIDIA Corporation.
from __future__ import division

import cuda4py as cu
import cuda4py.cufft as cufft
import gc
import logging
import numpy
import os
import scipy.misc
import scipy.signal
import sqlite3
import unittest


def norm_image(x):
    x = x.copy()
    nans = numpy.isnan(x)
    x = numpy.where(nans, 0, x)
    x -= x.min()
    mx = x.max()
    if mx:
        x /= mx
    x *= 255
    x = numpy.round(x).astype(numpy.uint8)
    return numpy.where(nans, 0xFF, x)


def roundup(a, n):
    m = a % n
    if m == 0:
        return a
    return a + (n - m)


class Test(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.old_env = os.environ.get("CUDA_DEVICE")
        if self.old_env is None:
            os.environ["CUDA_DEVICE"] = "0"
        self.ctx = cu.Devices().create_some_context()
        self.thisdir = os.path.dirname(__file__)
        if not len(self.thisdir):
            self.thisdir = "."
        self.db = sqlite3.connect("devices.db")
        self.fft_version = cufft.CUFFT(self.ctx).version
        device = self.ctx.device
        description = "%s (SM %d.%d, PROC %d, L2 %d, MEM %d)" % (
            device.name, device.compute_capability[0],
            device.compute_capability[1], device.multiprocessor_count,
            device.l2_cache_size, device.total_mem)
        self.device_id = 0
        try:
            cur = self.db.execute(
                "select device_id from devices where description = ?",
                (description,))
            for row in cur:
                self.device_id = row[0]
                break
            else:
                logging.warning("Could not get device_id from devices.db "
                                "by description: %s", description)
        except sqlite3.OperationalError as e:
            logging.warning("Could not get device_id from devices.db due: %s",
                            e)

    def tearDown(self):
        if self.old_env is None:
            del os.environ["CUDA_DEVICE"]
        else:
            os.environ["CUDA_DEVICE"] = self.old_env
        del self.old_env
        del self.ctx
        gc.collect()

    def test_roundup(self):
        self.assertEqual(roundup(7, 32), 32)
        self.assertEqual(roundup(57, 57), 57)
        self.assertEqual(roundup(67, 57), 114)

    def conv_roundup(self, width, dtype):
        try:
            cur = self.db.execute(
                "select min(size) from fft2d_sizes where device_id = ? and "
                "dtype = ? and fft_version = ? and size >= ?",
                (self.device_id, {numpy.float32: 1, numpy.float64: 2}[dtype],
                 self.fft_version, width))
        except sqlite3.OperationalError as e:
            logging.warning("Could not find optimal FFT size >= %d due: %s",
                            width, e)
            return width
        for row in cur:
            return int(row[0])
        logging.warning("Could not find optimal FFT size >= %d", width)
        return width

    def _test_conv(self, dtype):
        data = numpy.zeros((227, 127), dtype=dtype)
        kernel = numpy.zeros((8, 15), dtype=dtype)

        numpy.random.seed(1234)
        data[:] = numpy.random.rand(data.size).reshape(data.shape) - 0.5
        kernel[:] = numpy.random.rand(kernel.size).reshape(kernel.shape) - 0.5

        logging.debug("Doing scipy.signal.convolve2d...")
        gold = scipy.signal.convolve2d(data, kernel, mode="valid")
        logging.debug("Done")

        fft_y = self.conv_roundup(data.shape[0] + kernel.shape[0] - 1, dtype)
        fft_x = self.conv_roundup(data.shape[1] + kernel.shape[1] - 1, dtype)
        logging.debug("Frequency domain shape: (%d, %d)", fft_y, fft_x)

        forward = cufft.CUFFT(self.ctx)
        forward.auto_allocation = False
        sz_f = forward.make_plan_many((fft_y, fft_x), 1,
                                      {numpy.float32: cufft.CUFFT_R2C,
                                       numpy.float64: cufft.CUFFT_D2Z}[dtype])
        logging.debug("Forward plan size is %d", sz_f)

        inverse = cufft.CUFFT(self.ctx)
        inverse.auto_allocation = False
        sz_i = inverse.make_plan_many((fft_y, fft_x), 1,
                                      {numpy.float32: cufft.CUFFT_C2R,
                                       numpy.float64: cufft.CUFFT_Z2D}[dtype])
        logging.debug("Inverse plan size is %d", sz_i)

        sz = max(sz_f, sz_i)
        logging.debug("Combined plan size is %d", sz)

        forward.workarea = cu.MemAlloc(self.ctx, sz)
        inverse.workarea = forward.workarea

        logging.debug("Compiling CUDA kernels...")
        prog = cu.Module(
            self.ctx, source="#define dtype %s\r\n"
            "#include <test_conv.cu>\r\n" % {numpy.float32: "float",
                                             numpy.float64: "double"}[dtype],
            include_dirs=(self.thisdir,))
        logging.debug("Done")

        # Initializing padding parameters for kernel
        krn_pad_kernel = prog.create_function("padKernel")

        kernel_buf = cu.MemAlloc(self.ctx, kernel)
        padded_kernel = cu.MemAlloc(self.ctx, fft_y * fft_x * kernel.itemsize)
        pad_kernel_i = numpy.zeros(6, dtype=numpy.int32)

        kernel_y, kernel_x = kernel.shape[0] >> 1, kernel.shape[1] >> 1
        result_y = kernel_y if kernel.shape[0] & 1 else kernel_y - 1
        result_x = kernel_x if kernel.shape[1] & 1 else kernel_x - 1

        pad_kernel_i[0:6] = (fft_y, fft_x, kernel.shape[0], kernel.shape[1],
                             kernel_y, kernel_x)
        krn_pad_kernel.set_args(padded_kernel, kernel_buf, pad_kernel_i[0:1],
                                pad_kernel_i[1:2], pad_kernel_i[2:3],
                                pad_kernel_i[3:4], pad_kernel_i[4:5],
                                pad_kernel_i[5:6])
        local_size_pad_kernel = 32, 8, 1
        global_size_pad_kernel = (
            roundup(kernel.shape[1], local_size_pad_kernel[0]),
            roundup(kernel.shape[0], local_size_pad_kernel[1]), 1)

        # Initializing padding parameters for data
        krn_pad_data = prog.create_function("padData")

        data_buf = cu.MemAlloc(self.ctx, data)
        padded_data = cu.MemAlloc(self.ctx, fft_y * fft_x * data.itemsize)
        pad_data_i = numpy.zeros(8, dtype=numpy.int32)
        pad_data_i[0:8] = (fft_y, fft_x, data.shape[0], data.shape[1],
                           kernel.shape[0], kernel.shape[1],
                           kernel_y, kernel_x)
        krn_pad_data.set_args(padded_data, data_buf, pad_data_i[0:1],
                              pad_data_i[1:2], pad_data_i[2:3],
                              pad_data_i[3:4], pad_data_i[4:5],
                              pad_data_i[5:6], pad_data_i[6:7],
                              pad_data_i[7:8])
        local_size_pad_data = 32, 8, 1
        global_size_pad_data = (roundup(fft_x, local_size_pad_data[0]),
                                roundup(fft_y, local_size_pad_data[1]), 1)

        # Creating spectrum
        data_spectrum = cu.MemAlloc(
            self.ctx, fft_y * (fft_x // 2 + 1) * data.itemsize * 2)
        kernel_spectrum = cu.MemAlloc(
            self.ctx, fft_y * (fft_x // 2 + 1) * kernel.itemsize * 2)

        # Initializing parameters for mul_scale
        krn_mul_scale = prog.create_function("mul_scale")
        mul_scale_i = numpy.zeros(1, dtype=numpy.int32)
        mul_scale_f = numpy.zeros(1, dtype=dtype)
        mul_scale_i[0] = fft_y * (fft_x // 2 + 1)
        mul_scale_f[0] = 1.0 / (fft_x * fft_y)
        krn_mul_scale.set_args(data_spectrum, kernel_spectrum, mul_scale_f,
                               mul_scale_i)
        local_size_mul_scale = 256, 1, 1
        global_size_mul_scale = (
            roundup(fft_y * (fft_x // 2 + 1), local_size_mul_scale[0]), 1, 1)

        # Pad kernel
        padded_kernel.memset32_async(0)
        krn_pad_kernel(global_size_pad_kernel, local_size_pad_kernel)
        self.ctx.synchronize()
        del kernel_buf  # to avoid accidental further use
        result = numpy.zeros((fft_y, fft_x), dtype=dtype)
        padded_kernel.to_host(result)
        scipy.misc.imsave("kernel.png", result)

        # Pad data
        krn_pad_data(global_size_pad_data, local_size_pad_data)
        self.ctx.synchronize()
        del data_buf  # to avoid accidental further use
        padded_data.to_host(result)
        scipy.misc.imsave("data.png", result)

        # Computing spectrum
        {numpy.float32: forward.exec_r2c,
         numpy.float64: forward.exec_d2z}[dtype](padded_kernel, kernel_spectrum)
        spectrum = numpy.zeros((fft_y, fft_x // 2 + 1),
                               dtype={numpy.float32: numpy.complex64,
                                      numpy.float64: numpy.complex128}[dtype])
        kernel_spectrum.to_host(spectrum)
        if numpy.count_nonzero(numpy.isnan(spectrum)):
            logging.error("NaNs encountered in kernel_spectrum")
        {numpy.float32: forward.exec_r2c,
         numpy.float64: forward.exec_d2z}[dtype](padded_data, data_spectrum)
        data_spectrum.to_host(spectrum)
        if numpy.count_nonzero(numpy.isnan(spectrum)):
            logging.error("NaNs encountered in data_spectrum")

        # Multiply spectrum and scale for inverse transform
        krn_mul_scale(global_size_mul_scale, local_size_mul_scale)

        # Do inverse transform
        {numpy.float32: inverse.exec_c2r,
         numpy.float64: inverse.exec_z2d}[dtype](data_spectrum, padded_data)

        # Get the result back
        padded_data.to_host(result)

        valid = result[result_y:result_y + gold.shape[0],
                       result_x:result_x + gold.shape[1]]
        maxdiff = numpy.fabs(gold - valid).max()
        logging.debug("Maximum difference is %.6e", maxdiff)

        scipy.misc.imsave("gold.png", norm_image(gold))
        scipy.misc.imsave("result.png", norm_image(result))
        scipy.misc.imsave("valid.png", norm_image(valid))
        scipy.misc.imsave("sub.png", norm_image(numpy.fabs(gold - valid)))

    def test_conv_float32(self):
        logging.debug("ENTER: test_conv_float32")
        self._test_conv(numpy.float32)
        logging.debug("EXIT: test_conv_float32")

    def test_conv_float64(self):
        logging.debug("ENTER: test_conv_float64")
        self._test_conv(numpy.float64)
        logging.debug("EXIT: test_conv_float64")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
