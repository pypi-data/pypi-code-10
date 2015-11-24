import logging


# Setup basic logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
