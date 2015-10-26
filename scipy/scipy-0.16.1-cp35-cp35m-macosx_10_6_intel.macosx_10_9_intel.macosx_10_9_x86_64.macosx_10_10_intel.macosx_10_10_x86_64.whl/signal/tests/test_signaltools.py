from __future__ import division, print_function, absolute_import

from decimal import Decimal
from itertools import product

from numpy.testing import (
    TestCase, run_module_suite, assert_equal,
    assert_almost_equal, assert_array_equal, assert_array_almost_equal,
    assert_raises, assert_allclose, assert_, dec)
from numpy import array, arange
import numpy as np

from scipy.optimize import fmin
from scipy import signal
from scipy.signal import (
    correlate, convolve, convolve2d, fftconvolve,
    hilbert, hilbert2, lfilter, lfilter_zi, filtfilt, butter, tf2zpk,
    invres, invresz, vectorstrength, signaltools, lfiltic, tf2sos, sosfilt,
    sosfilt_zi)
from scipy.signal.signaltools import _filtfilt_gust


class _TestConvolve(TestCase):

    def test_basic(self):
        a = [3, 4, 5, 6, 5, 4]
        b = [1, 2, 3]
        c = convolve(a, b)
        assert_array_equal(c, array([3, 10, 22, 28, 32, 32, 23, 12]))

    def test_complex(self):
        x = array([1 + 1j, 2 + 1j, 3 + 1j])
        y = array([1 + 1j, 2 + 1j])
        z = convolve(x, y)
        assert_array_equal(z, array([2j, 2 + 6j, 5 + 8j, 5 + 5j]))

    def test_zero_rank(self):
        a = 1289
        b = 4567
        c = convolve(a, b)
        assert_equal(c, a * b)

    def test_single_element(self):
        a = array([4967])
        b = array([3920])
        c = convolve(a, b)
        assert_equal(c, a * b)

    def test_2d_arrays(self):
        a = [[1, 2, 3], [3, 4, 5]]
        b = [[2, 3, 4], [4, 5, 6]]
        c = convolve(a, b)
        d = array([[2, 7, 16, 17, 12],
                   [10, 30, 62, 58, 38],
                   [12, 31, 58, 49, 30]])
        assert_array_equal(c, d)

    def test_valid_mode(self):
        a = [1, 2, 3, 6, 5, 3]
        b = [2, 3, 4, 5, 3, 4, 2, 2, 1]
        c = convolve(a, b, 'valid')
        assert_array_equal(c, array([70, 78, 73, 65]))

    def test_input_swapping(self):
        small = arange(8).reshape(2, 2, 2)
        big = 1j * arange(27).reshape(3, 3, 3)
        big += arange(27)[::-1].reshape(3, 3, 3)

        out_array = array(
            [[[0 + 0j, 26 + 0j, 25 + 1j, 24 + 2j],
              [52 + 0j, 151 + 5j, 145 + 11j, 93 + 11j],
              [46 + 6j, 133 + 23j, 127 + 29j, 81 + 23j],
              [40 + 12j, 98 + 32j, 93 + 37j, 54 + 24j]],

             [[104 + 0j, 247 + 13j, 237 + 23j, 135 + 21j],
              [282 + 30j, 632 + 96j, 604 + 124j, 330 + 86j],
              [246 + 66j, 548 + 180j, 520 + 208j, 282 + 134j],
              [142 + 66j, 307 + 161j, 289 + 179j, 153 + 107j]],

             [[68 + 36j, 157 + 103j, 147 + 113j, 81 + 75j],
              [174 + 138j, 380 + 348j, 352 + 376j, 186 + 230j],
              [138 + 174j, 296 + 432j, 268 + 460j, 138 + 278j],
              [70 + 138j, 145 + 323j, 127 + 341j, 63 + 197j]],

             [[32 + 72j, 68 + 166j, 59 + 175j, 30 + 100j],
              [68 + 192j, 139 + 433j, 117 + 455j, 57 + 255j],
              [38 + 222j, 73 + 499j, 51 + 521j, 21 + 291j],
              [12 + 144j, 20 + 318j, 7 + 331j, 0 + 182j]]])

        assert_array_equal(convolve(small, big, 'full'), out_array)
        assert_array_equal(convolve(big, small, 'full'), out_array)
        assert_array_equal(convolve(small, big, 'same'),
                           out_array[1:3, 1:3, 1:3])
        assert_array_equal(convolve(big, small, 'same'),
                           out_array[0:3, 0:3, 0:3])
        assert_raises(ValueError, convolve, small, big, 'valid')
        assert_array_equal(convolve(big, small, 'valid'),
                           out_array[1:3, 1:3, 1:3])


class TestConvolve(_TestConvolve):

    def test_valid_mode(self):
        # 'valid' mode if b.size > a.size does not make sense with the new
        # behavior
        a = [1, 2, 3, 6, 5, 3]
        b = [2, 3, 4, 5, 3, 4, 2, 2, 1]

        def _test():
            convolve(a, b, 'valid')
        self.assertRaises(ValueError, _test)

    def test_same_mode(self):
        a = [1, 2, 3, 3, 1, 2]
        b = [1, 4, 3, 4, 5, 6, 7, 4, 3, 2, 1, 1, 3]
        c = convolve(a, b, 'same')
        d = array([57, 61, 63, 57, 45, 36])
        assert_array_equal(c, d)


class _TestConvolve2d(TestCase):

    def test_2d_arrays(self):
        a = [[1, 2, 3], [3, 4, 5]]
        b = [[2, 3, 4], [4, 5, 6]]
        d = array([[2, 7, 16, 17, 12],
                   [10, 30, 62, 58, 38],
                   [12, 31, 58, 49, 30]])
        e = convolve2d(a, b)
        assert_array_equal(e, d)

    def test_valid_mode(self):
        e = [[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]]
        f = [[1, 2, 3], [3, 4, 5]]
        g = convolve2d(e, f, 'valid')
        h = array([[62, 80, 98, 116, 134]])
        assert_array_equal(g, h)

    def test_valid_mode_complx(self):
        e = [[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]]
        f = np.array([[1, 2, 3], [3, 4, 5]], dtype=np.complex) + 1j
        g = convolve2d(e, f, 'valid')
        h = array([[62.+24.j, 80.+30.j, 98.+36.j, 116.+42.j, 134.+48.j]])
        assert_array_almost_equal(g, h)

    def test_fillvalue(self):
        a = [[1, 2, 3], [3, 4, 5]]
        b = [[2, 3, 4], [4, 5, 6]]
        fillval = 1
        c = convolve2d(a, b, 'full', 'fill', fillval)
        d = array([[24, 26, 31, 34, 32],
                   [28, 40, 62, 64, 52],
                   [32, 46, 67, 62, 48]])
        assert_array_equal(c, d)

    def test_wrap_boundary(self):
        a = [[1, 2, 3], [3, 4, 5]]
        b = [[2, 3, 4], [4, 5, 6]]
        c = convolve2d(a, b, 'full', 'wrap')
        d = array([[80, 80, 74, 80, 80],
                   [68, 68, 62, 68, 68],
                   [80, 80, 74, 80, 80]])
        assert_array_equal(c, d)

    def test_sym_boundary(self):
        a = [[1, 2, 3], [3, 4, 5]]
        b = [[2, 3, 4], [4, 5, 6]]
        c = convolve2d(a, b, 'full', 'symm')
        d = array([[34, 30, 44, 62, 66],
                   [52, 48, 62, 80, 84],
                   [82, 78, 92, 110, 114]])
        assert_array_equal(c, d)


class TestConvolve2d(_TestConvolve2d):

    def test_same_mode(self):
        e = [[1, 2, 3], [3, 4, 5]]
        f = [[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]]
        g = convolve2d(e, f, 'same')
        h = array([[22, 28, 34],
                   [80, 98, 116]])
        assert_array_equal(g, h)

    def test_valid_mode2(self):
        # Test when in2.size > in1.size
        e = [[1, 2, 3], [3, 4, 5]]
        f = [[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]]

        def _test():
            convolve2d(e, f, 'valid')
        self.assertRaises(ValueError, _test)

    def test_consistency_convolve_funcs(self):
        # Compare np.convolve, signal.convolve, signal.convolve2d
        a = np.arange(5)
        b = np.array([3.2, 1.4, 3])
        for mode in ['full', 'valid', 'same']:
            assert_almost_equal(np.convolve(a, b, mode=mode),
                                signal.convolve(a, b, mode=mode))
            assert_almost_equal(np.squeeze(
                signal.convolve2d([a], [b], mode=mode)),
                signal.convolve(a, b, mode=mode))


class TestFFTConvolve(TestCase):

    def test_real(self):
        x = array([1, 2, 3])
        assert_array_almost_equal(signal.fftconvolve(x, x), [1, 4, 10, 12, 9.])

    def test_complex(self):
        x = array([1 + 1j, 2 + 2j, 3 + 3j])
        assert_array_almost_equal(signal.fftconvolve(x, x),
                                  [0 + 2j, 0 + 8j, 0 + 20j, 0 + 24j, 0 + 18j])

    def test_2d_real_same(self):
        a = array([[1, 2, 3], [4, 5, 6]])
        assert_array_almost_equal(signal.fftconvolve(a, a),
                                  array([[1, 4, 10, 12, 9],
                                         [8, 26, 56, 54, 36],
                                         [16, 40, 73, 60, 36]]))

    def test_2d_complex_same(self):
        a = array([[1 + 2j, 3 + 4j, 5 + 6j], [2 + 1j, 4 + 3j, 6 + 5j]])
        c = fftconvolve(a, a)
        d = array([[-3 + 4j, -10 + 20j, -21 + 56j, -18 + 76j, -11 + 60j],
                   [10j, 44j, 118j, 156j, 122j],
                   [3 + 4j, 10 + 20j, 21 + 56j, 18 + 76j, 11 + 60j]])
        assert_array_almost_equal(c, d)

    def test_real_same_mode(self):
        a = array([1, 2, 3])
        b = array([3, 3, 5, 6, 8, 7, 9, 0, 1])
        c = fftconvolve(a, b, 'same')
        d = array([35., 41., 47.])
        assert_array_almost_equal(c, d)

    def test_real_same_mode2(self):
        a = array([3, 3, 5, 6, 8, 7, 9, 0, 1])
        b = array([1, 2, 3])
        c = fftconvolve(a, b, 'same')
        d = array([9., 20., 25., 35., 41., 47., 39., 28., 2.])
        assert_array_almost_equal(c, d)

    def test_real_valid_mode(self):
        a = array([3, 2, 1])
        b = array([3, 3, 5, 6, 8, 7, 9, 0, 1])

        def _test():
            fftconvolve(a, b, 'valid')
        self.assertRaises(ValueError, _test)

    def test_real_valid_mode2(self):
        a = array([3, 3, 5, 6, 8, 7, 9, 0, 1])
        b = array([3, 2, 1])
        c = fftconvolve(a, b, 'valid')
        d = array([24., 31., 41., 43., 49., 25., 12.])
        assert_array_almost_equal(c, d)

    def test_empty(self):
        # Regression test for #1745: crashes with 0-length input.
        assert_(fftconvolve([], []).size == 0)
        assert_(fftconvolve([5, 6], []).size == 0)
        assert_(fftconvolve([], [7]).size == 0)

    def test_zero_rank(self):
        a = array(4967)
        b = array(3920)
        c = fftconvolve(a, b)
        assert_equal(c, a * b)

    def test_single_element(self):
        a = array([4967])
        b = array([3920])
        c = fftconvolve(a, b)
        assert_equal(c, a * b)

    def test_random_data(self):
        np.random.seed(1234)
        a = np.random.rand(1233) + 1j * np.random.rand(1233)
        b = np.random.rand(1321) + 1j * np.random.rand(1321)
        c = fftconvolve(a, b, 'full')
        d = np.convolve(a, b, 'full')
        assert_(np.allclose(c, d, rtol=1e-10))

    @dec.slow
    def test_many_sizes(self):
        np.random.seed(1234)

        def ns():
            for j in range(1, 100):
                yield j
            for j in range(1000, 1500):
                yield j
            for k in range(50):
                yield np.random.randint(1001, 10000)

        for n in ns():
            msg = 'n=%d' % (n,)
            a = np.random.rand(n) + 1j * np.random.rand(n)
            b = np.random.rand(n) + 1j * np.random.rand(n)
            c = fftconvolve(a, b, 'full')
            d = np.convolve(a, b, 'full')
            assert_allclose(c, d, atol=1e-10, err_msg=msg)

    def test_next_regular(self):
        np.random.seed(1234)

        def ns():
            for j in range(1, 1000):
                yield j
            yield 2**5 * 3**5 * 4**5 + 1

        for n in ns():
            m = signaltools._next_regular(n)
            msg = "n=%d, m=%d" % (n, m)

            assert_(m >= n, msg)

            # check regularity
            k = m
            for d in [2, 3, 5]:
                while True:
                    a, b = divmod(k, d)
                    if b == 0:
                        k = a
                    else:
                        break
            assert_equal(k, 1, err_msg=msg)

    def test_next_regular_strict(self):
        hams = {
            1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 8, 8: 8, 14: 15, 15: 15,
            16: 16, 17: 18, 1021: 1024, 1536: 1536, 51200000: 51200000,
            510183360: 510183360, 510183360 + 1: 512000000,
            511000000: 512000000,
            854296875: 854296875, 854296875 + 1: 859963392,
            196608000000: 196608000000, 196608000000 + 1: 196830000000,
            8789062500000: 8789062500000, 8789062500000 + 1: 8796093022208,
            206391214080000: 206391214080000,
            206391214080000 + 1: 206624260800000,
            470184984576000: 470184984576000,
            470184984576000 + 1: 470715894135000,
            7222041363087360: 7222041363087360,
            7222041363087360 + 1: 7230196133913600,
            # power of 5    5**23
            11920928955078125: 11920928955078125,
            11920928955078125 - 1: 11920928955078125,
            # power of 3    3**34
            16677181699666569: 16677181699666569,
            16677181699666569 - 1: 16677181699666569,
            # power of 2   2**54
            18014398509481984: 18014398509481984,
            18014398509481984 - 1: 18014398509481984,
            # above this, int(ceil(n)) == int(ceil(n+1))
            19200000000000000: 19200000000000000,
            19200000000000000 + 1: 19221679687500000,
            288230376151711744: 288230376151711744,
            288230376151711744 + 1: 288325195312500000,
            288325195312500000 - 1: 288325195312500000,
            288325195312500000: 288325195312500000,
            288325195312500000 + 1: 288555831593533440,
            # power of 3    3**83
            3990838394187339929534246675572349035227 - 1:
                3990838394187339929534246675572349035227,
            3990838394187339929534246675572349035227:
                3990838394187339929534246675572349035227,
            # power of 2     2**135
            43556142965880123323311949751266331066368 - 1:
                43556142965880123323311949751266331066368,
            43556142965880123323311949751266331066368:
                43556142965880123323311949751266331066368,
            # power of 5      5**57
            6938893903907228377647697925567626953125 - 1:
                6938893903907228377647697925567626953125,
            6938893903907228377647697925567626953125:
                6938893903907228377647697925567626953125,
            # http://www.drdobbs.com/228700538
            # 2**96 * 3**1 * 5**13
            290142196707511001929482240000000000000 - 1:
                290142196707511001929482240000000000000,
            290142196707511001929482240000000000000:
                290142196707511001929482240000000000000,
            290142196707511001929482240000000000000 + 1:
                290237644800000000000000000000000000000,
            # 2**36 * 3**69 * 5**7
            4479571262811807241115438439905203543080960000000 - 1:
                4479571262811807241115438439905203543080960000000,
            4479571262811807241115438439905203543080960000000:
                4479571262811807241115438439905203543080960000000,
            4479571262811807241115438439905203543080960000000 + 1:
                4480327901140333639941336854183943340032000000000,
            # 2**37 * 3**44 * 5**42
            30774090693237851027531250000000000000000000000000000000000000 - 1:
                30774090693237851027531250000000000000000000000000000000000000,
            30774090693237851027531250000000000000000000000000000000000000:
                30774090693237851027531250000000000000000000000000000000000000,
            30774090693237851027531250000000000000000000000000000000000000 + 1:
                30778180617309082445871527002041377406962596539492679680000000,
        }
        for x, y in hams.items():
            assert_equal(signaltools._next_regular(x), y)


class TestMedFilt(TestCase):

    def test_basic(self):
        f = [[50, 50, 50, 50, 50, 92, 18, 27, 65, 46],
             [50, 50, 50, 50, 50, 0, 72, 77, 68, 66],
             [50, 50, 50, 50, 50, 46, 47, 19, 64, 77],
             [50, 50, 50, 50, 50, 42, 15, 29, 95, 35],
             [50, 50, 50, 50, 50, 46, 34, 9, 21, 66],
             [70, 97, 28, 68, 78, 77, 61, 58, 71, 42],
             [64, 53, 44, 29, 68, 32, 19, 68, 24, 84],
             [3, 33, 53, 67, 1, 78, 74, 55, 12, 83],
             [7, 11, 46, 70, 60, 47, 24, 43, 61, 26],
             [32, 61, 88, 7, 39, 4, 92, 64, 45, 61]]

        d = signal.medfilt(f, [7, 3])
        e = signal.medfilt2d(np.array(f, np.float), [7, 3])
        assert_array_equal(d, [[0, 50, 50, 50, 42, 15, 15, 18, 27, 0],
                               [0, 50, 50, 50, 50, 42, 19, 21, 29, 0],
                               [50, 50, 50, 50, 50, 47, 34, 34, 46, 35],
                               [50, 50, 50, 50, 50, 50, 42, 47, 64, 42],
                               [50, 50, 50, 50, 50, 50, 46, 55, 64, 35],
                               [33, 50, 50, 50, 50, 47, 46, 43, 55, 26],
                               [32, 50, 50, 50, 50, 47, 46, 45, 55, 26],
                               [7, 46, 50, 50, 47, 46, 46, 43, 45, 21],
                               [0, 32, 33, 39, 32, 32, 43, 43, 43, 0],
                               [0, 7, 11, 7, 4, 4, 19, 19, 24, 0]])
        assert_array_equal(d, e)

    def test_none(self):
        # Ticket #1124. Ensure this does not segfault.
        try:
            signal.medfilt(None)
        except:
            pass
        # Expand on this test to avoid a regression with possible contiguous
        # numpy arrays that have odd strides. The stride value below gets
        # us into wrong memory if used (but it does not need to be used)
        dummy = np.arange(10, dtype=np.float64)
        a = dummy[5:6]
        a.strides = 16
        assert_(signal.medfilt(a, 1) == 5.)


class TestWiener(TestCase):

    def test_basic(self):
        g = array([[5, 6, 4, 3],
                   [3, 5, 6, 2],
                   [2, 3, 5, 6],
                   [1, 6, 9, 7]], 'd')
        h = array([[2.16374269, 3.2222222222, 2.8888888889, 1.6666666667],
                   [2.666666667, 4.33333333333, 4.44444444444, 2.8888888888],
                   [2.222222222, 4.4444444444, 5.4444444444, 4.801066874837],
                   [1.33333333333, 3.92735042735, 6.0712560386, 5.0404040404]])
        assert_array_almost_equal(signal.wiener(g), h, decimal=6)
        assert_array_almost_equal(signal.wiener(g, mysize=3), h, decimal=6)


class TestResample(TestCase):

    def test_basic(self):
        # Regression test for issue #3603.
        # window.shape must equal to sig.shape[0]
        sig = np.arange(128)
        num = 256
        win = signal.get_window(('kaiser', 8.0), 160)
        assert_raises(ValueError, signal.resample, sig, num, window=win)


class TestCSpline1DEval(TestCase):

    def test_basic(self):
        y = array([1, 2, 3, 4, 3, 2, 1, 2, 3.0])
        x = arange(len(y))
        dx = x[1] - x[0]
        cj = signal.cspline1d(y)

        x2 = arange(len(y) * 10.0) / 10.0
        y2 = signal.cspline1d_eval(cj, x2, dx=dx, x0=x[0])

        # make sure interpolated values are on knot points
        assert_array_almost_equal(y2[::10], y, decimal=5)


class TestOrderFilt(TestCase):

    def test_basic(self):
        assert_array_equal(signal.order_filter([1, 2, 3], [1, 0, 1], 1),
                           [2, 3, 2])


class _TestLinearFilter(TestCase):
    def generate(self, shape):
        x = np.linspace(0, np.prod(shape) - 1, np.prod(shape)).reshape(shape)
        return self.convert_dtype(x)

    def convert_dtype(self, arr):
        if self.dtype == np.dtype('O'):
            arr = np.asarray(arr)
            out = np.empty(arr.shape, self.dtype)
            iter = np.nditer([arr, out], ['refs_ok','zerosize_ok'],
                        [['readonly'],['writeonly']])
            for x, y in iter:
                y[...] = self.type(x[()])
            return out
        else:
            return np.array(arr, self.dtype, copy=False)

    def test_rank_1_IIR(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, -0.5])
        y_r = self.convert_dtype([0, 2, 4, 6, 8, 10.])
        assert_array_almost_equal(lfilter(b, a, x), y_r)

    def test_rank_1_FIR(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, 1])
        a = self.convert_dtype([1])
        y_r = self.convert_dtype([0, 1, 3, 5, 7, 9.])
        assert_array_almost_equal(lfilter(b, a, x), y_r)

    def test_rank_1_IIR_init_cond(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, 0, -1])
        a = self.convert_dtype([0.5, -0.5])
        zi = self.convert_dtype([1, 2])
        y_r = self.convert_dtype([1, 5, 9, 13, 17, 21])
        zf_r = self.convert_dtype([13, -10])
        y, zf = lfilter(b, a, x, zi=zi)
        assert_array_almost_equal(y, y_r)
        assert_array_almost_equal(zf, zf_r)

    def test_rank_1_FIR_init_cond(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, 1, 1])
        a = self.convert_dtype([1])
        zi = self.convert_dtype([1, 1])
        y_r = self.convert_dtype([1, 2, 3, 6, 9, 12.])
        zf_r = self.convert_dtype([9, 5])
        y, zf = lfilter(b, a, x, zi=zi)
        assert_array_almost_equal(y, y_r)
        assert_array_almost_equal(zf, zf_r)

    def test_rank_2_IIR_axis_0(self):
        x = self.generate((4, 3))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])
        y_r2_a0 = self.convert_dtype([[0, 2, 4], [6, 4, 2], [0, 2, 4],
                                      [6, 4, 2]])
        y = lfilter(b, a, x, axis=0)
        assert_array_almost_equal(y_r2_a0, y)

    def test_rank_2_IIR_axis_1(self):
        x = self.generate((4, 3))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])
        y_r2_a1 = self.convert_dtype([[0, 2, 0], [6, -4, 6], [12, -10, 12],
                            [18, -16, 18]])
        y = lfilter(b, a, x, axis=1)
        assert_array_almost_equal(y_r2_a1, y)

    def test_rank_2_IIR_axis_0_init_cond(self):
        x = self.generate((4, 3))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])
        zi = self.convert_dtype(np.ones((4,1)))

        y_r2_a0_1 = self.convert_dtype([[1, 1, 1], [7, -5, 7], [13, -11, 13],
                              [19, -17, 19]])
        zf_r = self.convert_dtype([-5, -17, -29, -41])[:, np.newaxis]
        y, zf = lfilter(b, a, x, axis=1, zi=zi)
        assert_array_almost_equal(y_r2_a0_1, y)
        assert_array_almost_equal(zf, zf_r)

    def test_rank_2_IIR_axis_1_init_cond(self):
        x = self.generate((4,3))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])
        zi = self.convert_dtype(np.ones((1,3)))

        y_r2_a0_0 = self.convert_dtype([[1, 3, 5], [5, 3, 1],
                                        [1, 3, 5], [5, 3, 1]])
        zf_r = self.convert_dtype([[-23, -23, -23]])
        y, zf = lfilter(b, a, x, axis=0, zi=zi)
        assert_array_almost_equal(y_r2_a0_0, y)
        assert_array_almost_equal(zf, zf_r)

    def test_rank_3_IIR(self):
        x = self.generate((4, 3, 2))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])

        for axis in range(x.ndim):
            y = lfilter(b, a, x, axis)
            y_r = np.apply_along_axis(lambda w: lfilter(b, a, w), axis, x)
            assert_array_almost_equal(y, y_r)

    def test_rank_3_IIR_init_cond(self):
        x = self.generate((4, 3, 2))
        b = self.convert_dtype([1, -1])
        a = self.convert_dtype([0.5, 0.5])

        for axis in range(x.ndim):
            zi_shape = list(x.shape)
            zi_shape[axis] = 1
            zi = self.convert_dtype(np.ones(zi_shape))
            zi1 = self.convert_dtype([1])
            y, zf = lfilter(b, a, x, axis, zi)
            lf0 = lambda w: lfilter(b, a, w, zi=zi1)[0]
            lf1 = lambda w: lfilter(b, a, w, zi=zi1)[1]
            y_r = np.apply_along_axis(lf0, axis, x)
            zf_r = np.apply_along_axis(lf1, axis, x)
            assert_array_almost_equal(y, y_r)
            assert_array_almost_equal(zf, zf_r)

    def test_rank_3_FIR(self):
        x = self.generate((4, 3, 2))
        b = self.convert_dtype([1, 0, -1])
        a = self.convert_dtype([1])

        for axis in range(x.ndim):
            y = lfilter(b, a, x, axis)
            y_r = np.apply_along_axis(lambda w: lfilter(b, a, w), axis, x)
            assert_array_almost_equal(y, y_r)

    def test_rank_3_FIR_init_cond(self):
        x = self.generate((4, 3, 2))
        b = self.convert_dtype([1, 0, -1])
        a = self.convert_dtype([1])

        for axis in range(x.ndim):
            zi_shape = list(x.shape)
            zi_shape[axis] = 2
            zi = self.convert_dtype(np.ones(zi_shape))
            zi1 = self.convert_dtype([1, 1])
            y, zf = lfilter(b, a, x, axis, zi)
            lf0 = lambda w: lfilter(b, a, w, zi=zi1)[0]
            lf1 = lambda w: lfilter(b, a, w, zi=zi1)[1]
            y_r = np.apply_along_axis(lf0, axis, x)
            zf_r = np.apply_along_axis(lf1, axis, x)
            assert_array_almost_equal(y, y_r)
            assert_array_almost_equal(zf, zf_r)

    def test_zi_pseudobroadcast(self):
        x = self.generate((4, 5, 20))
        b,a = signal.butter(8, 0.2, output='ba')
        b = self.convert_dtype(b)
        a = self.convert_dtype(a)
        zi_size = b.shape[0] - 1

        # lfilter requires x.ndim == zi.ndim exactly.  However, zi can have
        # length 1 dimensions.
        zi_full = self.convert_dtype(np.ones((4, 5, zi_size)))
        zi_sing = self.convert_dtype(np.ones((1, 1, zi_size)))

        y_full, zf_full = lfilter(b, a, x, zi=zi_full)
        y_sing, zf_sing = lfilter(b, a, x, zi=zi_sing)

        assert_array_almost_equal(y_sing, y_full)
        assert_array_almost_equal(zf_full, zf_sing)

        # lfilter does not prepend ones
        assert_raises(ValueError, lfilter, b, a, x, -1, np.ones(zi_size))

    def test_scalar_a(self):
        # a can be a scalar.
        x = self.generate(6)
        b = self.convert_dtype([1, 0, -1])
        a = self.convert_dtype([1])
        y_r = self.convert_dtype([0, 1, 2, 2, 2, 2])

        y = lfilter(b, a[0], x)
        assert_array_almost_equal(y, y_r)

    def test_zi_some_singleton_dims(self):
        # lfilter doesn't really broadcast (no prepending of 1's).  But does
        # do singleton expansion if x and zi have the same ndim.  This was
        # broken only if a subset of the axes were singletons (gh-4681).
        x = self.convert_dtype(np.zeros((3,2,5), 'l'))
        b = self.convert_dtype(np.ones(5, 'l'))
        a = self.convert_dtype(np.array([1,0,0]))
        zi = np.ones((3,1,4), 'l')
        zi[1,:,:] *= 2
        zi[2,:,:] *= 3
        zi = self.convert_dtype(zi)

        zf_expected = self.convert_dtype(np.zeros((3,2,4), 'l'))
        y_expected = np.zeros((3,2,5), 'l')
        y_expected[:,:,:4] = [[[1]], [[2]], [[3]]]
        y_expected = self.convert_dtype(y_expected)

        # IIR
        y_iir, zf_iir = lfilter(b, a, x, -1, zi)
        assert_array_almost_equal(y_iir, y_expected)
        assert_array_almost_equal(zf_iir, zf_expected)

        # FIR
        y_fir, zf_fir = lfilter(b, a[0], x, -1, zi)
        assert_array_almost_equal(y_fir, y_expected)
        assert_array_almost_equal(zf_fir, zf_expected)

    def base_bad_size_zi(self, b, a, x, axis, zi):
        b = self.convert_dtype(b)
        a = self.convert_dtype(a)
        x = self.convert_dtype(x)
        zi = self.convert_dtype(zi)
        assert_raises(ValueError, lfilter, b, a, x, axis, zi)

    def test_bad_size_zi(self):
        # rank 1
        x1 = np.arange(6)
        self.base_bad_size_zi([1], [1], x1, -1, [1])
        self.base_bad_size_zi([1, 1], [1], x1, -1, [0, 1])
        self.base_bad_size_zi([1, 1], [1], x1, -1, [[0]])
        self.base_bad_size_zi([1, 1], [1], x1, -1, [0, 1, 2])
        self.base_bad_size_zi([1, 1, 1], [1], x1, -1, [[0]])
        self.base_bad_size_zi([1, 1, 1], [1], x1, -1, [0, 1, 2])
        self.base_bad_size_zi([1], [1, 1], x1, -1, [0, 1])
        self.base_bad_size_zi([1], [1, 1], x1, -1, [[0]])
        self.base_bad_size_zi([1], [1, 1], x1, -1, [0, 1, 2])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x1, -1, [0])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x1, -1, [[0], [1]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x1, -1, [0, 1, 2])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x1, -1, [0, 1, 2, 3])
        self.base_bad_size_zi([1, 1], [1, 1, 1], x1, -1, [0])
        self.base_bad_size_zi([1, 1], [1, 1, 1], x1, -1, [[0], [1]])
        self.base_bad_size_zi([1, 1], [1, 1, 1], x1, -1, [0, 1, 2])
        self.base_bad_size_zi([1, 1], [1, 1, 1], x1, -1, [0, 1, 2, 3])

        # rank 2
        x2 = np.arange(12).reshape((4,3))
        # for axis=0 zi.shape should == (max(len(a),len(b))-1, 3)
        self.base_bad_size_zi([1], [1], x2, 0, [0])

        # for each of these there are 5 cases tested (in this order):
        # 1. not deep enough, right # elements
        # 2. too deep, right # elements
        # 3. right depth, right # elements, transposed
        # 4. right depth, too few elements
        # 5. right depth, too many elements

        self.base_bad_size_zi([1, 1], [1], x2, 0, [0,1,2])
        self.base_bad_size_zi([1, 1], [1], x2, 0, [[[0,1,2]]])
        self.base_bad_size_zi([1, 1], [1], x2, 0, [[0], [1], [2]])
        self.base_bad_size_zi([1, 1], [1], x2, 0, [[0,1]])
        self.base_bad_size_zi([1, 1], [1], x2, 0, [[0,1,2,3]])

        self.base_bad_size_zi([1, 1, 1], [1], x2, 0, [0,1,2,3,4,5])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 0, [[[0,1,2],[3,4,5]]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 0, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 0, [[0,1],[2,3]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 0, [[0,1,2,3],[4,5,6,7]])

        self.base_bad_size_zi([1], [1, 1], x2, 0, [0,1,2])
        self.base_bad_size_zi([1], [1, 1], x2, 0, [[[0,1,2]]])
        self.base_bad_size_zi([1], [1, 1], x2, 0, [[0], [1], [2]])
        self.base_bad_size_zi([1], [1, 1], x2, 0, [[0,1]])
        self.base_bad_size_zi([1], [1, 1], x2, 0, [[0,1,2,3]])

        self.base_bad_size_zi([1], [1, 1, 1], x2, 0, [0,1,2,3,4,5])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 0, [[[0,1,2],[3,4,5]]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 0, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 0, [[0,1],[2,3]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 0, [[0,1,2,3],[4,5,6,7]])

        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 0, [0,1,2,3,4,5])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 0, [[[0,1,2],[3,4,5]]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 0, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 0, [[0,1],[2,3]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 0, [[0,1,2,3],[4,5,6,7]])

        # for axis=1 zi.shape should == (4, max(len(a),len(b))-1)
        self.base_bad_size_zi([1], [1], x2, 1, [0])

        self.base_bad_size_zi([1, 1], [1], x2, 1, [0,1,2,3])
        self.base_bad_size_zi([1, 1], [1], x2, 1, [[[0],[1],[2],[3]]])
        self.base_bad_size_zi([1, 1], [1], x2, 1, [[0, 1, 2, 3]])
        self.base_bad_size_zi([1, 1], [1], x2, 1, [[0],[1],[2]])
        self.base_bad_size_zi([1, 1], [1], x2, 1, [[0],[1],[2],[3],[4]])

        self.base_bad_size_zi([1, 1, 1], [1], x2, 1, [0,1,2,3,4,5,6,7])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 1, [[[0,1],[2,3],[4,5],[6,7]]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 1, [[0,1,2,3],[4,5,6,7]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 1, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1, 1, 1], [1], x2, 1, [[0,1],[2,3],[4,5],[6,7],[8,9]])

        self.base_bad_size_zi([1], [1, 1], x2, 1, [0,1,2,3])
        self.base_bad_size_zi([1], [1, 1], x2, 1, [[[0],[1],[2],[3]]])
        self.base_bad_size_zi([1], [1, 1], x2, 1, [[0, 1, 2, 3]])
        self.base_bad_size_zi([1], [1, 1], x2, 1, [[0],[1],[2]])
        self.base_bad_size_zi([1], [1, 1], x2, 1, [[0],[1],[2],[3],[4]])

        self.base_bad_size_zi([1], [1, 1, 1], x2, 1, [0,1,2,3,4,5,6,7])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 1, [[[0,1],[2,3],[4,5],[6,7]]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 1, [[0,1,2,3],[4,5,6,7]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 1, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1], [1, 1, 1], x2, 1, [[0,1],[2,3],[4,5],[6,7],[8,9]])

        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 1, [0,1,2,3,4,5,6,7])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 1, [[[0,1],[2,3],[4,5],[6,7]]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 1, [[0,1,2,3],[4,5,6,7]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 1, [[0,1],[2,3],[4,5]])
        self.base_bad_size_zi([1, 1, 1], [1, 1], x2, 1, [[0,1],[2,3],[4,5],[6,7],[8,9]])

    def test_empty_zi(self):
        # Regression test for #880: empty array for zi crashes.
        x = self.generate((5,))
        a = self.convert_dtype([1])
        b = self.convert_dtype([1])
        zi = self.convert_dtype([])
        y, zf = lfilter(b, a, x, zi=zi)
        assert_array_almost_equal(y, x)
        assert_equal(zf.dtype, self.dtype)
        assert_equal(zf.size, 0)

    def test_lfiltic_bad_zi(self):
        # Regression test for #3699: bad initial conditions
        a = self.convert_dtype([1])
        b = self.convert_dtype([1])
        # "y" sets the datatype of zi, so it truncates if int
        zi = lfiltic(b, a, [1., 0])
        zi_1 = lfiltic(b, a, [1, 0])
        zi_2 = lfiltic(b, a, [True, False])
        assert_array_equal(zi, zi_1)
        assert_array_equal(zi, zi_2)

    def test_do_not_modify_a_b_IIR(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, -1])
        b0 = b.copy()
        a = self.convert_dtype([0.5, -0.5])
        a0 = a.copy()
        y_r = self.convert_dtype([0, 2, 4, 6, 8, 10.])
        y_f = lfilter(b, a, x)
        assert_array_almost_equal(y_f, y_r)
        assert_equal(b, b0)
        assert_equal(a, a0)

    def test_do_not_modify_a_b_FIR(self):
        x = self.generate((6,))
        b = self.convert_dtype([1, 0, 1])
        b0 = b.copy()
        a = self.convert_dtype([2])
        a0 = a.copy()
        y_r = self.convert_dtype([0, 0.5, 1, 2, 3, 4.])
        y_f = lfilter(b, a, x)
        assert_array_almost_equal(y_f, y_r)
        assert_equal(b, b0)
        assert_equal(a, a0)

    def test_short_x_FIR(self):
        # regression test for #5116
        # x shorter than b, with non None zi fails
        a = self.convert_dtype([1])
        b = self.convert_dtype([1, 0, -1])
        zi = self.convert_dtype([2, 7])
        x = self.convert_dtype([72])
        ye = self.convert_dtype([74])
        zfe = self.convert_dtype([7, -72])
        y, zf = lfilter(b, a, x, zi=zi)
        assert_array_almost_equal(y, ye)
        assert_array_almost_equal(zf, zfe)

    def test_short_x_IIR(self):
        # regression test for #5116
        # x shorter than b, with non None zi fails
        a = self.convert_dtype([1, 1])
        b = self.convert_dtype([1, 0, -1])
        zi = self.convert_dtype([2, 7])
        x = self.convert_dtype([72])
        ye = self.convert_dtype([74])
        zfe = self.convert_dtype([-67, -72])
        y, zf = lfilter(b, a, x, zi=zi)
        assert_array_almost_equal(y, ye)
        assert_array_almost_equal(zf, zfe)


class TestLinearFilterFloat32(_TestLinearFilter):
    dtype = np.dtype('f')


class TestLinearFilterFloat64(_TestLinearFilter):
    dtype = np.dtype('d')


class TestLinearFilterFloatExtended(_TestLinearFilter):
    dtype = np.dtype('g')


class TestLinearFilterComplex64(_TestLinearFilter):
    dtype = np.dtype('F')


class TestLinearFilterComplex128(_TestLinearFilter):
    dtype = np.dtype('D')


class TestLinearFilterComplexExtended(_TestLinearFilter):
    dtype = np.dtype('G')

class TestLinearFilterDecimal(_TestLinearFilter):
    dtype = np.dtype('O')

    def type(self, x):
        return Decimal(str(x))


class TestLinearFilterObject(_TestLinearFilter):
    dtype = np.dtype('O')
    type = float


def test_lfilter_bad_object():
    # lfilter: object arrays with non-numeric objects raise TypeError.
    # Regression test for ticket #1452.
    assert_raises(TypeError, lfilter, [1.0], [1.0], [1.0, None, 2.0])
    assert_raises(TypeError, lfilter, [1.0], [None], [1.0, 2.0, 3.0])
    assert_raises(TypeError, lfilter, [None], [1.0], [1.0, 2.0, 3.0])


class _TestCorrelateReal(TestCase):
    dt = None

    def _setup_rank1(self):
        # a.size should be greater than b.size for the tests
        a = np.linspace(0, 3, 4).astype(self.dt)
        b = np.linspace(1, 2, 2).astype(self.dt)

        y_r = np.array([0, 2, 5, 8, 3]).astype(self.dt)
        return a, b, y_r

    def test_rank1_valid(self):
        a, b, y_r = self._setup_rank1()
        y = correlate(a, b, 'valid')
        assert_array_almost_equal(y, y_r[1:4])
        assert_equal(y.dtype, self.dt)

    def test_rank1_same(self):
        a, b, y_r = self._setup_rank1()
        y = correlate(a, b, 'same')
        assert_array_almost_equal(y, y_r[:-1])
        assert_equal(y.dtype, self.dt)

    def test_rank1_full(self):
        a, b, y_r = self._setup_rank1()
        y = correlate(a, b, 'full')
        assert_array_almost_equal(y, y_r)
        assert_equal(y.dtype, self.dt)

    def _setup_rank3(self):
        a = np.linspace(0, 39, 40).reshape((2, 4, 5), order='F').astype(
            self.dt)
        b = np.linspace(0, 23, 24).reshape((2, 3, 4), order='F').astype(
            self.dt)

        y_r = array([[[0., 184., 504., 912., 1360., 888., 472., 160.],
                      [46., 432., 1062., 1840., 2672., 1698., 864., 266.],
                      [134., 736., 1662., 2768., 3920., 2418., 1168., 314.],
                      [260., 952., 1932., 3056., 4208., 2580., 1240., 332.],
                      [202., 664., 1290., 1984., 2688., 1590., 712., 150.],
                      [114., 344., 642., 960., 1280., 726., 296., 38.]],

                     [[23., 400., 1035., 1832., 2696., 1737., 904., 293.],
                      [134., 920., 2166., 3680., 5280., 3306., 1640., 474.],
                      [325., 1544., 3369., 5512., 7720., 4683., 2192., 535.],
                      [571., 1964., 3891., 6064., 8272., 4989., 2324., 565.],
                      [434., 1360., 2586., 3920., 5264., 3054., 1312., 230.],
                      [241., 700., 1281., 1888., 2496., 1383., 532., 39.]],

                     [[22., 214., 528., 916., 1332., 846., 430., 132.],
                      [86., 484., 1098., 1832., 2600., 1602., 772., 206.],
                      [188., 802., 1698., 2732., 3788., 2256., 1018., 218.],
                      [308., 1006., 1950., 2996., 4052., 2400., 1078., 230.],
                      [230., 692., 1290., 1928., 2568., 1458., 596., 78.],
                      [126., 354., 636., 924., 1212., 654., 234., 0.]]],
                    dtype=self.dt)

        return a, b, y_r

    def test_rank3_valid(self):
        a, b, y_r = self._setup_rank3()
        y = correlate(a, b, "valid")
        assert_array_almost_equal(y, y_r[1:2, 2:4, 3:5])
        assert_equal(y.dtype, self.dt)

    def test_rank3_same(self):
        a, b, y_r = self._setup_rank3()
        y = correlate(a, b, "same")
        assert_array_almost_equal(y, y_r[0:-1, 1:-1, 1:-2])
        assert_equal(y.dtype, self.dt)

    def test_rank3_all(self):
        a, b, y_r = self._setup_rank3()
        y = correlate(a, b)
        assert_array_almost_equal(y, y_r)
        assert_equal(y.dtype, self.dt)


def _get_testcorrelate_class(datatype, base):
    class TestCorrelateX(base):
        dt = datatype
    TestCorrelateX.__name__ = "TestCorrelate%s" % datatype.__name__.title()
    return TestCorrelateX


for datatype in [np.ubyte, np.byte, np.ushort, np.short, np.uint, np.int,
                 np.ulonglong, np.ulonglong, np.float32, np.float64,
                 np.longdouble, Decimal]:
    cls = _get_testcorrelate_class(datatype, _TestCorrelateReal)
    globals()[cls.__name__] = cls


class _TestCorrelateComplex(TestCase):
    # The numpy data type to use.
    dt = None

    # The decimal precision to be used for comparing results.
    # This value will be passed as the 'decimal' keyword argument of
    # assert_array_almost_equal().
    decimal = None

    def _setup_rank1(self, mode):
        np.random.seed(9)
        a = np.random.randn(10).astype(self.dt)
        a += 1j * np.random.randn(10).astype(self.dt)
        b = np.random.randn(8).astype(self.dt)
        b += 1j * np.random.randn(8).astype(self.dt)

        y_r = (correlate(a.real, b.real, mode=mode) +
               correlate(a.imag, b.imag, mode=mode)).astype(self.dt)
        y_r += 1j * (-correlate(a.real, b.imag, mode=mode) +
                     correlate(a.imag, b.real, mode=mode))
        return a, b, y_r

    def test_rank1_valid(self):
        a, b, y_r = self._setup_rank1('valid')
        y = correlate(a, b, 'valid')
        assert_array_almost_equal(y, y_r, decimal=self.decimal)
        assert_equal(y.dtype, self.dt)

    def test_rank1_same(self):
        a, b, y_r = self._setup_rank1('same')
        y = correlate(a, b, 'same')
        assert_array_almost_equal(y, y_r, decimal=self.decimal)
        assert_equal(y.dtype, self.dt)

    def test_rank1_full(self):
        a, b, y_r = self._setup_rank1('full')
        y = correlate(a, b, 'full')
        assert_array_almost_equal(y, y_r, decimal=self.decimal)
        assert_equal(y.dtype, self.dt)

    def test_rank3(self):
        a = np.random.randn(10, 8, 6).astype(self.dt)
        a += 1j * np.random.randn(10, 8, 6).astype(self.dt)
        b = np.random.randn(8, 6, 4).astype(self.dt)
        b += 1j * np.random.randn(8, 6, 4).astype(self.dt)

        y_r = (correlate(a.real, b.real)
               + correlate(a.imag, b.imag)).astype(self.dt)
        y_r += 1j * (-correlate(a.real, b.imag) + correlate(a.imag, b.real))

        y = correlate(a, b, 'full')
        assert_array_almost_equal(y, y_r, decimal=self.decimal - 1)
        assert_equal(y.dtype, self.dt)


class TestCorrelate2d(TestCase):

    def test_consistency_correlate_funcs(self):
        # Compare np.correlate, signal.correlate, signal.correlate2d
        a = np.arange(5)
        b = np.array([3.2, 1.4, 3])
        for mode in ['full', 'valid', 'same']:
            assert_almost_equal(np.correlate(a, b, mode=mode),
                                signal.correlate(a, b, mode=mode))
            assert_almost_equal(np.squeeze(signal.correlate2d([a], [b],
                                                              mode=mode)),
                                signal.correlate(a, b, mode=mode))


# Create three classes, one for each complex data type. The actual class
# name will be TestCorrelateComplex###, where ### is the number of bits.
for datatype in [np.csingle, np.cdouble, np.clongdouble]:
    cls = _get_testcorrelate_class(datatype, _TestCorrelateComplex)
    cls.decimal = int(2 * np.finfo(datatype).precision / 3)
    globals()[cls.__name__] = cls


class TestLFilterZI(TestCase):

    def test_basic(self):
        a = np.array([1.0, -1.0, 0.5])
        b = np.array([1.0, 0.0, 2.0])
        zi_expected = np.array([5.0, -1.0])
        zi = lfilter_zi(b, a)
        assert_array_almost_equal(zi, zi_expected)

    def test_scale_invariance(self):
        # Regression test.  There was a bug in which b was not correctly
        # rescaled when a[0] was nonzero.
        b = np.array([2, 8, 5])
        a = np.array([1, 1, 8])
        zi1 = lfilter_zi(b, a)
        zi2 = lfilter_zi(2*b, 2*a)
        assert_allclose(zi2, zi1, rtol=1e-12)


class TestFiltFilt(TestCase):

    def test_basic(self):
        out = signal.filtfilt([1, 2, 3], [1, 2, 3], np.arange(12))
        assert_equal(out, arange(12))

    def test_sine(self):
        rate = 2000
        t = np.linspace(0, 1.0, rate + 1)
        # A signal with low frequency and a high frequency.
        xlow = np.sin(5 * 2 * np.pi * t)
        xhigh = np.sin(250 * 2 * np.pi * t)
        x = xlow + xhigh

        b, a = butter(8, 0.125)
        z, p, k = tf2zpk(b, a)
        # r is the magnitude of the largest pole.
        r = np.abs(p).max()
        eps = 1e-5
        # n estimates the number of steps for the
        # transient to decay by a factor of eps.
        n = int(np.ceil(np.log(eps) / np.log(r)))

        # High order lowpass filter...
        y = filtfilt(b, a, x, padlen=n)
        # Result should be just xlow.
        err = np.abs(y - xlow).max()
        assert_(err < 1e-4)

        # A 2D case.
        x2d = np.vstack([xlow, xlow + xhigh])
        y2d = filtfilt(b, a, x2d, padlen=n, axis=1)
        assert_equal(y2d.shape, x2d.shape)
        err = np.abs(y2d - xlow).max()
        assert_(err < 1e-4)

        # Use the previous result to check the use of the axis keyword.
        # (Regression test for ticket #1620)
        y2dt = filtfilt(b, a, x2d.T, padlen=n, axis=0)
        assert_equal(y2d, y2dt.T)

    def test_axis(self):
        # Test the 'axis' keyword on a 3D array.
        x = np.arange(10.0 * 11.0 * 12.0).reshape(10, 11, 12)
        b, a = butter(3, 0.125)
        y0 = filtfilt(b, a, x, padlen=0, axis=0)
        y1 = filtfilt(b, a, np.swapaxes(x, 0, 1), padlen=0, axis=1)
        assert_array_equal(y0, np.swapaxes(y1, 0, 1))
        y2 = filtfilt(b, a, np.swapaxes(x, 0, 2), padlen=0, axis=2)
        assert_array_equal(y0, np.swapaxes(y2, 0, 2))

    def test_acoeff(self):
        # test for 'a' coefficient as single number
        out = signal.filtfilt([.5, .5], 1, np.arange(10))
        assert_allclose(out, np.arange(10), rtol=1e-14, atol=1e-14)

    def test_gust_simple(self):
        # The input array has length 2.  The exact solution for this case
        # was computed "by hand".
        x = np.array([1.0, 2.0])
        b = np.array([0.5])
        a = np.array([1.0, -0.5])
        y, z1, z2 = _filtfilt_gust(b, a, x)
        assert_allclose([z1[0], z2[0]],
                        [0.3*x[0] + 0.2*x[1], 0.2*x[0] + 0.3*x[1]])
        assert_allclose(y, [z1[0] + 0.25*z2[0] + 0.25*x[0] + 0.125*x[1],
                            0.25*z1[0] + z2[0] + 0.125*x[0] + 0.25*x[1]])

    def test_gust_scalars(self):
        # The filter coefficients are both scalars, so the filter simply
        # multiplies its input by b/a.  When it is used in filtfilt, the
        # factor is (b/a)**2.
        x = np.arange(12)
        b = 3.0
        a = 2.0
        y = filtfilt(b, a, x, method="gust")
        expected = (b/a)**2 * x
        assert_allclose(y, expected)


def filtfilt_gust_opt(b, a, x):
    """
    An alternative implementation of filtfilt with Gustafsson edges.

    This function computes the same result as
    `scipy.signal.signaltools._filtfilt_gust`, but only 1-d arrays
    are accepted.  The problem is solved using `fmin` from `scipy.optimize`.
    `_filtfilt_gust` is significanly faster than this implementation.
    """
    def filtfilt_gust_opt_func(ics, b, a, x):
        """Objective function used in filtfilt_gust_opt."""
        m = max(len(a), len(b)) - 1
        z0f = ics[:m]
        z0b = ics[m:]
        y_f = lfilter(b, a, x, zi=z0f)[0]
        y_fb = lfilter(b, a, y_f[::-1], zi=z0b)[0][::-1]

        y_b = lfilter(b, a, x[::-1], zi=z0b)[0][::-1]
        y_bf = lfilter(b, a, y_b, zi=z0f)[0]
        value = np.sum((y_fb - y_bf)**2)
        return value

    m = max(len(a), len(b)) - 1
    zi = lfilter_zi(b, a)
    ics = np.concatenate((x[:m].mean()*zi, x[-m:].mean()*zi))
    result = fmin(filtfilt_gust_opt_func, ics, args=(b, a, x),
                  xtol=1e-10, ftol=1e-12,
                  maxfun=10000, maxiter=10000,
                  full_output=True, disp=False)
    opt, fopt, niter, funcalls, warnflag = result
    if warnflag > 0:
        raise RuntimeError("minimization failed in filtfilt_gust_opt: "
                           "warnflag=%d" % warnflag)
    z0f = opt[:m]
    z0b = opt[m:]

    # Apply the forward-backward filter using the computed initial
    # conditions.
    y_b = lfilter(b, a, x[::-1], zi=z0b)[0][::-1]
    y = lfilter(b, a, y_b, zi=z0f)[0]

    return y, z0f, z0b


def check_filtfilt_gust(b, a, shape, axis, irlen=None):
    # Generate x, the data to be filtered.
    np.random.seed(123)
    x = np.random.randn(*shape)

    # Apply filtfilt to x. This is the main calculation to be checked.
    y = filtfilt(b, a, x, axis=axis, method="gust", irlen=irlen)

    # Also call the private function so we can test the ICs.
    yg, zg1, zg2 = _filtfilt_gust(b, a, x, axis=axis, irlen=irlen)

    # filtfilt_gust_opt is an independent implementation that gives the
    # expected result, but it only handles 1-d arrays, so use some looping
    # and reshaping shenanigans to create the expected output arrays.
    xx = np.swapaxes(x, axis, -1)
    out_shape = xx.shape[:-1]
    yo = np.empty_like(xx)
    m = max(len(a), len(b)) - 1
    zo1 = np.empty(out_shape + (m,))
    zo2 = np.empty(out_shape + (m,))
    for indx in product(*[range(d) for d in out_shape]):
        yo[indx], zo1[indx], zo2[indx] = filtfilt_gust_opt(b, a, xx[indx])
    yo = np.swapaxes(yo, -1, axis)
    zo1 = np.swapaxes(zo1, -1, axis)
    zo2 = np.swapaxes(zo2, -1, axis)

    assert_allclose(y, yo, rtol=1e-9, atol=1e-10)
    assert_allclose(yg, yo, rtol=1e-9, atol=1e-10)
    assert_allclose(zg1, zo1, rtol=1e-9, atol=1e-10)
    assert_allclose(zg2, zo2, rtol=1e-9, atol=1e-10)


def test_filtfilt_gust():
    # Design a filter.
    b, a = signal.ellip(3, 0.01, 120, 0.0875)

    # Find the approximate impulse response length of the filter.
    z, p, k = tf2zpk(b, a)
    eps = 1e-10
    r = np.max(np.abs(p))
    approx_impulse_len = int(np.ceil(np.log(eps) / np.log(r)))

    np.random.seed(123)

    for irlen in [None, approx_impulse_len]:
        signal_len = 5 * approx_impulse_len

        # 1-d test case
        yield check_filtfilt_gust, b, a, (signal_len,), 0, irlen

        # 3-d test case; test each axis.
        for axis in range(3):
            shape = [2, 2, 2]
            shape[axis] = signal_len
            yield check_filtfilt_gust, b, a, shape, axis, irlen

    # Test case with length less than 2*approx_impulse_len.
    # In this case, `filtfilt_gust` should behave the same as if
    # `irlen=None` was given.
    length = 2*approx_impulse_len - 50
    yield check_filtfilt_gust, b, a, (length,), 0, approx_impulse_len


class TestDecimate(TestCase):

    def test_basic(self):
        x = np.arange(6)
        assert_array_equal(signal.decimate(x, 2, n=1).round(), x[::2])

    def test_shape(self):
        # Regression test for ticket #1480.
        z = np.zeros((10, 10))
        d0 = signal.decimate(z, 2, axis=0)
        assert_equal(d0.shape, (5, 10))
        d1 = signal.decimate(z, 2, axis=1)
        assert_equal(d1.shape, (10, 5))


class TestHilbert(object):

    def test_bad_args(self):
        x = np.array([1.0 + 0.0j])
        assert_raises(ValueError, hilbert, x)
        x = np.arange(8.0)
        assert_raises(ValueError, hilbert, x, N=0)

    def test_hilbert_theoretical(self):
        # test cases by Ariel Rokem
        decimal = 14

        pi = np.pi
        t = np.arange(0, 2 * pi, pi / 256)
        a0 = np.sin(t)
        a1 = np.cos(t)
        a2 = np.sin(2 * t)
        a3 = np.cos(2 * t)
        a = np.vstack([a0, a1, a2, a3])

        h = hilbert(a)
        h_abs = np.abs(h)
        h_angle = np.angle(h)
        h_real = np.real(h)

        # The real part should be equal to the original signals:
        assert_almost_equal(h_real, a, decimal)
        # The absolute value should be one everywhere, for this input:
        assert_almost_equal(h_abs, np.ones(a.shape), decimal)
        # For the 'slow' sine - the phase should go from -pi/2 to pi/2 in
        # the first 256 bins:
        assert_almost_equal(h_angle[0, :256],
                            np.arange(-pi / 2, pi / 2, pi / 256),
                            decimal)
        # For the 'slow' cosine - the phase should go from 0 to pi in the
        # same interval:
        assert_almost_equal(
            h_angle[1, :256], np.arange(0, pi, pi / 256), decimal)
        # The 'fast' sine should make this phase transition in half the time:
        assert_almost_equal(h_angle[2, :128],
                            np.arange(-pi / 2, pi / 2, pi / 128),
                            decimal)
        # Ditto for the 'fast' cosine:
        assert_almost_equal(
            h_angle[3, :128], np.arange(0, pi, pi / 128), decimal)

        # The imaginary part of hilbert(cos(t)) = sin(t) Wikipedia
        assert_almost_equal(h[1].imag, a0, decimal)

    def test_hilbert_axisN(self):
        # tests for axis and N arguments
        a = np.arange(18).reshape(3, 6)
        # test axis
        aa = hilbert(a, axis=-1)
        yield assert_equal, hilbert(a.T, axis=0), aa.T
        # test 1d
        yield assert_equal, hilbert(a[0]), aa[0]

        # test N
        aan = hilbert(a, N=20, axis=-1)
        yield assert_equal, aan.shape, [3, 20]
        yield assert_equal, hilbert(a.T, N=20, axis=0).shape, [20, 3]
        # the next test is just a regression test,
        # no idea whether numbers make sense
        a0hilb = np.array([0.000000000000000e+00 - 1.72015830311905j,
                           1.000000000000000e+00 - 2.047794505137069j,
                           1.999999999999999e+00 - 2.244055555687583j,
                           3.000000000000000e+00 - 1.262750302935009j,
                           4.000000000000000e+00 - 1.066489252384493j,
                           5.000000000000000e+00 + 2.918022706971047j,
                           8.881784197001253e-17 + 3.845658908989067j,
                          -9.444121133484362e-17 + 0.985044202202061j,
                          -1.776356839400251e-16 + 1.332257797702019j,
                          -3.996802888650564e-16 + 0.501905089898885j,
                           1.332267629550188e-16 + 0.668696078880782j,
                          -1.192678053963799e-16 + 0.235487067862679j,
                          -1.776356839400251e-16 + 0.286439612812121j,
                           3.108624468950438e-16 + 0.031676888064907j,
                           1.332267629550188e-16 - 0.019275656884536j,
                          -2.360035624836702e-16 - 0.1652588660287j,
                           0.000000000000000e+00 - 0.332049855010597j,
                           3.552713678800501e-16 - 0.403810179797771j,
                           8.881784197001253e-17 - 0.751023775297729j,
                           9.444121133484362e-17 - 0.79252210110103j])
        yield assert_almost_equal, aan[0], a0hilb, 14, 'N regression'


class TestHilbert2(object):

    def test_bad_args(self):
        # x must be real.
        x = np.array([[1.0 + 0.0j]])
        assert_raises(ValueError, hilbert2, x)

        # x must be rank 2.
        x = np.arange(24).reshape(2, 3, 4)
        assert_raises(ValueError, hilbert2, x)

        # Bad value for N.
        x = np.arange(16).reshape(4, 4)
        assert_raises(ValueError, hilbert2, x, N=0)
        assert_raises(ValueError, hilbert2, x, N=(2, 0))
        assert_raises(ValueError, hilbert2, x, N=(2,))


class TestPartialFractionExpansion(TestCase):
    def test_invresz_one_coefficient_bug(self):
        # Regression test for issue in gh-4646.
        r = [1]
        p = [2]
        k = [0]
        a_expected = [1.0, 0.0]
        b_expected = [1.0, -2.0]
        a_observed, b_observed = invresz(r, p, k)

        assert_allclose(a_observed, a_expected)
        assert_allclose(b_observed, b_expected)

    def test_invres_distinct_roots(self):
        # This test was inspired by github issue 2496.
        r = [3 / 10, -1 / 6, -2 / 15]
        p = [0, -2, -5]
        k = []
        a_expected = [1, 3]
        b_expected = [1, 7, 10, 0]
        a_observed, b_observed = invres(r, p, k)
        assert_allclose(a_observed, a_expected)
        assert_allclose(b_observed, b_expected)
        rtypes = ('avg', 'mean', 'min', 'minimum', 'max', 'maximum')

        # With the default tolerance, the rtype does not matter
        # for this example.
        for rtype in rtypes:
            a_observed, b_observed = invres(r, p, k, rtype=rtype)
            assert_allclose(a_observed, a_expected)
            assert_allclose(b_observed, b_expected)

        # With unrealistically large tolerances, repeated roots may be inferred
        # and the rtype comes into play.
        ridiculous_tolerance = 1e10
        for rtype in rtypes:
            a, b = invres(r, p, k, tol=ridiculous_tolerance, rtype=rtype)

    def test_invres_repeated_roots(self):
        r = [3 / 20, -7 / 36, -1 / 6, 2 / 45]
        p = [0, -2, -2, -5]
        k = []
        a_expected = [1, 3]
        b_expected = [1, 9, 24, 20, 0]
        rtypes = ('avg', 'mean', 'min', 'minimum', 'max', 'maximum')
        for rtype in rtypes:
            a_observed, b_observed = invres(r, p, k, rtype=rtype)
            assert_allclose(a_observed, a_expected)
            assert_allclose(b_observed, b_expected)

    def test_invres_bad_rtype(self):
        r = [3 / 20, -7 / 36, -1 / 6, 2 / 45]
        p = [0, -2, -2, -5]
        k = []
        assert_raises(ValueError, invres, r, p, k, rtype='median')


class TestVectorstrength(TestCase):

    def test_single_1dperiod(self):
        events = np.array([.5])
        period = 5.
        targ_strength = 1.
        targ_phase = .1

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 0)
        assert_equal(phase.ndim, 0)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_single_2dperiod(self):
        events = np.array([.5])
        period = [1, 2, 5.]
        targ_strength = [1.] * 3
        targ_phase = np.array([.5, .25, .1])

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 1)
        assert_equal(phase.ndim, 1)
        assert_array_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_equal_1dperiod(self):
        events = np.array([.25, .25, .25, .25, .25, .25])
        period = 2
        targ_strength = 1.
        targ_phase = .125

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 0)
        assert_equal(phase.ndim, 0)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_equal_2dperiod(self):
        events = np.array([.25, .25, .25, .25, .25, .25])
        period = [1, 2, ]
        targ_strength = [1.] * 2
        targ_phase = np.array([.25, .125])

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 1)
        assert_equal(phase.ndim, 1)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_spaced_1dperiod(self):
        events = np.array([.1, 1.1, 2.1, 4.1, 10.1])
        period = 1
        targ_strength = 1.
        targ_phase = .1

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 0)
        assert_equal(phase.ndim, 0)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_spaced_2dperiod(self):
        events = np.array([.1, 1.1, 2.1, 4.1, 10.1])
        period = [1, .5]
        targ_strength = [1.] * 2
        targ_phase = np.array([.1, .2])

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 1)
        assert_equal(phase.ndim, 1)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_partial_1dperiod(self):
        events = np.array([.25, .5, .75])
        period = 1
        targ_strength = 1. / 3.
        targ_phase = .5

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 0)
        assert_equal(phase.ndim, 0)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_partial_2dperiod(self):
        events = np.array([.25, .5, .75])
        period = [1., 1., 1., 1.]
        targ_strength = [1. / 3.] * 4
        targ_phase = np.array([.5, .5, .5, .5])

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 1)
        assert_equal(phase.ndim, 1)
        assert_almost_equal(strength, targ_strength)
        assert_almost_equal(phase, 2 * np.pi * targ_phase)

    def test_opposite_1dperiod(self):
        events = np.array([0, .25, .5, .75])
        period = 1.
        targ_strength = 0

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 0)
        assert_equal(phase.ndim, 0)
        assert_almost_equal(strength, targ_strength)

    def test_opposite_2dperiod(self):
        events = np.array([0, .25, .5, .75])
        period = [1.] * 10
        targ_strength = [0.] * 10

        strength, phase = vectorstrength(events, period)

        assert_equal(strength.ndim, 1)
        assert_equal(phase.ndim, 1)
        assert_almost_equal(strength, targ_strength)

    def test_2d_events_ValueError(self):
        events = np.array([[1, 2]])
        period = 1.
        assert_raises(ValueError, vectorstrength, events, period)

    def test_2d_period_ValueError(self):
        events = 1.
        period = np.array([[1]])
        assert_raises(ValueError, vectorstrength, events, period)

    def test_zero_period_ValueError(self):
        events = 1.
        period = 0
        assert_raises(ValueError, vectorstrength, events, period)

    def test_negative_period_ValueError(self):
        events = 1.
        period = -1
        assert_raises(ValueError, vectorstrength, events, period)


class TestSOSFilt(TestCase):

    # For sosfilt we only test a single datatype. Since sosfilt wraps
    # to lfilter under the hood, it's hopefully good enough to ensure
    # lfilter is extensively tested.
    dt = np.float64

    # The test_rank* tests are pulled from _TestLinearFilter
    def test_rank1(self):
        x = np.linspace(0, 5, 6).astype(self.dt)
        b = np.array([1, -1]).astype(self.dt)
        a = np.array([0.5, -0.5]).astype(self.dt)

        # Test simple IIR
        y_r = np.array([0, 2, 4, 6, 8, 10.]).astype(self.dt)
        assert_array_almost_equal(sosfilt(tf2sos(b, a), x), y_r)

        # Test simple FIR
        b = np.array([1, 1]).astype(self.dt)
        # NOTE: This was changed (rel. to TestLinear...) to add a pole @zero:
        a = np.array([1, 0]).astype(self.dt)
        y_r = np.array([0, 1, 3, 5, 7, 9.]).astype(self.dt)
        assert_array_almost_equal(sosfilt(tf2sos(b, a), x), y_r)

        b = [1, 1, 0]
        a = [1, 0, 0]
        x = np.ones(8)
        sos = np.concatenate((b, a))
        sos.shape = (1, 6)
        y = sosfilt(sos, x)
        assert_allclose(y, [1, 2, 2, 2, 2, 2, 2, 2])

    def test_rank2(self):
        shape = (4, 3)
        x = np.linspace(0, np.prod(shape) - 1, np.prod(shape)).reshape(shape)
        x = x.astype(self.dt)

        b = np.array([1, -1]).astype(self.dt)
        a = np.array([0.5, 0.5]).astype(self.dt)

        y_r2_a0 = np.array([[0, 2, 4], [6, 4, 2], [0, 2, 4], [6, 4, 2]],
                           dtype=self.dt)

        y_r2_a1 = np.array([[0, 2, 0], [6, -4, 6], [12, -10, 12],
                            [18, -16, 18]], dtype=self.dt)

        y = sosfilt(tf2sos(b, a), x, axis=0)
        assert_array_almost_equal(y_r2_a0, y)

        y = sosfilt(tf2sos(b, a), x, axis=1)
        assert_array_almost_equal(y_r2_a1, y)

    def test_rank3(self):
        shape = (4, 3, 2)
        x = np.linspace(0, np.prod(shape) - 1, np.prod(shape)).reshape(shape)

        b = np.array([1, -1]).astype(self.dt)
        a = np.array([0.5, 0.5]).astype(self.dt)

        # Test last axis
        y = sosfilt(tf2sos(b, a), x)
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                assert_array_almost_equal(y[i, j], lfilter(b, a, x[i, j]))

    def test_initial_conditions(self):
        b1, a1 = signal.butter(2, 0.25, 'low')
        b2, a2 = signal.butter(2, 0.75, 'low')
        b3, a3 = signal.butter(2, 0.75, 'low')
        b = np.convolve(np.convolve(b1, b2), b3)
        a = np.convolve(np.convolve(a1, a2), a3)
        sos = np.array((np.r_[b1, a1], np.r_[b2, a2], np.r_[b3, a3]))

        x = np.random.rand(50)

        # Stopping filtering and continuing
        y_true, zi = lfilter(b, a, x[:20], zi=np.zeros(6))
        y_true = np.r_[y_true, lfilter(b, a, x[20:], zi=zi)[0]]
        assert_allclose(y_true, lfilter(b, a, x))

        y_sos, zi = sosfilt(sos, x[:20], zi=np.zeros((3, 2)))
        y_sos = np.r_[y_sos, sosfilt(sos, x[20:], zi=zi)[0]]
        assert_allclose(y_true, y_sos)

        # Use a step function
        zi = sosfilt_zi(sos)
        x = np.ones(8)
        y, zf = sosfilt(sos, x, zi=zi)

        assert_allclose(y, np.ones(8))
        assert_allclose(zf, zi)

        # Initial condition shape matching
        x.shape = (1, 1) + x.shape  # 3D
        assert_raises(ValueError, sosfilt, sos, x, zi=zi)
        zi_nd = zi.copy()
        zi_nd.shape = (zi.shape[0], 1, 1, zi.shape[-1])
        assert_raises(ValueError, sosfilt, sos, x,
                      zi=zi_nd[:, :, :, [0, 1, 1]])
        y, zf = sosfilt(sos, x, zi=zi_nd)
        assert_allclose(y[0, 0], np.ones(8))
        assert_allclose(zf[:, 0, 0, :], zi)

    def test_initial_conditions_3d_axis1(self):
        # Test the use of zi when sosfilt is applied to axis 1 of a 3-d input.

        # Input array is x.
        np.random.seed(159)
        x = np.random.randint(0, 5, size=(2, 15, 3))

        # Design a filter in SOS format.
        sos = signal.butter(6, 0.35, output='sos')
        nsections = sos.shape[0]

        # Filter along this axis.
        axis = 1

        # Initial conditions, all zeros.
        shp = list(x.shape)
        shp[axis] = 2
        shp = [nsections] + shp
        z0 = np.zeros(shp)

        # Apply the filter to x.
        yf, zf = sosfilt(sos, x, axis=axis, zi=z0)

        # Apply the filter to x in two stages.
        y1, z1 = sosfilt(sos, x[:, :5, :], axis=axis, zi=z0)
        y2, z2 = sosfilt(sos, x[:, 5:, :], axis=axis, zi=z1)

        # y should equal yf, and z2 should equal zf.
        y = np.concatenate((y1, y2), axis=axis)
        assert_allclose(y, yf, rtol=1e-10, atol=1e-13)
        assert_allclose(z2, zf, rtol=1e-10, atol=1e-13)

    def test_bad_zi_shape(self):
        # The shape of zi is checked before using any values in the
        # arguments, so np.empty is fine for creating the arguments.
        x = np.empty((3, 15, 3))
        sos = np.empty((4, 6))
        zi = np.empty((4, 3, 3, 2))  # Correct shape is (4, 3, 2, 3)
        assert_raises(ValueError, sosfilt, sos, x, zi=zi, axis=1)

    def test_sosfilt_zi(self):
        sos = signal.butter(6, 0.2, output='sos')
        zi = sosfilt_zi(sos)

        y, zf = sosfilt(sos, np.ones(40), zi=zi)
        assert_allclose(zf, zi, rtol=1e-13)

        # Expected steady state value of the step response of this filter:
        ss = np.prod(sos[:, :3].sum(axis=-1) / sos[:, 3:].sum(axis=-1))
        assert_allclose(y, ss, rtol=1e-13)

if __name__ == "__main__":
    run_module_suite()
