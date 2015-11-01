import json
import os


def override(local_dict, prefix):
    suffixes = {
        '__INT': int,
        '__BOOL': lambda x: bool(int(x)),
        '__JSON': json.loads,
    }

    for key, value in os.environ.items():
        if key.startswith(prefix):
            key_name = key[len(prefix):]

            for suffix, processor in suffixes.items():
                if key_name.endswith(suffix):
                    value = processor(value)
                    key_name = key_name[:len(key_name)-len(suffix)]
                    break

            local_dict[key_name] = value
