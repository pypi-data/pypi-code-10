#!/usr/bin/env python3

import matplotlib.pyplot as plt
import scisalt.matplotlib as sm
import numpy as np

n_lines = 10

fig, ax = sm.setup_axes()

x = np.linspace(0, 10)
for shift in np.linspace(0, np.pi, n_lines):
    ax.plot(x, np.sin(x - shift), linewidth=2)

plt.show()
