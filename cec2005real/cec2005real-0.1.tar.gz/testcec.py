from cec2005real.cec2005 import Function
import numpy as np

b = Function(1, 10)
print(b.info())
f = b.get_eval_function()
x = np.zeros(10)
fitness = f(x)
print("fitness: {}".format(fitness))
        
