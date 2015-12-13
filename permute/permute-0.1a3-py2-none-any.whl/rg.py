from __future__ import division, print_function, absolute_import

import numpy as np

from scipy.stats import linregress

import matplotlib.pyplot as plt


X = np.array([np.ones(10), np.random.random_integers(1, 4, 10)]).T
beta = np.array([1.2, 2])
epsilon = np.random.normal(0, .15, 10)
y = X.dot(beta) + epsilon

slope, intercept, rval, pval, stderr = linregress(X[:, 1], y)

yhat = slope*X[:, 1] + intercept
epsilon_hat = y - yhat

print('r-squared:', rval**2)
print('p_value', pval)
print('standard deviation', stderr)

plt.plot(X[:, 1], yhat, 'r-', X[:, 1], y, 'o')
plt.show()

intercepts = np.empty(10000)
for i in range(10000):
    np.random.shuffle(epsilon_hat)
    ynew = X.dot(beta) + epsilon_hat
    slope, intercepts[i], rval, pval, stderr = linregress(X[:, 1], ynew)


