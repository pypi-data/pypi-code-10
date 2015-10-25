from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
import numpy as np

import dask.learn as dl
import dask.imperative as di
import dask

iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target)


from dask.diagnostics import Profiler, ResourceProfiler, visualize

pipeline = dask_pipeline


def test_grid_search():
    pipeline = dl.Pipeline([("pca", PCA()),
                            ("select_k", SelectKBest()),
                            ("svm", LinearSVC())])
    param_grid = {'select_k__k': [1, 2, 3, 4],
                  'svm__C': np.logspace(-3, 2, 6)}
    grid = dl.GridSearchCV(pipeline, param_grid)

    with dask.set_options(get=dask.async.get_sync):
        grid.fit(X_train, y_train)
        result = grid.score(X_test, y_test)
        print(result)


def test_grid_search_sklearn():
    from sklearn.pipeline import Pipeline
    from sklearn.grid_search import GridSearchCV

    pipeline = Pipeline([("pca", PCA()),
                            ("select_k", SelectKBest()),
                            ("svm", LinearSVC())])
    param_grid = {'select_k__k': [1, 2, 3, 4],
                  'svm__C': np.logspace(-3, 2, 6)}
    grid = GridSearchCV(pipeline, param_grid)
    grid.fit(X_train, y_train)

    result = grid.score(X_test, y_test)

if __name__ == '__main__':
    test_grid_search()
