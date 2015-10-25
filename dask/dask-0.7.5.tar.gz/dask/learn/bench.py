from time import time

from sklearn.svm import LinearSVC
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_selection import SelectFdr
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.pipeline
import sklearn.grid_search
import numpy as np

import dask.learn as dl
import dask.imperative as di
import dask

results = []
dask_pipeline = dl.Pipeline([("count", CountVectorizer()),
                         ("select_fdr", SelectFdr()),
                         ("svm", LinearSVC())])
skl_pipeline = sklearn.pipeline.Pipeline([("count", CountVectorizer()),
                         ("select_fdr", SelectFdr()),
                         ("svm", LinearSVC())])

categories = [
    'alt.atheism',
    'talk.religion.misc',
]

data_train = fetch_20newsgroups(subset='train', categories=categories)
data_test = fetch_20newsgroups(subset='test', categories=categories)
X_train, y_train = data_train.data, data_train.target
X_test, y_test = data_test.data, data_test.target

param_grid = {'select_fdr__alpha': [0.05, 0.01, 0.1, 0.2],
              'svm__C': np.logspace(-3, 2, 3)}

start = time()
grid = dl.GridSearchCV(dask_pipeline, param_grid)
with dask.set_options(get=dask.async.get_sync):
    grid.fit(X_train, y_train)
    result = grid.score(X_test, y_test)
print(result, time() - start)
grid._dask_value.visualize('gridsearch.pdf')


"""
start = time()
grid = sklearn.grid_search.GridSearchCV(skl_pipeline, param_grid)
grid.fit(X_train, y_train)
result = grid.score(X_test, y_test)
print(result, time() - start)
"""
