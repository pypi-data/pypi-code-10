"""Number-crunching functions for the duolingo-graph command."""
from collections import Counter, namedtuple
from enum import Enum
from functools import total_ordering
from itertools import groupby
# from igraph.summary import OUT, IN, ALL
OUT = 1
IN = 2
ALL = 3

__all__ = [
    'CourseType',
    'count', 'rank',
    'rank_courses', 'rank_progress', 'rank_avg_progress'
]


class CourseType(Enum):
    """
    Identifies whether a course is for speakers and/or learners of a language.
    """
    SPEAKERS = 1
    LEARNERS = 2
    BOTH = 3

    @property
    def _tuple(self):
        """
        Tuple of indices into graph.vs; 0 indicates speakers and 1 indicates
        learners.
        """
        return {1: (0,),
                2: (1,),
                3: (0, 1,)}[self.value]

    @property
    def _mode(self):
        """Graph edge mode for this course type."""
        return {1: OUT,
                2: IN,
                3: ALL}[self.value]


def count(graph, kind, key):
    """Sums up a function of course, language for courses of a given type."""
    counts = Counter()
    for edge in graph.es:
        for i in kind._tuple:
            name = graph.vs[edge.tuple[i]]['name']
            counts[name] += key(edge, graph.vs[edge.tuple[i]])
    return counts


def distance(graph, kind):
    """
    Figures out the average distance along the given paths (learning, speaking,
    or both) to a given language.
    """
    dists = {}
    for vertex in graph.vs:
        paths = graph.get_all_shortest_paths(vertex, mode=kind._mode)
        name = vertex['name']
        dists[name] = sum(len(path) for path in paths) / len(paths)
    return dists


def rank(counts):
    """
    Calculates a list of number, list pairs which correspond to the counts
    returned by the count function and languages which match that count, sorted
    in descending order by count.
    """
    return [
        (key, [lang[0] for lang in group])
        for key, group in groupby(
            sorted(
                counts,
                key=lambda x: x[1],
                reverse=True,
            ),
            key=lambda x: x[1],
        )
    ]


def rank_avg_distance(graph, kind=CourseType.BOTH):
    """
    Calculates a list of int, list pairs which correspond to the average
    distance from one language to another language, sorted in ascending order
    by average distance.

    graph:    the Duolingo graph
    kind:     CourseType to describe who the courses are for (default BOTH)
    """
    return rank(distance(graph, kind).items())


def rank_courses(graph, kind=CourseType.BOTH):
    """
    Calculates a list of int, list pairs which correspond to the amount of
    courses offered the languages which match that number, sorted in descending
    order by course amount.

    graph:    the Duolingo graph
    type:     CourseType to describe who the courses are for (default BOTH)
    """
    return rank(count(graph, kind, lambda e, v: 1).items())


def rank_progress(graph, kind=CourseType.BOTH):
    """
    Calculates a list of float, list pairs which correspond to the cumulative
    progress of courses offered and the languages which match that number,
    sorted in descending order by course progress.

    graph:    the Duolingo graph
    kind:     CourseType to describe who the courses are for (default BOTH)
    """
    return rank(count(graph, kind, lambda e, v: e['progress']).items())


def rank_avg_progress(graph, kind=CourseType.BOTH):
    """
    Calculates a list of float, list pairs which correspond to the average
    progress of courses offered and the languages which match that number,
    sorted in descending order by average progress.

    graph:    the Duolingo graph
    kind:     CourseType to describe who the courses are for (default BOTH)
    """
    courses = count(graph, kind, lambda e, v: 1)
    progress = count(graph, kind, lambda e, v: e['progress'])
    return rank((k, progress[k] / courses[k]) for k in courses.keys())
