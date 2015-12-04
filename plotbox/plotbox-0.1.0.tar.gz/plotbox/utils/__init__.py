
import numpy as np
import pandas as pd

def get_config():
    import plotly
    cred = plotly.tools.get_credentials_file()
    config = plotly.tools.get_config_file()
    return cred, config

def df_to_arrays(df, cols):
    '''function to easily convert data types
    Takes a df and a list of column names, returns a list of arrays in same order

    '''
    arrays = [df[c] for c in cols]
    return arrays

def arrays_to_df(arrays, names=None):
    '''function to easily convert data types
    Takes a list of arrays, returns a pandas dataframe in same order

    '''
    df = pd.DataFrame(arrays).T
    if names:
        df.columns = names
    return df

def mreplace(s, dic):
    for i, j in dic.iteritems():
        s = s.replace(i, j)
    return s