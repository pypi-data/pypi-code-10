import datetime
import random

import abc


NULL_OUTPUT = object()


class Experiment(object):
    __metaclass__ = abc.ABCMeta
    current_func = None
    candidate_func = None

    def __init__(self, name, current_func, candidate_func):
        # TODO check type of name, current_func, candidate_func
        self.name = name
        self.current_func = current_func
        self.candidate_func = candidate_func

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def compare(self, current_output, candidate_output, comparator=None):
        # TODO find a way to pass the comparator from the Concrete class
        # TODO test
        if comparator is None:
            comparator = lambda a, b: a == b

        is_equal = comparator(current_output, candidate_output)
        mismatch = None
        if not is_equal:
            mismatch = {
                'current': current_output,
                'candidate': candidate_output,
            }
        return not is_equal, mismatch

    @abc.abstractmethod
    def publish_duration(self, current_duration, candidate_duration):
        pass

    @abc.abstractmethod
    def publish_mismatch(self, is_mismatch, context):
        # TODO define the schema
        # maybe use https://github.com/seperman/deepdiff
        pass

    @abc.abstractmethod
    def is_enabled(self):
        pass


class Runner(object):
    def __init__(self, experiment, compare_rate=0.5):
        self.experiment = experiment
        self.compare_rate = compare_rate

        self._is_enabled_cache = None
        self._should_compare_cache = None

    def should_compare(self):
        if self._should_compare_cache is None:
            self._should_compare_cache = self.is_enabled() and random.random() < self.compare_rate
        return self._should_compare_cache

    def is_enabled(self):
        if self._is_enabled_cache is None:
            self._is_enabled_cache = self.experiment.is_enabled()
        return self._is_enabled_cache

    def run(self):
        self.experiment.set_up()

        run_current = (not self.is_enabled()) or self.should_compare()
        run_candidate = self.is_enabled()

        current_duration = None
        current_output = None
        candidate_output = None
        candidate_duration = None

        if run_current:
            start = datetime.datetime.now()
            current_output = self.experiment.current_func()
            end = datetime.datetime.now()
            current_duration = (end - start).total_seconds() * 1000

        if run_candidate:
            start = datetime.datetime.now()
            candidate_output = self.experiment.candidate_func()
            end = datetime.datetime.now()
            candidate_duration = (end - start).total_seconds() * 1000

        self.experiment.tear_down()
        if self.should_compare():
            is_mismatch, mismatch_context = self.experiment.compare(
                current_output, candidate_output)
            self.experiment.publish_mismatch(is_mismatch, mismatch_context)
        self.experiment.publish_duration(current_duration, candidate_duration)

        self._reset_cached_values()

    def _reset_cached_values(self):
        self._is_enabled_cache = None
        self._should_compare_cache = None
