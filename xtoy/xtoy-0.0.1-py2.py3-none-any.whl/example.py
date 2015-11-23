import sys
sys.path.append('..')

import pandas as pd
import numpy as np

from xtoy.prep import Sparsify
from xtoy.toys import Toy

from gplearn.genetic import SymbolicTransformer

z = np.array(pd.read_csv('/Users/pascal/Downloads/train (1).csv'))


X, y = z[:, 2:], np.array(z[:, 1], dtype=float)

X = np.hstack((np.reshape(X[:, 0], (len(y), 1)), X[:, 2:])).shape

toy = Toy()

gp = SymbolicTransformer(generations=20, population_size=2000,
                         hall_of_fame=100, n_components=10,
                         parsimony_coefficient=0.0005,
                         max_samples=0.9, verbose=1,
                         random_state=0, n_jobs=3)


s = Sparsify().fit(X)

XX = s.transform(X).todense()

XXX = gp.fit_transform(XX, y)

toy.fit(np.hstack((X, np.abs(XXX + np.max(XXX, 0)))), y)

Xtest = np.array(pd.read_csv('/Users/pascal/Downloads/test (1).csv'))

XXXtest = gp.transform(s.transform(Xtest[:, 1:]).todense())

predictions = toy.predict(np.hstack((Xtest[:, 1:], np.abs(XXXtest + np.max(XXXtest, 0)))))

Xtest = np.hstack((np.reshape(Xtest[:, 1], (len(Xtest[:, 1:]), 1)), Xtest[:, 3:]))

predictions = toy.predict(Xtest)

df = pd.DataFrame({'PassengerId': Xtest[:, 0], 'Survived': predictions})
df['Survived'] = df['Survived'].astype(int)
df.to_csv('apremovedname.csv', index=False)

# from sklearn.datasets import load_digits
# digits = load_digits()
# X, y = np.reshape(digits.images, (1797, 8 * 8)), digits.target


# rf n_est = 20
{"clf__min_samples_split": 20, "tsvd__n_iter": 20, "tsvd__n_components": 10, "clf__min_samples_leaf": 5,
    "clf__max_features": "sqrt", "clf__max_depth": 20, "clf__n_estimators": 20, "clf__class_weight": "balanced"}

# ridge
{"clf__alpha": 1.7, "tsvd__n_components": 200, "tsvd__n_iter": 5}

# rf n_est = 200
{"tsvd__n_iter": 5, "clf__min_samples_split": 10, "tsvd__n_components": 100, "clf__class_weight": "balanced",
    "clf__max_features": "log2", "clf__n_estimators": 200, "clf__min_samples_leaf": 5, "clf__max_depth": null}


from sklearn.feature_selection import RFE

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import SGDClassifier

rfe = RFE(LogisticRegression())
rfe.fit(XXd, y)

from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()
model.fit(XXd, y)
# display the relative importance of each attribute
print(model.feature_importances_)


XXd = XX.todense()


def test_titanic_data():
    z = np.array(pd.read_csv('/Users/pascal/Downloads/train (1).csv'))
    X, y = z[:, 2:], np.array(z[:, 1], dtype=float)
    assert apply_toy_on(X, y) > 0.7
