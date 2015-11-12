import json

ENV_PREFIX = 'JSON_URL_REWRITER_'
KEYS = ENV_PREFIX + 'KEYS'


def load_from_environment(env):
    if KEYS not in env:
        return {}

    keys = json.loads(env[KEYS])

    if not keys:
        return {}

    return {
        'keys': keys
    }
