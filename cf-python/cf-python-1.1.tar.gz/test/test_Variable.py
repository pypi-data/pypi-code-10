import os
import numpy
import cf
import unittest
import inspect

class VariableTest(unittest.TestCase):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'test_file.nc')
    chunk_sizes = (17, 34, 300, 100000)[::-1]
    original_chunksize = cf.CHUNKSIZE()

    f = cf.read(filename)[0]  

    test_only = ()

    def test_Variable_max_mean_mid_range_min_range_sd_sum_var(self):    
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return
            
        for chunksize in self.chunk_sizes:            
            f = cf.read(self.filename)[0]

            self.assertTrue(f.max()       == f.data.max(squeeze=True))
            self.assertTrue(f.mean()      == f.data.mean(squeeze=True))
            self.assertTrue(f.mid_range() == f.data.mid_range(squeeze=True))
            self.assertTrue(f.min()       == f.data.min(squeeze=True))
            self.assertTrue(f.range()     == f.data.range(squeeze=True))
            self.assertTrue(f.sd()        == f.data.sd(squeeze=True))
            self.assertTrue(f.sum()       == f.data.sum(squeeze=True))
            self.assertTrue(f.var()       == f.data.var(squeeze=True))
        #--- End: for    
        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def
        
#--- End: class
        
if __name__ == '__main__':
    print 'cf-python version:', cf.__version__
    print 'cf-python path:'   , os.path.abspath(cf.__file__)
    print''
    unittest.main(verbosity=2)
