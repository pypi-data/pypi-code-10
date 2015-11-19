#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import shutil
import sys

from prettytable import PrettyTable, NONE

input = raw_input if hasattr(__builtins__, 'raw_input') else input

def print_multicolumn(alist):
    """Formats a list into columns to fit on screen. Similar to `ls`. From http://is.gd/6dwsuA (daniweb snippet, search for func name)

    :param alist: list of data to print into columns

    >>> print_multicolumn(["a", "aa", "aaa", "aaaa"])
      a   aa   aaa   aaaa
    """
    try:
        ncols = shutil.get_terminal_size((80, 20)).columns // max(len(a) for a in alist)
    except AttributeError:
        ncols = 80 // max(len(a) for a in alist)
    try:
        nrows = - ((-len(alist)) // ncols)
        ncols = - ((-len(alist)) // nrows)
    except ZeroDivisionError:
        print("\n".join(alist), file=sys.stderr)
        return
    t = PrettyTable([str(x) for x in range(ncols)])
    t.header = False
    t.align = 'l'
    t.hrules = NONE
    t.vrules = NONE
    chunks = [alist[i:i+nrows] for i in range(0, len(alist), nrows)]
    chunks[-1].extend('' for i in range(nrows - len(chunks[-1])))
    chunks = zip(*chunks)
    for c in chunks:
        t.add_row(c)
    print(t, file=sys.stderr)

def choice(options, q="Enter your selection: "):
    if len(options) == 1:
        print("Selecting {}...".format(options[0][1]), file=sys.stderr)
        return options[0][0]
    print_multicolumn(["{}: {}".format(a, b) for a,b in options])
    if os.isatty(sys.stdout.fileno()):
        return prompt(q)

def prompt(*objs):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return input(*objs)
    finally:
        sys.stdout = old_stdout

def get_movie(movie, movie_id="", quality=""):
    data = requests.get("https://yts.ag/api/v2/list_movies.json", params={"query_term": movie}).json()
    if "data" in data:
        results = {m["id"]: m for m in data["data"]["movies"]}
        picked = movie_id or choice([(k, v["title_long"]) for k,v in results.items()], "Enter movie ID: ")
        if picked in results:
            movie = results[picked]
            torrents = {t["quality"][:-1]: t for t in movie["torrents"]}
            picked = quality or choice([(k, "") for k in torrents.keys()], "Enter torrent quality: ")
            if picked[-1] == "p":
                picked = picked[:-1]
            if picked in torrents:
                return torrents[picked]["url"]
            else:
                return "Invalid quality choice ({})".format(picked)
        else:
            return "Invalid movie ID choice ({})".format(picked)
    else:
        return "No results for {}".format(movie)

def main():
    parser = argparse.ArgumentParser(prog="getmovie")
    parser.add_argument("movie", help="Movie search term")
    parser.add_argument("-i", help="Specify ID, if you know it")
    parser.add_argument("-q", help="Specify quality. Defaults to 720p")
    args = parser.parse_args()
    print(get_movie(args.movie, movie_id=args.i, quality=args.q))
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
