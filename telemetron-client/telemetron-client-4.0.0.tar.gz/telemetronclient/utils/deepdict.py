"""
DeepDict utils module
"""


class DeepDict(object):
    """
    Utility class to make extended operations with dictionaries.
    """

    @classmethod
    def deep_merge(cls, *args):
        """
        Merge two or more dictionaries, in order, into the first dictionary.

        Retuns a copy of the first dict merged with the rest of dictionaries.
        """

        def _deep_merge(left, right):
            """
            Merge two dictionaries: 'right' into 'left'.

            Retuns a copy of 'left' with elements from right.
            """

            for key, value in right.iteritems():
                if isinstance(value, dict):
                    res[key] = DeepDict.deep_merge(left[key], right[key])
                else:
                    left[key] = value
            return left

        res = dict(args[0])
        for arg in args[1:]:
            _deep_merge(res, arg)
        return res

    @classmethod
    def diff(cls, left, right):
        """
        Diff not yet implemented
        """
        raise NotImplementedError
