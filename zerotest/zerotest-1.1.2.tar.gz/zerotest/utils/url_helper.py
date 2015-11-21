# compatible
try:
    from urlparse import urlparse, urljoin
except ImportError:
    # python3
    from urllib.parse import urlparse, urljoin
