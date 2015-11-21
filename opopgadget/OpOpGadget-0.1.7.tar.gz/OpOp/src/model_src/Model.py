import numpy as np

class Model:

    def __init__(self):
        self.use_c=use_c

    def dens(self,R):
        return self._evaluatedens(R)

    def mass(self,R):
        if self.use_c==True: mass=self._evaluatemassc
        else: mass=np.vectorize(self._evaluatemass)
        return mass(R)

    def pot(self,R):
        if self.use_c==True: pot=self._evaluatepotc
        else:pot=np.vectorize(self._evaluatepot)
        return pot(R)







