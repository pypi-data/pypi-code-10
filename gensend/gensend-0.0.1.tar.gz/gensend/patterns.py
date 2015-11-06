import os
import json


class PatternList(list):

    @classmethod
    def from_path(cls, pattern_path):
        pattern_path = os.path.abspath(pattern_path)
        patterns = []

        with open(pattern_path) as f:
            if pattern_path.endswith('.txt'):
                patterns = [pattern.strip() for pattern in f]
            elif pattern_path.endswith('.json'):
                patterns = json.load(f)
        assert len(patterns), 'Unable to parse patterns file at {0}.'.format(pattern_path)
        return PatternList(patterns)
