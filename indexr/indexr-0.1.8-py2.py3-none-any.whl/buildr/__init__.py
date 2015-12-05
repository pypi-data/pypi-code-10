def buildr(files, index_path, **kwargs):
    """
    Build an index.

    Optional parameters:
        indexer:        Indexing algorithm. The indexr package already has predefined algorithms in the
                        indexr.buildr.indexing submodule (default: indexr.buildr.indexing.BSB).
        force_rebuild:  Whether or not to rebuild the index.

    :param files:       List of files to include in the index.
    :type  files:       list
    :param index_path:  The path where all index files will be stored.
    :type  index_path:  str
    :param kwargs:      Optional parameters.
    :return             The index.
    """

    # Fetch the indexing algorithm
    indexer = kwargs.get('indexer', None)
    force_rebuild = kwargs.get('force_rebuild', False)
    if indexer is None:
        from indexr.buildr.indexing.BSB import BSB
    indexer.initialize(files, index_path)
    if not indexer.index_exists() or force_rebuild:
        indexer.construct()

    return indexer
