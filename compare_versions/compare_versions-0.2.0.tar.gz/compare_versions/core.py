from . import schemes

VALID_COMPARISONS=['eq','ne','gt','lt','ge','le']

def is_valid(version):
    try:
        schemes.schemes['semver'](version)
    except schemes.InvalidVersionError:
        return False
    return True

def verify_list(versions, comparison='lt', scheme='semver'):
    """
    Verify that a list of versions all match comparison
    Returns True if the versions are in order

    Arguments:
    versions -- a list of version strings
    comparison -- the comparison to evaluate on the list
    scheme -- the versioning scheme to use
    """
    if len(versions) < 2:
        raise ValueError('You must provide at least two versions to compare')

    if comparison not in VALID_COMPARISONS:
        raise ValueError('Invalid comparison "%s" - options are %s' % (comparison, '/'.join(c for c in VALID_COMPARISONS)))

    if scheme not in schemes.schemes:
        raise ValueError('Invalid scheme "%s" - options are %s' % (scheme, '/'.join(s for s in schemes.schemes)))

    prev = schemes.schemes[scheme](versions[0])
    for curr in versions[1:]:
        curr = schemes.schemes[scheme](curr)
        if comparison == 'eq':
            res = prev == curr
        elif comparison == 'ne':
            res = prev != curr
        elif comparison == 'gt':
            res = prev > curr
        elif comparison == 'lt':
            res = prev < curr
        elif comparison == 'ge':
            res = prev >= curr
        elif comparison == 'le':
            res = prev <= curr
        if not res:
            print('ERROR: %s %s %s' % (prev, comparison_symbol(prev, curr), curr))
            return False
        prev = curr
    return True

def comparison_symbol(v1, v2):
    """
    Returns a character representation of the relationship between two objects
    """
    if v1 == v2:
        return '=='
    elif v1 > v2:
        return '>'
    elif v1 < v2:
        return '<'
    else:
        raise RuntimeError('Could not compare "%s" and "%s"' % (v1, v2))

