'''
Created on May 3, 2015

@author: stou
'''

import os

class lut(object):
  """Represents a colormap (.lut) file"""

  def __init__(self, filename=None):

    self.name = None

    if filename:
      self.open(filename)
      import os
    else:
      self.cnots = [[0, 0.0, 0.0, 0.0], [255, 1.0, 1.0, 1.0]]
      self.anots = [[0, 0.0], [255, 1.0]]

  def open(self, filename):
    """ Load .lut from `filename` """

    f = open(filename, 'r')
    self.load(f.readlines())
    f.close()

    self.name = os.path.splitext(os.path.basename(filename))[0]

  def load(self, lut_lines):
    """ Parse lut lines """

    self.anots = [self.line_to_not(l) for l in lut_lines if l.startswith('Anot')]
    self.cnots = [self.line_to_not(l) for l in lut_lines if l.startswith('Cnot')]

  def save(self, filename):
    """ Save a lut to the given `filename`"""

    f = open(filename, 'w')
    f.write(self.__str__())
    f.close()

  def line_to_not(self, line):

    s = [k for k in line[5:].strip().split(' ')]

    d = [int(s[0])]
    d.extend([float(i) for i in s[1:]])

    return d

  def getFunctions(self):
    import numpy as np
    from scipy.interpolate import interp1d

    anot_array = np.array(self.anots, dtype=np.float32)
    cnot_array = np.array(self.cnots, dtype=np.float32).reshape(-1, 4)

    f_color = interp1d(cnot_array[:, 0], cnot_array[:, 1:].T)
    f_alpha = interp1d(anot_array[:, 0], anot_array[:, 1])

    return f_color, f_alpha

  def rgba1D(self, size=None):
    import numpy as np

    f_color, f_alpha = self.getFunctions()
    x = np.arange(size or 256, dtype=np.float32)

    return np.vstack((f_color(x), f_alpha(x))).T

  def __str__(self):

    lines = []

    for n in self.cnots:
      line = 'Cnot:\t%i %s' % (n[0], ' '.join('%0.9f' % k for k in n[1:]))
      lines.append(line)

    for n in self.anots:
      line = 'Anot:\t%i %s' % (n[0], ' '.join('%0.9f' % k for k in n[1:]))
      lines.append(line)

    return '\n'.join(lines)

if __name__ == '__main__':
  import sys
  print lut(filename=sys.argv[1])

