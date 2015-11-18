import re

def match_pattern_url(pattern, url):
    match = None
    if pattern and url:
        match = re.match(pattern, url, re.M|re.I)
    return match
