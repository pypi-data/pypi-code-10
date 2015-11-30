from collections import defaultdict
from nose.plugins import Plugin
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_name(test):
    return "{cls}.{method}".format(
        cls=test.test.__class__.__name__,
        method=test.test._testMethodName,
        )


class SlowTests(Plugin):
    enabled = True
    
    def begin(self):
        self._test_times = defaultdict(dict)

    def beforeTest(self, test):
        self._test_times[get_name(test)]['start'] = time.time()

    def afterTest(self, test):
        self._test_times[get_name(test)]['end'] = time.time()
    
    def finalize(self, result):
        times = [(k, v['end'] - v['start'],) for k, v in self._test_times.iteritems()]
        times.sort(key=lambda item: item[1], reverse=True)
        total_time = reduce(lambda memo, row: row[1] + memo, times, 0)
        num_tests = len(times)
        avg_time = total_time/float(num_tests)
        if num_tests % 2 == 0:
            t1 = times[num_tests/2][1]
            t2 = times[(num_tests/2)-1][1]
            median_time = (t1 + t2)/2.0
        else:
            median_time = times[num_tests/2][1]
        print "\n"
        print "Total Time:  {total}s".format(total=round(total_time, 3))
        print "Mean Time:   {avg}s".format(avg=round(avg_time, 3))
        print "Median Time: {median}s".format(median=round(median_time, 3))
        print "\nSlowest tests:"
        for name, t in times[:50]:
            t = round(t, 3)
            tstring = (str(t) + "s").ljust(8) + name
            if t > 1:
                tstring = bcolors.FAIL + tstring + bcolors.ENDC
            elif t > 0.1:
                tstring = bcolors.WARNING + tstring + bcolors.ENDC
            elif t < 0.01:
                tstring = bcolors.OKBLUE + tstring + bcolors.ENDC
            print tstring


