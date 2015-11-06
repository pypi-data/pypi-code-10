#!/usr/bin/env python3

import argparse
import random
import string
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup as Soup
from getlyrics import getlyrics # lol

def get_random_song_from_artist(artist_href=None, song_href=None):
    """ Picks random song from azlyrics artist page, returns lyrics
        via getlyrics.parse_lyrics_page

    :returns: str
    :rtype: str
    """
    if not song_href and artist_href:
        soup = Soup(urlopen("http://www.azlyrics.com/" + artist_href).read(), "html.parser")
        song_href = random.choice(soup.findAll('a', {'target': '_blank'}))["href"][2:] # 2: to remove the .. from the start of the url
    lyrics = getlyrics.parse_lyrics_page("http://azlyrics.com/" + song_href)
    return song_href, lyrics

def get_letter(letter=None):
    """ Returns list of artist hrefs for random or specified letter
        from azlyrics.com

    >>> get_letter()
    ["a/a.html", ...]

    :returns: List of hrefs from azlyrics.com/{letter}.html
    :rtype: [str, ...]
    """
    letter = letter if letter else random.choice(string.ascii_lowercase)
    soup = Soup(urlopen("http://www.azlyrics.com/{}.html".format(letter)).read(), "html.parser")
    outp = [a["href"] for a in soup.find('div', {'class': 'main-page'}).findAll('a')]
    return outp

def main():
    parser = argparse.ArgumentParser(prog="randomlyric")
    parser.add_argument("--letter", help="Specify letter instead of allowing random choice")
    parser.add_argument("--artist-href", help="Specifies the artist you want. No preceding slash. Example: m/mutemath.html")
    parser.add_argument("--song-href", help="Specifies the song you want. No preceding slash. Example: lyrics/mutemath/typical.html")
    args = parser.parse_args()
    artist_href = random.choice(get_letter(args.letter)) if not args.artist_href else args.artist_href
    song_href, lyrics = get_random_song_from_artist(artist_href, args.song_href)
    lyric = ", ".join(line for line in random.choice(lyrics.split("\n\n")).strip().split("\n") if not line[0] == "[" and line)
    print("{} ( http://www.azlyrics.com{} )".format(lyric, song_href))
    return 0

if __name__ == "__main__":
    sys.exit(main())
