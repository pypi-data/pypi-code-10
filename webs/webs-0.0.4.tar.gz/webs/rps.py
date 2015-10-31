#!/usr/bin/env python
import sys
import math


def parse_number(num):
    if num.isdigit():
        return int(num)
    elif num.endswith('k'):
        return 10**3 * int(num[:-1])
    elif num.endswith('m'):
        return 10**6 * int(num[:-1])
    elif num.endswith('b'):
        return 10**9 * int(num[:-1])
    else:
        raise Exception('Could not parse number %s' % num)


def main():
    try:
        rps = parse_number(sys.argv[1])
        count = parse_number(sys.argv[2])
    except (IndexError, ValueError):
        print('Usage: rps <rps> <total-count>')
    else:
        parallel_count = math.ceil(count / float(rps))
        t_hr, t_sec = divmod(parallel_count, 3600)
        t_min, t_sec = divmod(t_sec, 60)
        items = []
        if t_hr:
            items.append('%d hr' % t_hr)
        if t_min:
            items.append('%d min' % t_min)
        if t_sec:
            items.append('%d sec' % t_sec)
        print(', '.join(items))
