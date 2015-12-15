from .template import Template, TemplateContainer
from . import cache, config
import os

def make(path, **kwargs):
    path = os.path.join(config.base_path, path)

    if cache.has(path):
        t = cache.get(path)
    else:
        t = Template(path)
        t.compile()

        cache.save(path, t)

    tc = TemplateContainer(t)
    tc.impart(**kwargs)
    return tc

def load_cache():
    def load_from_dir(d):
        for root, subdirs, files in os.walk(d):
            
            for subdir in subdirs:
                load_from_dir(os.path.join(d, subdir))
            
            for f in files:
                if f.endswith('.tmp'):
                    path = os.path.join(d, f)
                    t = Template(path)
                    t.compile()

                    cache.save(path, t)

    load_from_dir(config.base_path)
