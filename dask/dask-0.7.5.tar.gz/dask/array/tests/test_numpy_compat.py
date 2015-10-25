from dask.array.numpy_compat import divide
import numpy as np

def test_divide():
    assert divide(np.float32(4.0), np.float32(2.0), dtype='f8').dtype == 'f8'
