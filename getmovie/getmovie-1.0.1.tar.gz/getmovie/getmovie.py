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
        if type(options[0]) is tuple:
            print("Selecting {}...".format(options[0][1]), file=sys.stderr)
        else:
            print("Selecting {}...".format(options[0]), file=sys.stderr)
        return options[0][0] if type(options[0]) is tuple else options[0]
    if type(options[0]) is tuple:
        choices = ["{}: {}".format(a, b) for a,b in options]
    else:
        choices = options
    print_multicolumn(choices)
    if os.isatty(sys.stdout.fileno()):
        return prompt(q)

def prompt(*objs):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return input(*objs)
    finally:
        sys.stdout = old_stdout

def get_movie(movie="", movie_id="", quality=""):
    if movie_id:
        if not movie_id.isdigit():
            return "ID parameter must be a number"
        data = requests.get("https://yts.ag/api/v2/movie_details.json", params={"movie_id": movie_id}).json()
        if "data" in data:
            movie = data["data"]["movie"]
        else:
            return "No results for {}".format(movie_id)
    else:
        data = requests.get("https://yts.ag/api/v2/list_movies.json", params={"query_term": movie}).json()
        if "data" in data:
            results = {m["id"]: m for m in data["data"]["movies"]}
            picked = movie_id or choice([(k, v["title_long"]) for k,v in results.items()], "Enter movie ID: ")
            if picked in results:
                movie = results[picked]
            else:
                return "Invalid movie ID choice ({})".format(picked)
        else:
            return "No results for {}".format(movie)
    torrents = {t["quality"].lower(): t for t in movie["torrents"]}
    picked = quality or choice(list(torrents.keys()), "Enter torrent quality: ")
    if picked.lower() in torrents:
        return torrents[picked]["url"]
    else:
        return "Invalid quality choice ({})".format(picked)

def main():
    parser = argparse.ArgumentParser(prog="getmovie")
    parser.add_argument("-m", "--movie", help="Movie search term")
    parser.add_argument("-i", "--id", help="Specify ID, if you know it")
    parser.add_argument("-q", "--quality", help="Specify quality. Defaults to 720p")
    args = parser.parse_args()
    if not args.movie and not args.id:
        parser.print_usage()
        print("You need to specify either a movie search term (-m) or a movie ID (-i)")
        return 30
    print(get_movie(args.movie, args.id, args.quality))
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
