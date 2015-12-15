base_path = 'templates/'

# possibilities to override config from external sources
try:
    from ..config import amaze

    for k, v in vars(amaze).items():
        if not k.startswith('__'):
            globals()[k] = v
except:
    pass

try:
    from ...config import amaze

    for k, v in vars(amaze).items():
        if not k.startswith('__'):
            globals()[k] = v
except:
    pass
