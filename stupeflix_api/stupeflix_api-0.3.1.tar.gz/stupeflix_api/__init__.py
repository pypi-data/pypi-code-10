import warnings
import logging

warnings.warn("""
    This client and API are no longer supported,
    please go to http://developer.stupeflix.com
    to get the latest documentation.""")

# Setup basic logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
