"""
Algorithms for imputing missing values in data
"""
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.cross_decomposition import PLSRegression

def plsimp(df):
    """
    A simple implementation of a least-squares approach to imputation using partial least squares
    regression (PLS).
    
    """
    df = df.copy()
    df[ np.isinf(df) ] = np.nan

    dfo = df.dropna(how='any', axis=0)
    dfo = dfo.astype(np.float64)
    
    imputed_n = np.sum(np.isnan(dfi.values), axis=1)
    
    # All this is just to ensure we don't bugger up the columns
    idx = list(dfi.index.names)
    col = dfi.columns

    dfi = df.copy()
    dfi = dfi.reset_index()
    dfi['ImputedN'] = imputed
    idx.extend(['ImputedN'])
    dfi.set_index(idx, inplace=True)
    dfi.columns = col
    
    # List of proteins with missing values in their rows
    missing_values = df[ np.sum(np.isnan(df), axis=1) > 0 ].index
    ix_mask = np.arange(0, df.shape[1])
    total_n = len(missing_values)

    plsr = PLSRegression(n_components=2)
    
    for n, p in enumerate(missing_values):
        # Generate model for this protein from missing data
        target = df.loc[p].values.copy().T
        ixes = ix_mask[ np.isnan(target) ]
        
        # Fill missing values with row median for calculation
        target[np.isnan(target)] = np.nanmedian(target)
        plsr.fit(dfo.values.T, target)
        
        # For each missing value, calculate imputed value from the column data input
        for ix in ixes:
            imputv = plsr.predict(dfo.iloc[:, ix])[0]
            dfi.loc[p].ix[ix] = imputv

        print("%d%%" % ((n/total_n)*100), end="\r")

    return dfi