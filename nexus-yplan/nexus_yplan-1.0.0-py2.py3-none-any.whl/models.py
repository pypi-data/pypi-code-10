from nexus.checks import pre_checks_requirements

# This is here so that it gets run at Django import time, on old versions of Django
pre_checks_requirements()
