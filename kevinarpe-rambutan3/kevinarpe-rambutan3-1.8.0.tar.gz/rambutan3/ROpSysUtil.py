"""This module is fully tested."""

import os

from rambutan3 import RIterableUtil
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.op_sys.RFileAccessEnum import RFileAccessEnum
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.NON_EMPTY_STR import NON_EMPTY_STR
from rambutan3.check_args.annotation.ONE_OR_MORE_OF import ONE_OR_MORE_OF


# Ref: https://docs.python.org/3/library/os.html#os.supports_effective_ids
__SUPPORTS_EFFECTIVE_IDS_FLAG = (os.access in os.supports_effective_ids)


@check_args
def access(path: NON_EMPTY_STR,
           modes: ONE_OR_MORE_OF(INSTANCE_OF(RFileAccessEnum)),
           *,
           effective_ids: BOOL=True) -> BOOL:
    """
    Check current user's permissions for a file system path.

    On POSIX compatibile systems, this effectively calls access() or faccessat()

    @param path
           file system path, e.g., '/a/b/c'
           can be for any type of object, e.g., regular file, directory, named pipe, socket, etc.
    @param modes
           one or more access types to check
    @param effective_ids
           default value is different from Python3 standard (False -> True)
           using {@code True} enumlates the '-r', '-w', and '-x' operators in Perl
           using {@code False} enumlates the '-R', '-W', and '-X' operators in Perl

    @return {@code True} if current user has access to all {@code modes} on the file
            else: {@code False}

    @see http://stackoverflow.com/a/15655273/257299
    """

    # Ref: https://docs.python.org/3/library/os.html#os.access
    # If effective_ids is True, access() will perform its access checks using the effective uid/gid instead of the real
    # uid/gid. effective_ids may not be supported on your platform; you can check whether or not it is available using
    # os.supports_effective_ids. If it is unavailable, using it will raise a NotImplementedError.
    if not __SUPPORTS_EFFECTIVE_IDS_FLAG and effective_ids:
        adj_effective_ids = False
    else:
        adj_effective_ids = effective_ids

    # follow_symlinks=False is useless to me.  Maybe we will add option later.
    x = all(os.access(path, m.value, effective_ids=adj_effective_ids, follow_symlinks=True)
            for m in RIterableUtil.make_iterable(modes))

    return x
