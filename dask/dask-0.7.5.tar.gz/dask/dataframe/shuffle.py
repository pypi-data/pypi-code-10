from __future__ import absolute_import, division, print_function

from collections import Iterator
import uuid

import numpy as np
import pandas as pd
from toolz import merge

from ..optimize import cull
from ..base import tokenize
from .core import DataFrame, Series, _Frame
from .utils import (strip_categories, shard_df_on_index, _categorize,
                    get_categories)


def set_index(df, index, npartitions=None, compute=True, **kwargs):
    """ Set DataFrame index to new column

    Sorts index and realigns Dataframe to new sorted order.

    This shuffles and repartitions your data.  If done in parallel the
    resulting order is non-deterministic.
    """
    if isinstance(index, (DataFrame, tuple, list)):
        raise NotImplementedError(
            "Dask dataframe does not yet support multi-indexes.\n"
            "You tried to index with this index: %s\n"
            "Indexes must be single columns only." % str(index))

    npartitions = npartitions or df.npartitions
    if not isinstance(index, Series):
        index2 = df[index]
    else:
        index2 = index

    divisions = (index2
                  .quantile(np.linspace(0, 1, npartitions+1))
                  .compute()).tolist()
    return set_partition(df, index, divisions, compute=compute, **kwargs)


def new_categories(categories, index):
    """ Flop around index for '.index' """
    if index in categories:
        categories = categories.copy()
        categories['.index'] = categories.pop(index)
    return categories


def set_partition(df, index, divisions, compute=False, **kwargs):
    """ Group DataFrame by index

    Sets a new index and partitions data along that index according to
    divisions.  Divisions are often found by computing approximate quantiles.
    The function ``set_index`` will do both of these steps.

    Parameters
    ----------
    df: DataFrame/Series
        Data that we want to re-partition
    index: string or Series
        Column to become the new index
    divisions: list
        Values to form new divisions between partitions

    See Also
    --------
    set_index
    shuffle
    partd
    """
    if isinstance(index, _Frame):
        assert df.divisions == index.divisions
        columns = df.columns
    else:
        columns = tuple([c for c in df.columns if c != index])

    token = tokenize(df, index, divisions)
    always_new_token = uuid.uuid1().hex
    import partd

    p = ('zpartd-' + always_new_token,)

    # Get Categories
    catname = 'set-partition--get-categories-old-' + always_new_token
    catname2 = 'set-partition--get-categories-new-' + always_new_token

    dsk1 = {catname: (get_categories, df._keys()[0]),
            p: (partd.PandasBlocks, (partd.Buffer, (partd.Dict,), (partd.File,))),
            catname2: (new_categories, catname,
                            index.name if isinstance(index, Series) else index)}

    # Partition data on disk
    name = 'set-partition--partition-' + always_new_token
    if isinstance(index, _Frame):
        dsk2 = dict(((name, i),
                     (_set_partition, part, ind, divisions, p))
                     for i, (part, ind)
                     in enumerate(zip(df._keys(), index._keys())))
    else:
        dsk2 = dict(((name, i),
                     (_set_partition, part, index, divisions, p))
                     for i, part
                     in enumerate(df._keys()))

    # Barrier
    barrier_token = 'barrier-' + always_new_token
    dsk3 = {barrier_token: (barrier, list(dsk2))}

    if compute:
        dsk = merge(df.dask, dsk1, dsk2, dsk3)
        if isinstance(index, _Frame):
            dsk.update(index.dask)
        p, barrier_token, categories = df._get(dsk, [p, barrier_token, catname], **kwargs)
        dsk4 = {catname2: categories}
    else:
        dsk4 = {}

    # Collect groups
    name = 'set-partition--collect-' + token
    if compute and not categories:
        dsk4.update(dict(((name, i),
                     (_set_collect, i, p, barrier_token, df.columns))
                     for i in range(len(divisions) - 1)))
    else:
        dsk4.update(dict(((name, i),
                     (_categorize, catname2,
                        (_set_collect, i, p, barrier_token, df.columns)))
                    for i in range(len(divisions) - 1)))

    dsk = merge(df.dask, dsk1, dsk2, dsk3, dsk4)
    if isinstance(index, _Frame):
        dsk.update(index.dask)

    if compute:
        dsk = cull(dsk, list(dsk4.keys()))

    return DataFrame(dsk, name, columns, divisions)


def barrier(args):
    list(args)
    return 0

def _set_partition(df, index, divisions, p):
    """ Shard partition and dump into partd """
    df = df.set_index(index)
    df = strip_categories(df)
    divisions = list(divisions)
    shards = shard_df_on_index(df, divisions[1:-1])
    p.append(dict(enumerate(shards)))


def _set_collect(group, p, barrier_token, columns):
    """ Get new partition dataframe from partd """
    try:
        return p.get(group)
    except ValueError:
        assert columns is not None, columns
        # when unable to get group, create dummy DataFrame
        # which has the same columns as original
        return pd.DataFrame(columns=columns)


def shuffle(df, index, npartitions=None):
    """ Group DataFrame by index

    Hash grouping of elements.  After this operation all elements that have
    the same index will be in the same partition.  Note that this requires
    full dataset read, serialization and shuffle.  This is expensive.  If
    possible you should avoid shuffles.

    This does not preserve a meaningful index/partitioning scheme.  This is not
    deterministic if done in parallel.

    See Also
    --------
    set_index
    set_partition
    partd
    """
    if isinstance(index, _Frame):
        assert df.divisions == index.divisions
    if npartitions is None:
        npartitions = df.npartitions

    token = tokenize(df, index, npartitions)
    always_new_token = uuid.uuid1().hex

    import partd
    p = ('zpartd-' + always_new_token,)
    dsk1 = {p: (partd.PandasBlocks, (partd.Buffer, (partd.Dict,),
                                                   (partd.File,)))}

    # Partition data on disk
    name = 'shuffle-partition-' + always_new_token
    if isinstance(index, _Frame):
        dsk2 = dict(((name, i),
                     (partition, part, ind, npartitions, p))
                     for i, (part, ind)
                     in enumerate(zip(df._keys(), index._keys())))
    else:
        dsk2 = dict(((name, i),
                     (partition, part, index, npartitions, p))
                     for i, part
                     in enumerate(df._keys()))

    # Barrier
    barrier_token = 'barrier-' + always_new_token
    dsk3 = {barrier_token: (barrier, list(dsk2))}

    # Collect groups
    name = 'shuffle-collect-' + token
    dsk4 = dict(((name, i),
                 (collect, i, p, barrier_token))
                for i in range(npartitions))

    divisions = [None] * (npartitions + 1)

    dsk = merge(df.dask, dsk1, dsk2, dsk3, dsk4)
    if isinstance(index, _Frame):
        dsk.update(index.dask)

    return DataFrame(dsk, name, df.columns, divisions)


def partition(df, index, npartitions, p):
    """ Partition a dataframe along a grouper, store partitions to partd """
    rng = pd.Series(np.arange(len(df)))
    if isinstance(index, Iterator):
        index = list(index)
    if not isinstance(index, (pd.Index, pd.Series, pd.DataFrame)):
        index = df[index]

    if isinstance(index, pd.Index):
        groups = rng.groupby([abs(hash(x)) % npartitions for x in index])
    if isinstance(index, pd.Series):
        groups = rng.groupby(index.map(lambda x: abs(hash(x)) % npartitions).values)
    elif isinstance(index, pd.DataFrame):
        groups = rng.groupby(index.apply(
                    lambda row: abs(hash(tuple(row))) % npartitions,
                    axis=1).values)
    d = dict((i, df.iloc[groups.groups[i]]) for i in range(npartitions)
                                            if i in groups.groups)
    p.append(d)


def collect(group, p, barrier_token):
    """ Collect partitions from partd, yield dataframes """
    return p.get(group)
